from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from ..models.url import OriginalURL, ShortURL, AllOriginalURL, AllShortURL


@receiver(post_save, sender=ShortURL)
def create_all_short_url(sender, instance, created, **kwargs):
    """
            Check if recently created short url already exists,
            if it does not exist, then add it into All Craeted Short URLs
    """

    if created:
        try:
            AllShortURL.objects.get(url__shortURL=instance.shortURL)
        except ObjectDoesNotExist:
            AllShortURL.objects.create(url=instance, visited=0)

