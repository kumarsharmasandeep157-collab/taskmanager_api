from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Task

class AuthTestCase(APITestCase):
    def test_register_user(self):
        """Test user registration returns 201 and token."""
        data = {'username': 'newuser', 'password': 'Pass@1234', 'email': 'new@test.com'}
        response = self.client.post('/api/auth/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], 'newuser')

    def test_login_valid(self):
        """Test login with correct credentials returns token."""
        user = User.objects.create_user('loginuser', password='Pass@1234')
        data = {'username': 'loginuser', 'password': 'Pass@1234'}
        response = self.client.post('/api/auth/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_invalid(self):
        """Test login with wrong password returns 401."""
        User.objects.create_user('user2', password='correct')
        data = {'username': 'user2', 'password': 'wrong'}
        response = self.client.post('/api/auth/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TaskTestCase(APITestCase):
    def setUp(self):
        """Run before every test: create user and authenticate."""
        self.user = User.objects.create_user('taskuser', password='Pass@1234')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_task(self):
        """Test creating a simple task manually."""
        data = {'title': 'Test Task', 'priority': 'high'}
        response = self.client.post('/api/tasks/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().owner, self.user)

    def test_list_tasks(self):
        """Test viewing created tasks."""
        Task.objects.create(title='Task A', owner=self.user)
        Task.objects.create(title='Task B', owner=self.user)
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_unauthenticated_access(self):
        """Without token, should get 401."""
        client = APIClient() # Fresh client, no credentials
        response = client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_cannot_see_other_users_tasks(self):
        """Tasks should only be visible to their owner."""
        other_user = User.objects.create_user('other', password='Pass@1234')
        Task.objects.create(title='Other Task', owner=other_user)
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.data['count'], 0) # Our user has 0 tasks
