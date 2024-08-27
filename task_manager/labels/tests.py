from django.test import TestCase
from django.contrib.auth import get_user_model

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
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

        Status.objects.create(name='status_action')

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

    def test_labels_view(self):
        response_redirect = self.client.get('/labels/')
        self.assertRedirects(response_redirect, '/login/?next=/labels/')

        self.client.login(username="user_creator", password="ptesttest")
        response = self.client.get('/labels/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        self.assertTemplateUsed(response, 'labels/index.html')

    def test_label_create_view(self):
        self.client.login(username="user_creator", password="ptesttest")

        label_create_url = '/labels/create/'
        response = self.client.get(label_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/create.html')

        response_redirect = self.client.post(label_create_url,
                                             {'name': 'label_test1', })

        response = self.client.get('/labels/')
        content = response.content.decode()
        self.assertIn(_("Label created successfully"), content)
        self.assertRedirects(response_redirect, '/labels/')

    def test_update_label(self):
        self.client.login(username="user_executor", password="ptesttest")
        label_id = Label.objects.get(name='label_action').id
        response = self.client.get(f'/labels/{label_id}/update/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        self.assertTemplateUsed(response, 'labels/update.html')

        response_redirect = self.client.post(f'/labels/{label_id}/update/',
                                             {"name": "label_unaction", })
        response = self.client.get('/labels/')
        content = response.content.decode()
        self.assertIn(_("Label changed successfully"), content)
        self.assertIn('label_unaction', content)
        self.assertIn(_('Labels'), content)
        self.assertRedirects(response_redirect, '/labels/', 302, 200)

    def test_delete_label(self):
        self.client.login(username="user_creator", password="ptesttest")

        label_id = Label.objects.get(name='label_action').id
        response_redirect = self.client.post(f'/labels/{label_id}/delete/')
        response = self.client.get('/labels/')
        content = response.content.decode()
        self.assertIn(_("Label used in a task cannot be deleted"),
                      content)
        self.assertRedirects(response_redirect, '/labels/', 302, 200)

        task_id = Task.objects.get(name='task_action').id
        response_redirect = self.client.post(f'/tasks/{task_id}/delete/')
        self.assertRedirects(response_redirect, '/tasks/', 302, 200)

        response_redirect = self.client.post(f'/labels/{label_id}/delete/')
        response = self.client.get('/labels/')
        content = response.content.decode()
        self.assertIn(_("Label deleted successfully"), content)
        self.assertNotIn('task_action', content)
        self.assertIn(_("Labels"), content)
        self.assertRedirects(response_redirect, '/labels/', 302, 200)