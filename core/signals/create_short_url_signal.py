from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from ..models.url import OriginalURL, ShortURL, AllShortURL
from ..utils.urls import utils



@receiver(post_save, sender=OriginalURL)
def create_short_url(sender, instance, created,**kwargs):
    if created:
        try:
            ShortURL.objects.get(original_url=instance, user=instance.user)
        except ObjectDoesNotExist:
            hashed_url = utils.hash_the_url(instance.user, instance.url)
            ShortURL.objects.create(original_url=instance, user=instance.user, short_url=settings.DEFAULT_DOMAIN+hashed_url, url_hash=hashed_url)
