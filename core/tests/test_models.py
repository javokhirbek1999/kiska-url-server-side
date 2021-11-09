from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    """Tests for models"""

    def test_create_user_with_email_success(self):
        """Test creating a user with email successfully"""
        
        payload = {'email': 'test@gmail.com', 'user_name':'testusername123', 'password':'testpass123'}

        user = get_user_model().objects.create_user(
            email=payload['email'],
            user_name=payload['user_name'],
            password=payload['password']
        )

        self.assertEqual(user.email, payload['email'])
        self.assertEqual(user.user_name, payload['user_name'])
        self.assertTrue(user.check_password(payload['password']))
    
    def test_create_user_email_is_normalized(self):
        """Test email is normalized when creating a user"""

        user = get_user_model().objects.create_user(
            email='test@GmAIl.com',
            user_name='testusername',
            password='testpass123'
        )

        self.assertEqual(user.email, 'test@gmail.com')
    
    def test_create_superuser_sucess(self):
        """Test creating an admin successfully"""

        user = get_user_model().objects.create_superuser(
            email='test@gmail.com',
            user_name='testuser123',
            password='testpass123'
        )

        self.assertTrue(user.is_superuser)