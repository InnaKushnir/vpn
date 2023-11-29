from django.core.validators import URLValidator
from django.db import models
from django.contrib.auth import get_user_model


class Site(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url = models.URLField(validators=[URLValidator()])


class SiteTransition(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    from_site = models.CharField(max_length=255)
    to_site = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_site} -> {self.to_site}"
