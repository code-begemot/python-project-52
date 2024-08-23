from django.db import models
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    """Statuses for Task."""
    name = models.CharField(_('Name'), max_length=100, null=False, unique=True)
    created_at = models.DateTimeField(_('Date created'), auto_now_add=True)

    def __str__(self):
        return self.name
