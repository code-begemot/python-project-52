from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import redirect
from task_manager.users.forms import UserForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusNameForm
from django.db.models import ProtectedError



class IndexView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = messages.get_messages(self.request)
        return context


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = StatusNameForm
    model = Status
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status created successfully')


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = StatusNameForm
    model = Status
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status changed successfully')


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    success_url = reverse_lazy('statuses')
    template_name = "statuses/delete.html"
    success_message = _('Status deleted successfully')
    error_message = _('Status used in a task cannot be deleted')

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(request, self.success_message)
        except ProtectedError:
            messages.error(request, self.error_message)

        finally:
            return redirect(self.success_url)