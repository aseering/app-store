from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from app_collection.models import App
from app_collection.forms import AppForm
from utils.json_response import json_response

# Create your views here.

def list_apps(request):
    return render(request, 'list_apps.html',
                  {'apps': App.objects.filter(status="ACCEPTED")})

@json_response
def list_apps_json(request):
    return App.objects.filter(status="ACCEPTED").select_related('submitter')\
        .values('submission_date',
                'last_updated_date',
                'name',
                'shortname',
                'description',
                'github_account',
                'github_project',
                'app',
                'submitter__email',
                'submitter__first_name',
                'submitter__last_name')
                                                        

def show_app(request, app_name):
    app = get_object_or_404(App, name=app_name)
    return render(request, 'show_app.html',
                  {'app': app})

@json_response
@login_required
def show_app_json(request, app_name):
    app = get_object_or_404(App.models.select_related('submitter'),
                            name=app_name)
    return {'submission_date': app.submission_date,
            'last_updated_date': app.last_updated_date,
            'name': app.name,
            'shortname': app.shortname,
            'description': app.description,
            'status': app.status,
            'description': app.description,
            'github_account': app.github_account,
            'github_project': app.github_project,
            'app': app.app,
            'submitter__email': app.submitter.email,
            'submitter__first_name': app.submitter.first_name,
            'submitter__last_name': app.submitter.last_name}

@login_required
def my_apps(request):
    return render(request, 'my_apps.html',
                  {'apps': App.objects.filter(submitter=request.user)})

@login_required
def submit_app(request):
    if request.method == 'POST':
        ## Handle a form submission
        form = AppForm(request.POST, request.FILES)
        if form.is_valid():
            rec = form.save(commit=False)
            rec.submitter = request.user
            rec.shortname = slugify(rec.name)
            rec.status = "PENDING"
            rec.save()
            return redirect(my_apps)

        ## 'form' variable falls through, with errors attached
    else:
        form = AppForm()
        
    return render(request, 'submit_form.html', {'form': form})
