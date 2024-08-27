from django.test import TestCase
from django.contrib.auth import get_user_model

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from django.utils.translation import gettext as _

class BaseTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        user_model.objects.create_user(username='user_creator',
                                       password='ptesttest')
        user_model.objects.create_user(username='user_executor',
                                       password='ptesttest')

        Status.objects.create(name='status_test')
        Status.objects.create(name='status_action')

        Task.objects.create(
            name='task_action',
            description='description_action',
            status=Status.objects.get(name='status_action'),
            creator=user_model.objects.get(username='user_creator'),
            executor=user_model.objects.get(username='user_executor'),
        )

    def test_statuses_view(self):
        response_redirect = self.client.get('/statuses/')
        self.assertRedirects(response_redirect, '/login/?next=/statuses/')

        self.client.login(username="user_creator", password="ptesttest")
        response = self.client.get('/statuses/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        self.assertTemplateUsed(response, 'statuses/index.html')

    def test_status_create_view(self):
        self.client.login(username="user_creator", password="ptesttest")

        status_create_url = '/statuses/create/'
        response = self.client.get(status_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/create.html')

        response_redirect = self.client.post(status_create_url,
                                             {'name': 'status_test1', })

        response = self.client.get('/statuses/')
        content = response.content.decode()
        self.assertIn(_('Status created successfully'), content)
        self.assertRedirects(response_redirect, '/statuses/')

    def test_update_status(self):
        self.client.login(username="user_executor", password="ptesttest")
        status_id = Status.objects.get(name='status_action').id
        response = self.client.get(f'/statuses/{status_id}/update/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        self.assertTemplateUsed(response, 'statuses/update.html')

        response_redirect = self.client.post(f'/statuses/{status_id}/update/',
                                             {"name": "status_unaction", })
        response = self.client.get('/statuses/')
        content = response.content.decode()
        self.assertIn(_('Status changed successfully'), content)
        self.assertIn('status_unaction', content)
        self.assertIn(_('Statuses'), content)
        self.assertRedirects(response_redirect, '/statuses/', 302, 200)

    def test_delete_status(self):
        self.client.login(username="user_creator", password="ptesttest")

        status_id = Status.objects.get(name='status_action').id
        response_redirect = self.client.post(f'/statuses/{status_id}/delete/')
        response = self.client.get('/statuses/')
        content = response.content.decode()
        self.assertIn(_('Status used in a task cannot be deleted'),
                      content)
        self.assertRedirects(response_redirect, '/statuses/', 302, 200)

        task_id = Task.objects.get(name='task_action').id
        response_redirect = self.client.post(f'/tasks/{task_id}/delete/')
        self.assertRedirects(response_redirect, '/tasks/', 302, 200)

        response_redirect = self.client.post(f'/statuses/{status_id}/delete/')
        response = self.client.get('/statuses/')
        content = response.content.decode()
        self.assertIn(_('Status deleted successfully'), content)
        self.assertNotIn('status_action', content)
        self.assertIn(_('Statuses'), content)
        self.assertRedirects(response_redirect, '/statuses/', 302, 200)
