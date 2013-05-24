from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from app_collection.models import App, AppInstance
from app_collection.forms import AppForm, InstanceForm, PartialInstanceForm
from utils.json_response import json_response

# Create your views here.

def list_apps(request):
    return render(request, 'list_apps.html',
                  {'apps': App.objects.filter(status="ACCEPTED").select_related('submitter').prefetch_related('appinstance_set').prefetch_related('appinstance_set__app').order_by('name')})

@json_response
def list_apps_json(request):
    ## TODO: Make this not be O(n) queries on appinstance_set
    apps = App.objects.filter(status="ACCEPTED").select_related('submitter').prefetch_related('appinstance_set')
    return [{'submission_date': app.submission_date,
             'last_updated_date': app.last_updated_date,
             'name': app.name,
             'shortname': app.shortname,
             'description': app.description,
             'github_account': app.github_account,
             'github_project': app.github_project,
             'submitter': {'email': app.submitter.email,
                           'first_name': app.submitter.first_name,
                           'last_name': app.submitter.last_name},
             'appinstance_set': dict((inst.api_version.sdk_version,
                                      {'setup_sql': inst.setup_sql,
                                       'remove_sql': inst.remove_sql,
                                       'so_file': inst.so_file,
                                       'tarball': inst.tarball,
                                       'sdk_version': inst.api_version.sdk_version,
                                       'brand_version': inst.api_version.brand_version})
                                 for inst in app.appinstance_set.all()) 
             } for app in apps]
                                                        

def show_app(request, app_name):
    app = get_object_or_404(App, shortname=app_name)
    return render(request, 'show_app.html',
                  {'app': app})

@json_response
def show_app_json(request, app_name):
    ## TODO: Test me!
    app = get_object_or_404(App.objects.select_related('submitter').prefetch_related('appinstance_set').prefetch_related('appinstance_set__api_version'),
                            shortname=app_name)
    return {'submission_date': app.submission_date,
            'last_updated_date': app.last_updated_date,
            'name': app.name,
            'shortname': app.shortname,
            'description': app.description,
            'status': app.status,
            'description': app.description,
            'appinstance_set': dict((inst.api_version.sdk_version,
                                     {'setup_sql': inst.setup_sql,
                                      'remove_sql': inst.remove_sql,
                                      'so_file': inst.so_file,
                                      'tarball': inst.tarball,
                                      'sdk_version': inst.api_version.sdk_version,
                                      'brand_version': inst.api_version.brand_version})
                                    for inst in app.appinstance_set.all()),
            'github_account': app.github_account,
            'github_project': app.github_project,
            'submitter': {'email': app.submitter.email,
                          'first_name': app.submitter.first_name,
                          'last_name': app.submitter.last_name}
            }

@login_required
def my_apps(request):
    return render(request, 'my_apps.html',
                  {'apps': App.objects.filter(submitter=request.user)})

@login_required
def submit_app(request):
    if request.method == 'POST':
        ## Handle a form submission
        app_form = AppForm(request.POST, request.FILES)
        inst_form = PartialInstanceForm(request.POST, request.FILES)
        if app_form.is_valid() and inst_form.is_valid():
            rec = app_form.save(commit=False)
            rec.submitter = request.user
            rec.shortname = slugify(rec.name)
            rec.status = "ACCEPTED"
            rec.save()
            inst = inst_form.save(commit=False)
            inst.app = rec

            ## New uploads clobber existing content
            AppInstance.objects.filter(app=inst.app, api_version=inst.api_version).delete()

            inst.save()
            return redirect(my_apps)

        ## 'form' variable falls through, with errors attached
    else:
        app_form = AppForm()
        inst_form = PartialInstanceForm()
        
    return render(request, 'submit_app_inst_form.html',
                  {'app_form': app_form, 'inst_form': inst_form})

@login_required
def submit_instance(request):
    if request.method == 'POST':
        ## Handle a form submission
        form = InstanceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(my_apps)
        ## 'form' variable falls through, with errors attached
    else:
        form = InstanceForm()
        
    return render(request, 'submit_form.html', {'form': form})
