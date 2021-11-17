from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from ..models.url import OriginalURL, ShortURL
from ..utils.urls import utils



@receiver(post_save, sender=OriginalURL)
def create_short_url(sender, instance, created,**kwargs):
    
    """Create short url once original url is posted"""
    
    if created:
        try:
            ShortURL.objects.get(originalURL__url=instance.url, user=instance.user)
        except ObjectDoesNotExist:
            hashed_url = utils.hash_the_url(instance.user, instance.url)
            ShortURL.objects.create(originalURL=instance, user=instance.user, shortURL=settings.DEFAULT_DOMAIN+hashed_url, urlHash=hashed_url)
