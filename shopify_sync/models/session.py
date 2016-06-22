from __future__ import unicode_literals

from django.db import models


class Session(models.Model):
    token = models.CharField(max_length=255)
    site = models.CharField(max_length=511)

    class Meta:
        app_label = 'shopify_sync'

    def __str__(self):
        return "Session: %s" % self.site
