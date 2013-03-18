from django.forms import ModelForm
from app_collection.models import App

class AppForm(ModelForm):
    class Meta:
        model = App
        exclude = ('submitter', 'submission_date', 'last_updated_date')

    def __init__(user, *args, **kwargs):
        self.user = user
        super(AppForm, self).__init__(*args, **kwargs)
