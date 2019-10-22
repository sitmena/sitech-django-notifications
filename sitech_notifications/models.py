from django.db import models
from datetime import datetime
from jsonfield import JSONField
from django.utils.timezone import get_current_timezone


class DatabaseNotification(models.Model):
    type = models.CharField(verbose_name='Type', max_length=255)
    notifiable_id = models.PositiveIntegerField('Notifiable Id')
    notifiable_type = models.CharField(verbose_name='Notifiable Type', max_length=255)
    data = JSONField(verbose_name='Data')
    read_at = models.DateTimeField(null=True, blank=True, verbose_name='Read At')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='Updated At')

    # Mark the notification as read.
    def mark_as_read(self):
        if self.unread():
            self.read_at = datetime.now(tz=get_current_timezone())
            self.save()

    # Mark the notification as unread.
    def mark_as_unread(self):
        if self.read():
            self.read_at = None
            self.save()

    # Determine if a notification has been read.
    def read(self):
        return bool(self.read_at)

    # Determine if a notification has not been read.
    def unread(self):
        return bool(not self.read_at)
