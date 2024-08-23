from django_filters import FilterSet, BooleanFilter, ModelChoiceFilter

from django.forms import CheckboxInput
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import Task
from task_manager.labels.models import Label


class TaskFilter(FilterSet):
    my_tasks = BooleanFilter(widget=CheckboxInput,
                             method='filter_creator',
                             label=_('Only my tasks'))

    def filter_creator(self, queryset, *args, **kwargs):
        is_my_tasks = args[-1]
        if is_my_tasks:
            creator = getattr(self.request, 'user', None)
            return queryset.filter(creator=creator)
        return queryset

    choice_label = ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Label'),
        field_name='labels',
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'choice_label', 'my_tasks']
