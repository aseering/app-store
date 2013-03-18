from django.shortcuts import render, get_object_or_404, redirect
from app_collection.models import App
from app_collection.forms import AppForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def list_apps(request):
    return render(request, 'list_apps.html',
                  {'apps': App.objects.filter(status=App.statuses.ACCEPTED)})

def show_app(request, app_name):
    app = get_object_or_404(App, name=app_name)
    return render(request, 'show_app.html',
                  {'app': app})

@login_required
def my_apps(request):
    return render(request, 'my_apps.html',
                  {'apps': App.objects.filter(user=request.user)})

@login_required
def submit_app(request):
    if request.method == 'POST':
        ## Handle a form submission
        form = AppForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            redirect(list_apps)

        ## 'form' variable falls through, with errors attached
    else:
        form = AppForm(request.user)
        
    return render(request, 'submit_form.html', {'form': form})
