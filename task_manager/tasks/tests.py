from django.test import TestCase
from django.contrib.auth import get_user_model

from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
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
        Label.objects.create(name='label_test')
        Label.objects.create(name='label_action')

        task_action = Task.objects.create(
            name='task_action',
            description='description_action',
            status=Status.objects.get(name='status_action'),
            creator=user_model.objects.get(username='user_creator'),
            executor=user_model.objects.get(username='user_executor'),
        )
        task_action.save()
        task_action.labels.add(Label.objects.get(name='label_action'))

    def test_tasks_view(self):
        response_redirect = self.client.get('/tasks/')
        self.assertRedirects(response_redirect, '/login/?next=/tasks/')

        self.client.login(username="user_creator", password="ptesttest")
        response = self.client.get('/tasks/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        self.assertTemplateUsed(response, 'tasks/index.html')

    def test_tasks_create_view(self):
        self.client.login(username="user_creator", password="ptesttest")

        user_model = get_user_model()
        task_create_url = '/tasks/create/'
        response = self.client.get(task_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/create.html')

        status_id = Status.objects.get(name='status_test').id
        creator_id = user_model.objects.get(username='user_creator').id
        executor_id = user_model.objects.get(username='user_executor').id
        label_id = Label.objects.get(name='label_test').id

        response_redirect = self.client.post(task_create_url,
                                             {'name': 'task_test1',
                                              'description': 'descr_test1',
                                              'status': status_id,
                                              'creator': creator_id,
                                              'executor': executor_id,
                                              'labels': label_id, })

        response = self.client.get('/tasks/')
        content = response.content.decode()
        self.assertIn(_('Task created successfully'), content)
        self.assertRedirects(response_redirect, '/tasks/')

    def test_update_task(self):
        self.client.login(username="user_executor", password="ptesttest")
        task_id = Task.objects.get(name='task_action').id
        response = self.client.get(f'/tasks/{task_id}/update/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        self.assertTemplateUsed(response, 'tasks/update.html')

        response_redirect = self.client.post(
            f'/tasks/{task_id}/update/',
            {"name": "task_unaction",
             "description": "finish",
             "status": Status.objects.get(name='status_test').id, }
        )
        response = self.client.get('/tasks/')
        content = response.content.decode()
        self.assertIn(_('Task changed successfully'), content)
        self.assertIn('task_unaction', content)
        self.assertIn(_('Tasks'), content)
        self.assertRedirects(response_redirect, '/tasks/', 302, 200)

    def test_delete_task(self):
        self.client.login(username="user_executor", password="ptesttest")
        task_id = Task.objects.get(name='task_action').id
        response_redirect = self.client.get(f'/tasks/{task_id}/delete/')
        response = self.client.get('/tasks/')
        content = response.content.decode()
        self.assertIn(_('Only creator can delete the task'), content)
        self.assertRedirects(response_redirect, '/tasks/', 302, 200)

        self.client.logout()

        self.client.login(username="user_creator", password="ptesttest")

        response = self.client.get(f'/tasks/{task_id}/delete/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn('task_action', content)

        response_redirect = self.client.post(f'/tasks/{task_id}/delete/')
        response = self.client.get('/tasks/')
        content = response.content.decode()
        self.assertIn(_('Task deleted successfully'), content)
        self.assertNotIn('task_action', content)
        self.assertIn(_('Tasks'), content)
        self.assertRedirects(response_redirect, '/tasks/', 302, 200)
