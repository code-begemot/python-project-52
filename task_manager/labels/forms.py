from django.forms import ModelForm
from task_manager.labels.models import Label


class LabelNameForm(ModelForm):
    class Meta:
        model = Label
        fields = ['name']
