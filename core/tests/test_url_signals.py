from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import url


class UrlTestCase(TestCase):

    """Tests signals for URL model"""

    def test_url_created_in_all_urls_in_post_save(self):
        
        """Test that posting original url creats url instance in AllUrls instance"""
        user = get_user_model().objects.create_user(
            email="test@gmail.com",
            user_name="testuser123",
            password="testpass123"
        )

        payload = {'user':user, 'url':'https://youtube.com/djsidjsidjsidjsid'}

        url.OriginalURL.objects.create(**payload)

        
        self.assertEqual(payload['url'], url.AllOriginalURL.objects.get(url=payload['url']).url)

    def test_url_created_in_all_urls_in_post_save_not_duplicated(self):
        
        """Test that same urls are not duplicated in AllURLs, instead increasing counts"""
        user = get_user_model().objects.create_user(
            email='test@gmail.com',
            user_name='testuser123',
            password='testpass123'
        ) 

        payload = {'user': user, 'url': 'https://medium.com/dsudsdhuds/3232ffdfd'}

        url.OriginalURL.objects.create(**payload)
        url.OriginalURL.objects.create(**payload)

        self.assertEqual(url.AllOriginalURL.objects.filter(url=payload['url']).count(),1)
        self.assertEqual(url.AllOriginalURL.objects.get(url=payload['url']).shortened, 2)
