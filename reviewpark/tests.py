from django.test import TestCase
from userpark.models import User as myUser
from django.urls import reverse
from datetime import date
from logging import getLogger

logger = getLogger('response_logger')

# Create your tests here.


class FeedbackPermissionTests(TestCase):

    def setUp(self):
        # Setup run before every test method.
        user = myUser.objects.create(username='paola98', first_name='paola', last_name='verdi', gender='F',
                                     email='pv@gmail.com', is_staff_member=False, is_staff=False,
                                     is_superuser=False, birth_date='1998-02-13')
        user.set_password('Asdfghjkl!!')
        user.save()
        self.client.force_login(myUser.objects.get(username='paola98'))
        super().setUp()

    def test_purchase_required_mixin_feedback_access(self):
        # Test code
        response = self.client.get(reverse('reviewpark:leave-feedback'))
        self.assertEqual(response.status_code, 403)  # Permission denied, no purchase exists
        logger.warning(response.content)

    def test_purchase_made_feedback_access(self):
        self.client.post(reverse('waterpark:customer-buy-tiket'), {'validity_day': date.today()})
        response = self.client.get(reverse('reviewpark:leave-feedback'))
        self.assertEqual(response.status_code, 200)  # Permission allowed, purchase made
        logger.warning(response.content)
