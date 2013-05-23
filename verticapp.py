#!/usr/bin/env python

import argparse
import urllib, urllib2
import tempfile
import os, sys
import subprocess
import json
import re
import random

## Unique id for this session
## Can't run two instances of some commands with the same session ID safely at once
VERTICAPP_SESSION_ID = "%d_%d" % (os.getpid(), random.randint(1,1000000000))

SERVER = os.environ.get('VERTICAPP_SERVER')
if not SERVER:
    print "Please set the VERTICAPP_SERVER environment variable to point at your VerticApps server"
    print "For example, 'export VERTICAPP_SERVER=http://localhost:8000/'"
    sys.exit(0)

URL_TEMPLATE = SERVER + "apps/%s/"
INFO_TEMPLATE = URL_TEMPLATE + "app.json"
LIST_URL = SERVER + "apps/list.json"

SERVER_VERSION = None

def find_server_version():
    svn_version = None
    match_re = re.compile(r'static const char \*VERTICA_BUILD_ID_Revision *= "([0-9]*)";')
    with open('/opt/vertica/sdk/include/BuildInfo.h') as f:
        for l in f:
            matched_l = match_re.search(l)
            if matched_l:
                svn_version = matched_l.group(1)

    if svn_version:
        return "r%s" % svn_version

SERVER_VERSION = find_server_version()

if not SERVER_VERSION:
    print "Can't determine the version of the installed SDK"
    print "Please make sure that '' is present and is up-to-date."
    print "Proceeding without a specified version."
    print "Functionality may be limited."

## {{{ http://code.activestate.com/recipes/577058/ (r2)
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.
    
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":"yes",   "y":"yes",  "ye":"yes",
             "no":"no",     "n":"no"}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while 1:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")
## end of http://code.activestate.com/recipes/577058/ }}}

## {{{ http://code.activestate.com/recipes/552732/ (r1)
import os
def rm_rf(d):
    for path in (os.path.join(d,f) for f in os.listdir(d)):
        if os.path.isdir(path):
            rm_rf(path)
        else:
            os.unlink(path)
    os.rmdir(d)
## end of http://code.activestate.com/recipes/552732/ }}}

## {{{ http://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python

def download_progressbar(url, path):
    file_name = os.path.join(path, url.split('/')[-1])
    u = urllib2.urlopen(url)
    with open(file_name, 'wb') as f:
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (file_name, file_size)
        
        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            
            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,
        
    return file_name
        

## end of http://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python }}}

## Generic utility functions
def sql_str_escape(st):
    return st.replace("'", "''")


## Actual execution logic

def main():
    parser = argparse.ArgumentParser(description="Install Vertica UDx's from the unofficial verticapps repository")

    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--install", '-i',
                         help="Name of the package to install")
    actions.add_argument("--remove", '-r',
                         help="Name of the package to remove")
    actions.add_argument("--list", '-l', action="store_true",
                         help="List all packages available in the repository")
    actions.add_argument("--search", '-s',
                         help="Search for a package matching the specified keyword")

    parser.add_argument("--server",
                        help="Server to download from, ie., 'http://example.com'/")

    args = parser.parse_args()

    if args.server:
        SERVER = args.server

    ## Don't support uninstall just yet
    if args.install:
        install(args)
    elif args.remove:
        remove(args)
    elif args.list:
        list_(args)
    elif args.search:
        search(args)
    else:
        print >>sys.stderr, "Please specify an action (--install, --remove, --list, --search)"
        print >>sys.stderr, "Use --help for more information"

def install(args):
    install_impl(args.install)

def install_impl(app_slug):
    url = INFO_TEMPLATE % app_slug

    try:
        info_json_f = urllib2.urlopen(url)
    except:
        print >>sys.stderr, "Can't find application '%s'" % app_slug
        print >>sys.stderr, "Tried URL: %s" % url
        sys.exit(0)

    app_info = None
    try:
        app_info = json.load(info_json_f)
    except Exception, e:
        print >>sys.stderr, "Can't find data for application '%s'" % app_slug
        sys.exit(0)
        
    print "App:", app_info['name']
    print app_info['description']

    if not query_yes_no("Install this application?"):
        print "Install cancelled."
        sys.exit(0)

    if not SERVER_VERSION in app_info['appinstance_set'].keys():
        print "Server API version '%s' not found in supported-version list [%s] for app %s.  Can't install." % (SERVER_VERSION, ", ".join(app_info['appinstance_set'].keys()), app_info['name'])
        sys.exit(0)

    has_tarball = False
    if app_info['appinstance_set'][SERVER_VERSION]['tarball']:
        has_tarball = True
        print "App has associated helper files; downloading shell_package as a dependency..."
        install_impl('shell-package')

    so_url = SERVER + "media/" + app_info['appinstance_set'][SERVER_VERSION]['so_file']
    if has_tarball:
        tar_url = SERVER + "media/" + app_info['appinstance_set'][SERVER_VERSION]['tarball']

    tmpdir = tempfile.mkdtemp()
    setup_sql_file = os.path.join(tmpdir, "setup.sql")
    
    inst_file = download_progressbar(so_url, tmpdir)
    if has_tarball:
        tarball_file = download_progressbar(tar_url, tmpdir)
        # HACK:  Hex-encode the tarball file so we can load it with the stock loader
        tarball_hexenc_file = tarball_file + ".hexcsv"
        hexencode_file(tarball_file, tarball_hexenc_file)
            
    with open(setup_sql_file, "w") as f:
        f.write("\\set libfile '\\'%s\\''\n" % inst_file.replace("'", "''"))
        f.write("CREATE SCHEMA verticapp;  -- May already exist; this is ok\n")
        f.write("CREATE TABLE IF NOT EXISTS verticapp.installed_apps (name VARCHAR, shortname VARCHAR, description VARCHAR(8192), github_url VARCHAR(512), setup_sql VARCHAR(65000), remove_sql VARCHAR(65000));\n")
        f.write("INSERT INTO verticapp.installed_apps VALUES ('%s', '%s', '%s', '%s', '%s', '%s');\n" \
                % tuple(map(sql_str_escape, 
                            [app_info['name'], app_info['shortname'], app_info['description'],
                             "http://github.com/%s/%s/" % (app_info['github_account'],
                                                           app_info['github_project']), 
                             app_info['appinstance_set'][SERVER_VERSION]['setup_sql'],
                             app_info['appinstance_set'][SERVER_VERSION]['remove_sql']])))
        f.write("\n")

        if has_tarball:
            f.write("-- Install the tarball first\n")
            f.write("CREATE TABLE verticapp.tmp_install_%s (id IDENTITY, data VARBINARY(32500)) UNSEGMENTED ALL NODES;  -- Should not already exist\n" % VERTICAPP_SESSION_ID)
            f.write("COPY verticapp.tmp_install_%s (data_filler FILLER VARCHAR(65000), data AS HEX_TO_BINARY(data_filler)) FROM '%s' NO ESCAPE;\n" % (VERTICAPP_SESSION_ID, tarball_hexenc_file.replace("'", "''")))
            f.write("SELECT shell_execute_binary(data USING PARAMETERS cmd='mkdir -p /opt/vertica/config/verticapp/%s && tar xzvC /opt/vertica/config/verticapp/%s') OVER (PARTITION BY segval ORDER BY id) FROM verticapp.tmp_install_%s, onallnodes;\n" % (app_info['shortname'], app_info['shortname'], VERTICAPP_SESSION_ID))
            f.write("DROP TABLE verticapp.tmp_install_%s;\n" % VERTICAPP_SESSION_ID)
            f.write("\n")

        f.write(app_info['appinstance_set'][SERVER_VERSION]['setup_sql'])

    print "Downloaded!  Running installation through vsql..."
    success = subprocess.call(["vsql", "-a", "-f", setup_sql_file])
    if success == 0:
        print "Installation successful!"

        ## Clean up!
        rm_rf(tmpdir)
    else:
        print "vsql reported an error.  Please see the above output for details."
        print "Setup script and UDx .so file are in [%s]." % tmpdir

def hexencode_file(src, dest):
    READ_SIZE = 65000/2  ## We're doubling the string size
    with open(src, "r") as src_file:
        with open(dest, "w") as dest_file:
            while True:
                data = src_file.read(READ_SIZE)
                if data:
                    data = data.encode('hex')
                    dest_file.write(data + '\n')
                else:
                    break
                

def remove(args):
    url = INFO_TEMPLATE % args.remove
    info_json_f = urllib2.urlopen(url)
    app_info = None
    try:
        app_info = json.load(info_json_f)
    except Exception, e:
        print >>sys.stderr, "Can't find applicaion '%s'" % args.install
        
    print "App:", app_info['name']
    print app_info['description']

    if not query_yes_no("Remove this application?"):
        print "Removal cancelled."
        sys.exit(0)

    if not SERVER_VERSION in app_info['appinstance_set'].keys():
        print "Server version '%s' not found in key-set [%s] for app %s.  Can't install." % (SERVER_VERSION, ", ".join(app_info['appinstance_set'].keys()), app_info['name'])
        sys.exit(0)

    url = SERVER + "media/" + app_info['appinstance_set'][SERVER_VERSION]['so_file']
    
    tmpdir = tempfile.mkdtemp()
    remove_sql_file = os.path.join(tmpdir, "remove.sql")
    
    with open(remove_sql_file, "w") as f:
        f.write(app_info['appinstance_set'][SERVER_VERSION]['remove_sql'])

    print "Running removal through vsql..."
    success = subprocess.call(["vsql", "-a", "-f", remove_sql_file])
    if success == 0:
        print "Removal successful!"

        ## Clean up!
        rm_rf(tmpdir)
    else:
        print "vsql reported an error.  Please see the above output for details."
        print "Tear-down script is in [%s]." % tmpdir

def _fetch_app_list(url):
    info_json_f = urllib2.urlopen(url)
    try:
        return json.load(info_json_f)
    except Exception, e:
        print >>sys.stderr, "Can't download list from server"
        sys.exit(0)
        
def _print_app(app, short_list=False):
    print 'App: %s ("%s")' % (app['shortname'], app['name'])
    print 'Author: "%s %s" <%s>' % (app['submitter']['first_name'], app['submitter']['last_name'], app['submitter']['email'])
    print "Source: <http://github.com/%s/%s/>" % (app['github_account'], app['github_project'])
    if short_list:
        print "\n".join(["\t" + x for x in app['description'].split('\n')][:5])
    else:
        print "\n".join(["\t" + x for x in app['description'].split("\n")])

def list_(args):
    url = LIST_URL
    app_list = _fetch_app_list(url)
    
    for app in app_list:
        if SERVER_VERSION and (not SERVER_VERSION in app['appinstance_set'].keys()):
            continue  ## Skip apps that don't match our server version
        print
        _print_app(app, short_list=True)

def search(args):
    url = LIST_URL
    search_term = args.search.upper()
    app_list = _fetch_app_list(url)
    
    for app in app_list:
        if (search_term in json.dumps(app).upper()):
            print
            _print_app(app)


if __name__ == "__main__":
    main()
