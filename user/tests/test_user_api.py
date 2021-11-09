from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):

    """Public API tests for user"""
    def setUp(self):
        self.client = APIClient()
    
    def test_create_user_sucess(self):
        """Test creating user through an API is successful"""
        payload = {'email':'test@gmail.com', 'password':'testpass123'}

        res = self.client.post(CREATE_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        user = get_user_model().objects.get(**res.data)

        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
    
    def test_uesr_already_exists(self):
        """Test creating already exisitng user fails"""

        paylaod = {'email':'test@gmail.com', 'password':'testpass123'}
        create_user(**paylaod)

        res = self.client.post(CREATE_URL, paylaod)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_is_too_short(self):
        """Test creating user with too short password fails"""

        payload = {'email': 'test@gmail.com', 'password':'pw'}
        
        res = self.client.post(CREATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    