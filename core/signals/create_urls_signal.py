from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from ..models.url import OriginalURL, ShortURL, AllOriginalURL, AllShortURL


@receiver(post_save, sender=OriginalURL)
def create_original_url(sender, instance, created, **kwargs):
    if created:
        original_url = None
        try:
            original_url = AllOriginalURL.objects.get(url=instance.url)
            original_url.shortened += 1
            original_url.save()
        except ObjectDoesNotExist:
            AllOriginalURL.objects.create(url=instance.url, shortened=1)


