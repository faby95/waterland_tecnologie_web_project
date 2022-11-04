from django.test import TestCase
from .models import Tiket, validity_delta
from userpark.models import User as myUser
from django.urls import reverse
from datetime import date, timedelta
from logging import getLogger

logger = getLogger('response_logger')

# Create your tests here.


class CustomerTiketBuyViewTests(TestCase):

    def setUp(self):
        # Setup run before every test method.
        user = myUser.objects.create(username='paola98', first_name='paola', last_name='verdi', gender='F',
                                     email='pv@gmail.com', is_staff_member=False, is_staff=False,
                                     is_superuser=False, birth_date='1998-02-13')
        user.set_password('Asdfghjkl!!')
        user.save()
        self.client.force_login(myUser.objects.get(username='paola98'))
        super().setUp()

    def test_customer_tiket_buy_access_mixin(self):
        # Test code
        response = self.client.get(reverse('waterpark:customer-buy-tiket'))
        self.assertEqual(response.status_code, 200)  # 403 FORBIDDEN status code for not customer user
        logger.warning(response.status_code)
        logger.warning(response.content)  # Print with red color the content

    def test_customer_buy_tiket_legit_period(self):
        # Test code
        self.client.post(reverse('waterpark:customer-buy-tiket'), {'validity_day': date.today()})
        self.client.post(reverse('waterpark:customer-buy-tiket'), {'validity_day': date.today()+timedelta(days=55)})
        tiket = Tiket.objects.all()
        self.assertEqual(tiket.count(), 2)

    def test_customer_buy_tiket_validity_day_before_today(self):
        # Test code
        self.client.post(reverse('waterpark:customer-buy-tiket'), {'validity_day': date.today()-timedelta(days=1)})
        tiket = Tiket.objects.all()
        self.assertEqual(tiket.count(), 0)  # No tikets created, out of validation range

    def test_customer_buy_tiket_validity_day_after_a_year(self):
        # Test code
        self.client.post(reverse('waterpark:customer-buy-tiket'), {'validity_day': date.today()+timedelta(days=366)})
        tiket = Tiket.objects.all()
        self.assertEqual(tiket.count(), 0)  # No tikets created, out of validation range

    def test_customer_buy_tiket_check_integrity(self):
        # Test code
        self.client.post(reverse('waterpark:customer-buy-tiket'), {'validity_day': date.today()})
        tiket = Tiket.objects.all()
        self.assertIsNotNone(tiket[0].tiket_slug)  # Tiket id created, created in override method save
        self.assertIsNotNone(tiket[0].customer)    # Foreign key not null, tiket linked to the user 'paola98'
        self.assertEqual(tiket[0].customer.get_username(), 'paola98')

    def test_customer_tiket_check_integrity_after_deleted_customer(self):
        # Test code
        self.client.post(reverse('waterpark:customer-buy-tiket'), {'validity_day': date.today()})
        tiket = Tiket.objects.all()
        self.assertEqual(tiket.count(), 1)  # Tiket created
        user = myUser.objects.filter(username='paola98')
        user.delete()
        self.assertEqual(len(myUser.objects.all()), 0)  # User deleted
        self.assertIsNone(tiket[0].customer)  # Tiket still saved with no customer


class CustomerTiketListViewTests(TestCase):

    def setUp(self):
        # Setup run before every test method.
        user = myUser.objects.create(username='paola98', first_name='paola', last_name='verdi', gender='F',
                                     email='pv@gmail.com', is_staff_member=False, is_staff=False,
                                     is_superuser=False, birth_date='1998-02-13')
        user.set_password('Asdfghjkl!!')
        user.save()
        self.client.force_login(myUser.objects.get(username='paola98'))
        super().setUp()

    def test_customer_tiket_personal_list(self):
        # Create 3 tikets
        self.client.post(reverse('waterpark:customer-buy-tiket'), {'validity_day': date.today()})
        self.client.post(reverse('waterpark:customer-buy-tiket'), {'validity_day': date.today() + timedelta(days=1)})
        self.client.post(reverse('waterpark:customer-buy-tiket'), {'validity_day': date.today() + timedelta(days=2)})
        self.assertEqual(Tiket.objects.filter(customer__username='paola98').count(), 3)  # 3 tikets created, advanced data (date.today() + timedelta(days=2))
        # Go to the personal tiket list
        response = self.client.get(reverse('waterpark:customer-tiket-list'))
        self.assertEqual(response.status_code, 200)
        logger.warning(response.content)
        first_tiket_result_date = response.context['tiket_list'][0]['validity_day']
        self.assertEqual(first_tiket_result_date, date.today() + timedelta(days=2))  # DESC ORDER paginated by 1
        customer = myUser.objects.filter(username='paola98').values('id')[0]['id']
        self.assertEqual(response.context['tiket_list'][0]['customer_id'], customer)


class CustomerRequiredMixinTests(TestCase):

    def setUp(self):
        # Setup run before every test method.
        user = myUser.objects.create(username='paola98', first_name='paola', last_name='verdi', gender='F',
                                     email='pv@gmail.com', is_staff_member=True, is_staff=False,
                                     is_superuser=False, birth_date='1998-02-13')
        user.set_password('Asdfghjkl!!')
        user.save()  # User staff created
        self.client.force_login(myUser.objects.get(username='paola98'))
        super().setUp()

    def test_customer_required_mixin(self):
        # For example go to the personal tiket list, a page permited just to the customers
        response = self.client.get(reverse('waterpark:customer-tiket-list'))
        self.assertEqual(response.status_code, 403)  # Permission denied
        logger.warning(response.content)

    def test_staff_required_mixin(self):
        response = self.client.get(reverse('waterpark:staff-manage-tiket-main'))
        self.assertEqual(response.status_code, 200)  # Permission allowed
        logger.warning(response.content)


class StaffRequiredMixinTests(TestCase):

    def setUp(self):
        # Setup run before every test method.
        user = myUser.objects.create(username='paola98', first_name='paola', last_name='verdi', gender='F',
                                     email='pv@gmail.com', is_staff_member=False, is_staff=False,
                                     is_superuser=False, birth_date='1998-02-13')
        user.set_password('Asdfghjkl!!')
        user.save()  # User staff created
        self.client.force_login(myUser.objects.get(username='paola98'))
        super().setUp()

    def test_customer_required_mixin(self):
        # For example go to the personal tiket list, a page permited just to the customers
        response = self.client.get(reverse('waterpark:customer-tiket-list'))
        self.assertEqual(response.status_code, 200)  # Permission allowed
        logger.warning(response.content)

    def test_staff_required_mixin(self):
        response = self.client.get(reverse('waterpark:staff-manage-tiket-main'))
        self.assertEqual(response.status_code, 403)  # Permission denied
        logger.warning(response.content)


class DuplicateTiketTests(TestCase):

    def setUp(self):
        # Setup run before every test method.
        user = myUser.objects.create(username='paola98', first_name='paola', last_name='verdi', gender='F',
                                     email='pv@gmail.com', is_staff_member=False, is_staff=False,
                                     is_superuser=False, birth_date='1998-02-13')
        user.set_password('Asdfghjkl!!')
        user.save()
        self.client.force_login(myUser.objects.get(username='paola98'))
        super().setUp()

    def test_duplicate_tikets(self):
        self.client.post(reverse('waterpark:customer-buy-tiket'), {'validity_day': date.today()})
        self.client.post(reverse('waterpark:customer-buy-tiket'), {'validity_day': date.today()})
        tiket = Tiket.objects.all()
        self.assertEqual(tiket.count(), 1)


class ValidityDeltaFunctionTests(TestCase):

    def test_validity_delta_seasonpass(self):
        today = date.today()
        end_validity_first_january_next_year = today + timedelta(days=validity_delta())
        logger.warning('Today date: {}'.format(today))
        logger.warning('Expected: NEXT YEAR-01-01')
        logger.warning('Target date after function: {}'.format(end_validity_first_january_next_year))
        self.assertEqual(end_validity_first_january_next_year, date(today.year + 1, 1, 1))
