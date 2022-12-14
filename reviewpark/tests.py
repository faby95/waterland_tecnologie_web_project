from django.test import TestCase
from .models import Feedback
from userpark.models import User as myUser
from waterpark.models import Tiket as Ticket
from django.urls import reverse
from datetime import date
from logging import getLogger

logger = getLogger('response_logger')

# Create your tests here.


class TestFeedback(TestCase):

    def setUp(self):
        self.customer = myUser.objects.create(username='paola98', first_name='paola',
                                                                     last_name='verdi', gender='F',
                                                                     email='pv@gmail.com', is_staff_member=False,
                                                                     is_staff=False, is_superuser=False,
                                                                     birth_date='1998-02-13')
        self.f = Feedback.objects.create(stars=5, customer=self.customer, feedback_text='Feedback for test')

    def testSetupCreation(self):
        self.assertIsNotNone(self.customer, 'customer is null')
        self.assertIsNotNone(self.f, 'f is null')
        self.assertIsNotNone(self.f.customer, 'customer foreign key is null')

    # Consistenza architetturale
    def testCustomerObj(self):
        self.assertTrue(isinstance(self.customer, myUser), 'Customer is not a User')

    def testFeedbackObj(self):
        self.assertTrue(isinstance(self.f, Feedback), 'f is not a Feedback')

    def testCustomerForeignkeyObj(self):
        self.assertTrue(isinstance(self.f.customer, myUser), 'f.customer foreign key is not a User')

    def testDefaultAttribute(self):
        self.assertEqual(self.f.feedback_date.date(), date.today(), 'Wrong feedback date')

    def testStarsAttribute(self):
        self.assertTrue(isinstance(self.f.stars, int), 'Stars is not a number (int)')
        self.assertEqual(self.f.stars, 5, 'Wrong value of stars attribute')

    def testFeedbackTextAttribute(self):
        self.assertTrue(isinstance(self.f.feedback_text, str), 'Feedback_text is not a text field')
        self.assertEqual(self.f.feedback_text, 'Feedback for test', 'Wrong feedback text value')

    # Coerenza funzionale, metodi che hanno subito un override, metodi utilizzati dal modello
    def testMethods(self):
        self.assertTrue(callable(self.f.__str__), 'f haven\'t got __str__ method')
        # callable get_username from foreign key
        self.assertTrue(callable(self.f.customer.get_username))

    # Coerenza funzionale: risultati attesi dei metodi
    def testGetCustomerUsername(self):
        self.assertIsNotNone(self.f.customer, 'A customer must be associated to the feedback to get the username')
        self.assertEqual(self.f.customer.get_username(), 'paola98', 'Got wrong username')

    def test__str__method(self):
        self.assertEqual(self.f.__str__(), f'Feedback - n°{self.f.id}', "Wrong self rappresentation")

    def tearDown(self):
        self.f.delete()
        self.customer.delete()


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
        logger.warning('Purchase number = {}'.format(Ticket.objects.all().count()))
        logger.warning('Status code = {}'.format(response.status_code))
        logger.warning('Content = {}'.format(response.content))

    def test_purchase_made_feedback_access(self):
        self.client.post(reverse('waterpark:customer-buy-tiket'), {'validity_day': date.today()})
        response = self.client.get(reverse('reviewpark:leave-feedback'))
        self.assertEqual(response.status_code, 200)  # Permission allowed, purchase made
        logger.warning('Purchase number = {}'.format(Ticket.objects.all().count()))
        logger.warning('Status code = {}'.format(response.status_code))
        logger.warning('Content = {}'.format(response.content))

    def tearDown(self):
        myUser.objects.get(username='paola98').delete()
