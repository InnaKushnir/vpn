from django.contrib.auth import get_user_model
from django.core.validators import URLValidator
from django.db import models
from easyaudit.models import CRUDEvent


class Site(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url = models.URLField(validators=[URLValidator()])


class SiteTransition(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    from_site = models.CharField(max_length=255)
    to_site = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    downloaded_content_size = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.from_site} -> {self.to_site}"

