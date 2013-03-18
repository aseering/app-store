# Create your views here.

from django.views.generic.base import TemplateView

class HomePageView(TemplateView):
    template_name = 'index.html'
