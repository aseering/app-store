#!/usr/bin/env python

import argparse
import urllib, urllib2
import tempfile
import os, sys
import subprocess
import json

SERVER = "http://verticapps.seering.org/"
URL_TEMPLATE = SERVER + "apps/%s/"
INFO_TEMPLATE = URL_TEMPLATE + "app.json"

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

def main():
    parser = argparse.ArgumentParser(description="Install Vertica UDx's from the unofficial verticapps repository")

    parser.add_argument("--install", '-i',
                        help="Name of the package to install")
    parser.add_argument("--server", '-s',
                        help="Server to download from, ie., 'http://example.com'/")

    args = parser.parse_args()

    SERVER = args.server

    ## Don't support uninstall just yet
    install(args)

def install(args):
    url = INFO_TEMPLATE % args.install
    info_json_f = urllib2.urlopen(url)
    app_info = None
    try:
        app_info = json.load(info_json_f)
    except Exception, e:
        print >>sys.stderr, "Can't find applicaion '%s'" % args.install
        
    print "App:", app_info['name']
    print app_info['description']

    if not query_yes_no("Install this application?"):
        print "Install cancelled."
        sys.exit(0)

    url = SERVER + "media/" + app_info['app']
    
    tmpdir = tempfile.mkdtemp()
    setup_sql_file = os.path.join(tmpdir, "setup.sql")
    
    inst_file = download_progressbar(url, tmpdir)
    with open(setup_sql_file, "w") as f:
        f.write("\\set libfile '\\'%s\\''\n" % inst_file.replace("'", "''"))
        f.write(app_info['setup_sql'])

    print "Downloaded!  Running installation through vsql..."
    success = subprocess.call(["vsql", "-a", "-f", setup_sql_file])
    if success == 0:
        print "Installation successful!"
    else:
        print "vsql reported an error.  Please see the above output for details."

    ## Clean up!
    rm_rf(tmpdir)


if __name__ == "__main__":
    main()
