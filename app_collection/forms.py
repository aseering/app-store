from django.forms import forms, ModelForm
from django.template.defaultfilters import slugify
from app_collection.models import App

class AppForm(ModelForm):
    class Meta:
        model = App
        exclude = ('submitter',
                   'status',
                   'shortname')

    def clean_name(self):
        print self.cleaned_data
        name = self.cleaned_data['name']
        shortname = slugify(name)
        if App.objects.filter(shortname=shortname):
            raise forms.ValidationError("Can't use the name '%s' because the shortname '%s' is already in use" % (name, shortname))
        return self.cleaned_data['name']

