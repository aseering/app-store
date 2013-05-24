# Create your views here.

from django.views.generic.base import TemplateView

class HomePageView(TemplateView):
    template_name = 'index.html'

class AboutView(TemplateView):
    template_name = 'about.html'

class DownloadView(TemplateView):
    template_name = 'verticapp_download.html'
