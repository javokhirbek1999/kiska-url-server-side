from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

class OriginalURL(models.Model):

    """Original URL Model"""

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    url = models.URLField(max_length=2048)
    date_created = models.DateTimeField(auto_now_add=True)
    shortened = models.IntegerField(default=1, editable=False)

    @property
    def get_user_username(self):
        return self.user.user_name
    
    class Meta:
        ordering = ['-date_created']
    
    def __str__(self) -> str:
        return f"\nURL: {self.url}\nUSER: {self.user.user_name}\nDATE_CREATED: {self.date_created}\n\n"

    def to_json(self):
        return {
            'id': self.id,
            'user': self.user.user_name,
            'date_created': self.date_created
        }



class ShortURL(models.Model):

    """Short URL model"""
    originalURL = models.ForeignKey(OriginalURL, on_delete=models.DO_NOTHING, null=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=0)
    shortURL = models.URLField(max_length=2048)
    urlHash = models.CharField(max_length=200, default="")
    visited = models.IntegerField(default=0)

    @property
    def get_original_url(self):
        return self.originalURL.url
    
    @property
    def get_username(self):
        return self.user.user_name
    
    @property
    def date_created(self):
        return self.originalURL.date_created
    
    def to_json(self):
        return {
            'id': self.id,
            'original_url': self.originalURL.url,
            'short_url': self.shortURL
        }
