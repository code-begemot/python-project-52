from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import redirect
from task_manager.users.forms import UserForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.db.models import ProtectedError


class IndexView(ListView):
    model = get_user_model()
    template_name = 'users/index.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = messages.get_messages(self.request)
        return context


class UserDeleteView(DeleteView):
    model = get_user_model()
    success_url = reverse_lazy('users')
    template_name = "users/delete.html"
    success_message = _('User data deleted successfully')

    def get(self, request, *args, **kwargs):
        user_id = self.request.user.id
        url_id = kwargs.get('pk')
        if url_id != user_id:
            messages.error(self.request, _('No access rights'))
            return redirect(reverse_lazy('users'))

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(request, self.success_message)
        except ProtectedError:
            messages.error(self.request, _('No access rights'))

        finally:
            return redirect(self.success_url)


class UserUpdateView(SuccessMessageMixin, UpdateView):
    form_class = UserForm
    model = get_user_model()
    template_name = 'users/update.html'
    success_url = reverse_lazy('users')
    success_message = _('User data changed successfully')
    error_message = _('Incorrect data, please try again')

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        user_id = self.request.user.id
        url_id = kwargs.get('pk')
        if url_id != user_id:
            messages.error(self.request, _('No access rights'))
            return redirect(reverse_lazy('users'))

        return super().get(request, *args, **kwargs)


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserForm
    model = get_user_model()
    template_name = 'users/registration.html'
    success_url = reverse_lazy('login')
    success_message = _('User created successfully')
    error_message = _('Incorrect data, please try again')

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)
