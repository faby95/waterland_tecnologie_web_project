from django.test import TestCase
from .models import Tiket as Ticket, validity_delta
from userpark.models import User as myUser
from django.urls import reverse
from datetime import date, timedelta
from logging import getLogger

logger = getLogger('response_logger')

# Create your tests here.


class TestTicket(TestCase):

    def setUp(self):
        self.t = Ticket.objects.create(customer=myUser.objects.create(username='paola98', first_name='paola',
                                                                      last_name='verdi', gender='F',
                                                                      email='pv@gmail.com', is_staff_member=False,
                                                                      is_staff=False, is_superuser=False,
                                                                      birth_date='1998-02-13'),
                                       validity_day=date.today()+timedelta(days=20))
        return super().setUp()

    def testSetUpCreation(self):
        self.assertIsNotNone(self.t, 't do not exists')
        self.assertIsNotNone(self.t.customer, 'No customer associated')

    # Consistenza architetturale
    def testTicketObj(self):
        self.assertTrue(isinstance(self.t, Ticket), 't is not a Ticket')

    def testCustomerForeignkeyObj(self):
        self.assertTrue(isinstance(self.t.customer, myUser), 'Customer is not a user')

    def testDefaultAttribute(self):
        self.assertEqual(self.t.cost, 15, 'Wrong default cost attribute')
        self.assertIsNotNone(self.t.date_of_purchase, 'This field cannot be null')
        self.assertEqual(self.t.date_of_purchase.date(), date.today(), 'Wrong purchase date')

    def testValidityDay(self):
        self.assertIsNotNone(self.t.validity_day, 'Validity day cannot be null')
        self.assertEqual(self.t.validity_day, date.today()+timedelta(days=20), 'Wrong validity day')

    # Coerenza funzionale, metodi che hanno subito un override, metodi utilizzati dal modello
    def testMethods(self):
        self.assertTrue(callable(self.t.__str__), 't haven\'t got __str__ method')
        self.assertTrue(callable(self.t.save), 't haven\'t got save method')
        # callable get_username from foreign key
        self.assertTrue(callable(self.t.customer.get_username))

    # Coerenza funzionale: risultati attesi dei metodi
    def testGetCustomerUsername(self):
        self.assertIsNotNone(self.t.customer, 'A customer must be associated to the ticket to get the username')
        self.assertEqual(self.t.customer.get_username(), 'paola98', 'Got wrong username')

    def test__str__method(self):
        self.assertEqual(self.t.__str__(), f'{self.t.customer.get_username()} - Ticket:{self.t.tiket_slug}',
                         "Wrong self rappresentation")

    def testSaveMethod(self):
        self.assertIsNotNone(self.t.tiket_slug, "Ticket slug do not created, it cannot be null")

    def tearDown(self):
        self.t.delete()
        myUser.objects.get(username='paola98').delete()
        return super().tearDown()
    # validity_date attribute range tested in view, customer use the view to interact with database
    # view use validation logic before to save in database


class CustomerTicketBuyViewTests(TestCase):

    def setUp(self):
        # Setup run before every test method.
        user = myUser.objects.create(username='paola98', first_name='paola', last_name='verdi', gender='F',
                                     email='pv@gmail.com', is_staff_member=False, is_staff=False,
                                     is_superuser=False, birth_date='1998-02-13')
        user.set_password('Asdfghjkl!!')
        user.save()
        self.client.force_login(myUser.objects.get(username='paola98'))
        return super().setUp()

    def test_customer_ticket_buy_access_mixin(self):
        # Test code
        response = self.client.get(reverse('waterpark:customer-buy-tiket'))
        self.assertEqual(response.status_code, 200, 'customer cannot buy a ticket')  # 403 FORBIDDEN status code for not customer user
        logger.info(response.status_code)
        logger.info(response.content)  # Print with red color the content

    def test_customer_buy_ticket_legit_period(self):
        # Test code
        self.client.post(reverse('waterpark:customer-buy-tiket'), {'validity_day': date.today()})
        self.client.post(reverse('waterpark:customer-buy-tiket'), {'validity_day': date.today()+timedelta(days=55)})
        tiket = Ticket.objects.all()
        self.assertEqual(tiket.count(), 2, 'Tickets expected error')

    def test_customer_buy_tiket_validity_day_before_today(self):
        # Test code
        self.client.post(reverse('waterpark:customer-buy-tiket'), {'validity_day': date.today()-timedelta(days=1)})
        tiket = Ticket.objects.all()
        self.assertEqual(tiket.count(), 0, 'No expected tickets')  # No tickets created, out of validation range

    def test_customer_buy_tiket_validity_day_after_a_year(self):
        # Test code
        self.client.post(reverse('waterpark:customer-buy-tiket'), {'validity_day': date.today()+timedelta(days=366)})
        tiket = Ticket.objects.all()
        self.assertEqual(tiket.count(), 0, 'No expected tickets')  # No tickets created, out of validation range

    def test_customer_buy_tiket_check_integrity(self):
        # Test code
        self.client.post(reverse('waterpark:customer-buy-tiket'), {'validity_day': date.today()})
        tiket = Ticket.objects.all()
        self.assertIsNotNone(tiket[0].tiket_slug, 'Expected ticket id')  # Ticket id created, created in override method save
        self.assertIsNotNone(tiket[0].customer, 'Expected assigned customer')    # Foreign key not null, ticket linked to the user 'paola98'
        self.assertEqual(tiket[0].customer.get_username(), 'paola98', 'Wrong tiket\'s owner')

    def test_customer_tiket_check_integrity_after_deleted_customer(self):
        # Test code
        self.client.post(reverse('waterpark:customer-buy-tiket'), {'validity_day': date.today()})
        tiket = Ticket.objects.all()
        self.assertEqual(tiket.count(), 1, 'Expected 1 ticket')  # Ticket created
        user = myUser.objects.filter(username='paola98')
        user.delete()
        self.assertEqual(len(myUser.objects.all()), 0, 'Expected no user')  # User deleted
        self.assertIsNone(tiket[0].customer, 'Expected null customer field')  # Ticket still saved with no customer


class CustomerTicketListViewTests(TestCase):

    def setUp(self):
        # Setup run before every test method.
        user = myUser.objects.create(username='paola98', first_name='paola', last_name='verdi', gender='F',
                                     email='pv@gmail.com', is_staff_member=False, is_staff=False,
                                     is_superuser=False, birth_date='1998-02-13')
        user.set_password('Asdfghjkl!!')
        user.save()
        self.client.force_login(myUser.objects.get(username='paola98'))
        return super().setUp()

    def test_customer_tiket_personal_list(self):
        # Create 3 tikets
        self.client.post(reverse('waterpark:customer-buy-tiket'), {'validity_day': date.today()})
        self.client.post(reverse('waterpark:customer-buy-tiket'), {'validity_day': date.today() + timedelta(days=1)})
        self.client.post(reverse('waterpark:customer-buy-tiket'), {'validity_day': date.today() + timedelta(days=2)})
        self.assertEqual(Ticket.objects.filter(customer__username='paola98').count(), 3, 'Expected 3 tikets')  # 3 tikets created, advanced data (date.today() + timedelta(days=2))
        # Go to the personal tiket list
        response = self.client.get(reverse('waterpark:customer-tiket-list'))
        self.assertEqual(response.status_code, 200, 'Expected 200 OK')
        logger.info(response.status_code)
        logger.info(response.content)
        first_tiket_result_date = response.context['tiket_list'][0]['validity_day']
        self.assertEqual(first_tiket_result_date, date.today() + timedelta(days=2), 'Expected most recent date')  # DESC ORDER paginated by 1
        customer = myUser.objects.filter(username='paola98').values('id')[0]['id']
        self.assertEqual(response.context['tiket_list'][0]['customer_id'], customer, 'Wrong owner')

    def tearDown(self):
        myUser.objects.get(username='paola98').delete()
        return super().tearDown()


class CustomerRequiredMixinTests(TestCase):

    def setUp(self):
        # Setup run before every test method.
        user = myUser.objects.create(username='paola98', first_name='paola', last_name='verdi', gender='F',
                                     email='pv@gmail.com', is_staff_member=True, is_staff=False,
                                     is_superuser=False, birth_date='1998-02-13')
        user.set_password('Asdfghjkl!!')
        user.save()  # User staff created
        self.client.force_login(myUser.objects.get(username='paola98'))
        return super().setUp()

    def test_customer_required_mixin(self):
        # For example go to the personal tiket list, a page permited just to the customers
        response = self.client.get(reverse('waterpark:customer-tiket-list'))
        self.assertEqual(response.status_code, 403, 'Expected 403 status code')  # Permission denied
        logger.info(response.status_code)
        logger.info(response.content)

    def test_staff_required_mixin(self):
        response = self.client.get(reverse('waterpark:staff-manage-tiket-main'))
        self.assertEqual(response.status_code, 200, 'Expected 200 OK')  # Permission allowed
        logger.info(response.status_code)
        logger.info(response.content)

    def tearDown(self):
        myUser.objects.get(username='paola98').delete()
        return super().tearDown()


class StaffRequiredMixinTests(TestCase):

    def setUp(self):
        # Setup run before every test method.
        user = myUser.objects.create(username='paola98', first_name='paola', last_name='verdi', gender='F',
                                     email='pv@gmail.com', is_staff_member=False, is_staff=False,
                                     is_superuser=False, birth_date='1998-02-13')
        user.set_password('Asdfghjkl!!')
        user.save()  # User staff created
        self.client.force_login(myUser.objects.get(username='paola98'))
        return super().setUp()

    def test_customer_required_mixin(self):
        # For example go to the personal tiket list, a page permited just to the customers
        response = self.client.get(reverse('waterpark:customer-tiket-list'))
        self.assertEqual(response.status_code, 200, 'Expected 200 OK')  # Permission allowed
        logger.info(response.status_code)
        logger.info(response.content)

    def test_staff_required_mixin(self):
        response = self.client.get(reverse('waterpark:staff-manage-tiket-main'))
        self.assertEqual(response.status_code, 403, 'Expected 403 status code')  # Permission denied
        logger.info(response.status_code)
        logger.info(response.content)

    def tearDown(self):
        myUser.objects.get(username='paola98').delete()
        return super().tearDown()


class DuplicateTicketTests(TestCase):

    def setUp(self):
        # Setup run before every test method.
        user = myUser.objects.create(username='paola98', first_name='paola', last_name='verdi', gender='F',
                                     email='pv@gmail.com', is_staff_member=False, is_staff=False,
                                     is_superuser=False, birth_date='1998-02-13')
        user.set_password('Asdfghjkl!!')
        user.save()
        self.client.force_login(myUser.objects.get(username='paola98'))
        return super().setUp()

    def test_duplicate_tikets(self):
        self.client.post(reverse('waterpark:customer-buy-tiket'), {'validity_day': date.today()})
        self.client.post(reverse('waterpark:customer-buy-tiket'), {'validity_day': date.today()})
        tiket = Ticket.objects.all()
        self.assertEqual(tiket.count(), 1, "Duplicated ticket at the same day")

    def tearDown(self):
        myUser.objects.get(username='paola98').delete()
        return super().tearDown()


class ValidityDeltaFunctionTests(TestCase):

    def test_validity_delta_seasonpass(self):
        today = date.today()
        end_validity_first_january_next_year = today + timedelta(days=validity_delta())
        logger.info('Today date: {}'.format(today))
        logger.info('Expected: NEXT YEAR-01-01')
        logger.info('Target date after function: {}'.format(end_validity_first_january_next_year))
        self.assertEqual(end_validity_first_january_next_year, date(today.year + 1, 1, 1),
                         'Date was not NEXT YEAR-01-01')
