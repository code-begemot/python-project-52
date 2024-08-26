from django.shortcuts import redirect

from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from task_manager.labels.models import Label
from task_manager.labels.forms import LabelNameForm


class IndexView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = messages.get_messages(self.request)
        print(context)
        return context


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = LabelNameForm
    model = Label
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels')
    success_message = _('Label created successfully')


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = LabelNameForm
    model = Label
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels')
    success_message = _('Label changed successfully')


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    success_url = reverse_lazy('labels')
    template_name = "labels/delete.html"
    success_message = _('Label deleted successfully')
    error_message = _('Label used in a task cannot be deleted')

    def form_valid(self, form):
        if not self.object.labels.all():
            self.object.delete()
            messages.success(self.request, self.success_message)
            return redirect(self.success_url)

        else:
            messages.error(self.request, self.error_message)
            return redirect(self.success_url)
