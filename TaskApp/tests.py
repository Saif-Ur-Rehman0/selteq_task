from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from TaskApp.models import Task
from rest_framework_simplejwt.tokens import RefreshToken

def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class TaskAppTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = get_token_for_user(self.user)['access']
        
        self.task = Task.objects.create(user=self.user, title="Test Task", duration=10)
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_task(self):
        url = reverse('create_task')
        data = {
            'title': 'New Task',
            'duration': 30
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['title'], 'New Task')

    def test_get_all_tasks(self):
        url = reverse('get_all_tasks')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_retrieve_task(self):
        url = reverse('retrieve_task', args=[self.task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Use response.json() to access the response data
        response_data = response.json()
        self.assertEqual(response_data['title'], 'Test Task')

    def test_update_task_title(self):
        url = reverse('update_task_title', args=[self.task.id])
        data = {'title': 'Updated Task'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')

    def test_delete_task(self):
        url = reverse('delete_task', args=[self.task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=self.task.id)

    def test_trigger_print_tasks(self):
        url = reverse('trigger_tasks')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
