from django.db import models
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    """Tasks."""
    name = models.CharField(_('Name'), max_length=100, unique=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=_('Status')
    )
    creator = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        verbose_name=_('Creator'),
        related_name='creator_id'
    )
    executor = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        verbose_name=_('Executor'),
        related_name='executor_id',
        blank=True,
        null=True
    )
    labels = models.ManyToManyField(Label, verbose_name=_('Labels'), blank=True, related_name='labels', null=True)
    created_at = models.DateTimeField(_('Date created'), auto_now_add=True)

    def __str__(self):
        return self.name
