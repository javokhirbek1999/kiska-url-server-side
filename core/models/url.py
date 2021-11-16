from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

class OriginalURL(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    url = models.URLField(max_length=2048)
    date_created = models.DateTimeField(auto_now_add=True)

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
    original_url = models.ForeignKey(OriginalURL, on_delete=models.DO_NOTHING, null=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False, default=0)
    short_url = models.URLField(max_length=2048)
    url_hash = models.CharField(max_length=200, default="")

    @property
    def get_original_url(self):
        return self.original_url.url
    
    @property
    def get_username(self):
        return self.user.user_name
    
    @property
    def date_created(self):
        return self.original_url.date_created
    
    def to_json(self):
        return {
            'id': self.id,
            'original_url': self.original_url.url,
            'short_url': self.short_url
        }


class AllOriginalURL(models.Model):
    url = models.URLField(max_length=2048)
    shortened = models.IntegerField(default=0, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']
    
    def __str__(self) -> str:
        return f"URL: {self.url} || Shortended: {self.shortened} || Created: {self.date_created}"

    def to_json(self):
        return {
            'id': self.id,
            'url': self.url,
            'shortened': self.shortened,
            'date_created': self.date_created
        }

class AllShortURL(models.Model):
    url = models.URLField(max_length=2048)
    visited = models.IntegerField(default=0, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']
    
    def __str__(self) -> str:
        return f"URL: {self.url} || Visited: {self.visited} || Created: {self.date_created}"
    
    def to_json(self):
        return {
            'id': self.id,
            'url': self.url,
            'visited': self.visited,
            'date_created': self.date_created
        }