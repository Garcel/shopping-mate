from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class ShoppingList(models.Model):
    class Meta:
        db_table = 'shopping_list'
        ordering = ['-id']

    name = models.CharField(_('name'), max_length=30)
    description = models.CharField(_('description'), max_length=150, blank=True, null=True)
    creation_date = models.DateTimeField(_('date created'), auto_now_add=True)
    last_update = models.DateTimeField(_('date last modification'), auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class ShoppingItem(models.Model):
    class Meta:
        db_table = 'shopping_item'
        ordering = ['-id']

    list = models.ForeignKey('ShoppingList', on_delete=models.CASCADE, related_name='items')
    name = models.CharField(_('name'), max_length=30)
    data = models.JSONField(null=True, blank=True)
    description = models.CharField(_('description'), max_length=150, blank=True, null=True)
    creation_date = models.DateTimeField(_('date created'), default=timezone.now)
    last_update = models.DateTimeField(_('date last modification'), default=timezone.now)
    due_date = models.DateTimeField(_('date of expiration'), null=True, blank=True)

    def get_seconds_to_expiration(self):
        """
        Returns the seconds left for the expiration of this item.

        Returns None when due_date is None.
        """
        if self.due_date is None:
            return None

        diff = (self.due_date - timezone.now()).total_seconds()
        return diff if diff >= 0 else 0
