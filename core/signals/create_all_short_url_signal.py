from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from ..models.url import OriginalURL, ShortURL, AllOriginalURL, AllShortURL


@receiver(post_save, sender=ShortURL)
def create_all_short_url(sender, instance, created, **kwargs):
    if created:
        try:
            AllShortURL.objects.get(url=instance.short_url)
        except ObjectDoesNotExist:
            AllShortURL.objects.create(url=instance.short_url, visited=0)

