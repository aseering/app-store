from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from app_collection.models import App
from app_collection.forms import AppForm

# Create your views here.

def list_apps(request):
    return render(request, 'list_apps.html',
                  {'apps': App.objects.filter(status="ACCEPTED")})

def show_app(request, app_name):
    app = get_object_or_404(App, name=app_name)
    return render(request, 'show_app.html',
                  {'app': app})

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
