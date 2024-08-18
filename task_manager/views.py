from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

class IndexView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = messages.get_messages(self.request)
        return context