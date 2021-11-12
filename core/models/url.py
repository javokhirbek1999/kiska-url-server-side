from django.db import models
from django.contrib.auth import get_user_model


class OriginalURL(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    url = models.URLField()
    date_created = models.DateTimeField(auto_now_add=True)
    shorten_count = models.IntegerField(default=0)


class ShortURL(models.Model):
    original_url = models.ForeignKey(OriginalURL, on_delete=models.DO_NOTHING)
    short_url = models.URLField()
    visit_count = models.IntegerField(default=0)    
