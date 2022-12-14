from django.test import TestCase
from datetime import date, timedelta
from .models import User as myUser
from .models import StaffAuthTable
from django.urls import reverse

# Create your tests here.

# Test completi in waterpark (tiket) e reviewpark (feedback)
# Questi sono test di prova sulle view dell'utente


class CreateUserTypeTests(TestCase):

    def test_create_customer_type(self):
        response = self.client.post(reverse('userpark:customer-create'), {'username': 'paola98', 'gender': 'F',
                                                                          'email': 'pv@gmail.com',
                                                                          'birth_date': date.today()-timedelta(days=(365*27)),
                                                                          'password1': 'Asdfghjkl!!',
                                                                          'password2': 'Asdfghjkl!!'}, follow=True)
        customer = myUser.objects.filter(username='paola98').values('is_staff_member')
        admin_login_interface = myUser.objects.filter(username='paola98').values('is_staff')
        superuser_permission = myUser.objects.filter(username='paola98').values('is_superuser')
        active_user = myUser.objects.filter(username='paola98').values('is_active')
        self.assertEqual(response.status_code, 200)  # After redirect to home, 200 OK
        self.assertEqual(customer[0]['is_staff_member'], False)
        self.assertEqual(admin_login_interface[0]['is_staff'], False)
        self.assertEqual(superuser_permission[0]['is_superuser'], False)
        self.assertEqual(active_user[0]['is_active'], True)

    def test_create_staff_type(self):
        StaffAuthTable.objects.create(code='52gf3', key='createstaffuser', is_used=False)
        response = self.client.post(reverse('userpark:staff-create'), {'username': 'paola98', 'gender': 'F',
                                                                       'email': 'pv@gmail.com',
                                                                       'birth_date': date.today()-timedelta(days=(365*27)),
                                                                       'password1': 'Asdfghjkl!!',
                                                                       'password2': 'Asdfghjkl!!',
                                                                       'staff_assigned_code': '52gf3',
                                                                       'staff_key': 'createstaffuser'}, follow=True)
        staff = myUser.objects.filter(username='paola98').values('is_staff_member')
        admin_login_interface = myUser.objects.filter(username='paola98').values('is_staff')
        superuser_permission = myUser.objects.filter(username='paola98').values('is_superuser')
        active_user = myUser.objects.filter(username='paola98').values('is_active')
        self.assertEqual(response.status_code, 200)  # After redirect to home, 200 OK
        self.assertEqual(staff[0]['is_staff_member'], True)
        self.assertEqual(admin_login_interface[0]['is_staff'], False)
        self.assertEqual(superuser_permission[0]['is_superuser'], False)
        self.assertEqual(active_user[0]['is_active'], True)

    def test_create_customer_out_of_birthdate_range_in_past(self):
        response = self.client.post(reverse('userpark:customer-create'), {'username': 'paola98', 'gender': 'F',
                                                                          'email': 'pv@gmail.com',
                                                                          'birth_date': date.today() - timedelta(
                                                                              days=(365 * 105)),
                                                                          'password1': 'Asdfghjkl!!',
                                                                          'password2': 'Asdfghjkl!!'})
        customer = myUser.objects.filter(username='paola98')
        self.assertEqual(response.status_code, 200)  # No follow=True, 200 OK = no redirect, no user created
        self.assertEqual(customer.count(), 0)

    def test_create_customer_out_of_birthdate_range_in_future(self):
        response = self.client.post(reverse('userpark:customer-create'), {'username': 'paola98', 'gender': 'F',
                                                                          'email': 'pv@gmail.com',
                                                                          'birth_date': date.today() + timedelta(
                                                                              days=1),
                                                                          'password1': 'Asdfghjkl!!',
                                                                          'password2': 'Asdfghjkl!!'})
        customer = myUser.objects.filter(username='paola98')
        self.assertEqual(response.status_code, 200)  # No follow=True, 200 OK = no redirect, no user created
        self.assertEqual(customer.count(), 0)

    def test_create_customer_in_range_of_birthdate(self):
        response = self.client.post(reverse('userpark:customer-create'), {'username': 'paola98', 'gender': 'F',
                                                                          'email': 'pv@gmail.com',
                                                                          'birth_date': date.today() - timedelta(
                                                                              days=(365 * 15)),
                                                                          'password1': 'Asdfghjkl!!',
                                                                          'password2': 'Asdfghjkl!!'})
        customer = myUser.objects.filter(username='paola98')
        self.assertEqual(response.status_code, 302)  # No follow=True, 302 redirect to home = user has been created
        self.assertEqual(customer.count(), 1)

    def test_create_staff_out_of_birthdate_range_in_past(self):
        StaffAuthTable.objects.create(code='52gf3', key='createstaffuser', is_used=False)
        response = self.client.post(reverse('userpark:staff-create'), {'username': 'paola98', 'gender': 'F',
                                                                       'email': 'pv@gmail.com',
                                                                       'birth_date': date.today()-timedelta(days=(365*105)),
                                                                       'password1': 'Asdfghjkl!!',
                                                                       'password2': 'Asdfghjkl!!',
                                                                       'staff_assigned_code': '52gf3',
                                                                       'staff_key': 'createstaffuser'})
        staff = myUser.objects.filter(username='paola98')
        self.assertEqual(response.status_code, 200)  # No follow=True, 200 OK = no redirect, no user created
        self.assertEqual(staff.count(), 0)

    def test_create_staff_out_of_birthdate_range_in_future(self):
        StaffAuthTable.objects.create(code='52gf3', key='createstaffuser', is_used=False)
        response = self.client.post(reverse('userpark:staff-create'), {'username': 'paola98', 'gender': 'F',
                                                                       'email': 'pv@gmail.com',
                                                                       'birth_date': date.today()+timedelta(days=1),
                                                                       'password1': 'Asdfghjkl!!',
                                                                       'password2': 'Asdfghjkl!!',
                                                                       'staff_assigned_code': '52gf3',
                                                                       'staff_key': 'createstaffuser'})
        staff = myUser.objects.filter(username='paola98')
        self.assertEqual(response.status_code, 200)  # No follow=True, 200 OK = no redirect, no user created
        self.assertEqual(staff.count(), 0)

    def test_create_staff_in_range_of_birthdate(self):
        StaffAuthTable.objects.create(code='52gf3', key='createstaffuser', is_used=False)
        response = self.client.post(reverse('userpark:staff-create'), {'username': 'paola98', 'gender': 'F',
                                                                       'email': 'pv@gmail.com',
                                                                       'birth_date': date.today() - timedelta(days=(365*27)),
                                                                       'password1': 'Asdfghjkl!!',
                                                                       'password2': 'Asdfghjkl!!',
                                                                       'staff_assigned_code': '52gf3',
                                                                       'staff_key': 'createstaffuser'})
        staff = myUser.objects.filter(username='paola98')
        self.assertEqual(response.status_code, 302)  # No follow=True, 302 redirect to home = user has been created
        self.assertEqual(staff.count(), 1)


class CreateCustomerMissingFieldsTests(TestCase):

    def test_username_missing(self):
        response = self.client.post(reverse('userpark:customer-create'), {'username': '', 'gender': 'F',
                                                                          'email': 'pv@gmail.com',
                                                                          'birth_date': date.today() - timedelta(
                                                                              days=(365 * 27)),
                                                                          'password1': 'Asdfghjkl!!',
                                                                          'password2': 'Asdfghjkl!!'})
        usercount = myUser.objects.all()
        self.assertNotEqual(response.status_code, 302)    # No redirect to home, no user created
        self.assertEqual(usercount.count(), 0)

    def test_email_missing(self):
        response = self.client.post(reverse('userpark:customer-create'), {'username': 'paola98', 'gender': 'F',
                                                                          'email': '',
                                                                          'birth_date': date.today() - timedelta(
                                                                              days=(365 * 27)),
                                                                          'password1': 'Asdfghjkl!!',
                                                                          'password2': 'Asdfghjkl!!'})
        usercount = myUser.objects.all()
        self.assertNotEqual(response.status_code, 302)  # No redirect to home, no user created
        self.assertEqual(usercount.count(), 0)

    def test_birth_date_missing(self):
        response = self.client.post(reverse('userpark:customer-create'), {'username': 'paola98', 'gender': 'F',
                                                                          'email': '',
                                                                          'birth_date': '',
                                                                          'password1': 'Asdfghjkl!!',
                                                                          'password2': 'Asdfghjkl!!'})
        usercount = myUser.objects.all()
        self.assertNotEqual(response.status_code, 302)  # No redirect to home, no user created
        self.assertEqual(usercount.count(), 0)


class CreateStaffMissingFieldsTests(TestCase):

    def test_username_missing(self):
        StaffAuthTable.objects.create(code='52gf3', key='createstaffuser', is_used=False)
        response = self.client.post(reverse('userpark:staff-create'), {'username': '', 'gender': 'F',
                                                                       'email': 'pv@gmail.com',
                                                                       'birth_date': date.today() - timedelta(
                                                                           days=(365 * 27)),
                                                                       'password1': 'Asdfghjkl!!',
                                                                       'password2': 'Asdfghjkl!!',
                                                                       'staff_assigned_code': '52gf3',
                                                                       'staff_key': 'createstaffuser'})
        usercount = myUser.objects.all()
        self.assertNotEqual(response.status_code, 302)  # No redirect to home, no user created
        self.assertEqual(usercount.count(), 0)

    def test_email_missing(self):
        StaffAuthTable.objects.create(code='52gf3', key='createstaffuser', is_used=False)
        response = self.client.post(reverse('userpark:staff-create'), {'username': 'paola98', 'gender': 'F',
                                                                       'email': '',
                                                                       'birth_date': date.today() - timedelta(
                                                                           days=(365 * 27)),
                                                                       'password1': 'Asdfghjkl!!',
                                                                       'password2': 'Asdfghjkl!!',
                                                                       'staff_assigned_code': '52gf3',
                                                                       'staff_key': 'createstaffuser'})
        usercount = myUser.objects.all()
        self.assertNotEqual(response.status_code, 302)  # No redirect to home, no user created
        self.assertEqual(usercount.count(), 0)

    def test_staff_code_missing(self):
        StaffAuthTable.objects.create(code='52gf3', key='createstaffuser', is_used=False)
        response = self.client.post(reverse('userpark:staff-create'), {'username': 'paola98', 'gender': 'F',
                                                                       'email': 'pv@gmail.com',
                                                                       'birth_date': date.today() - timedelta(
                                                                           days=(365 * 27)),
                                                                       'password1': 'Asdfghjkl!!',
                                                                       'password2': 'Asdfghjkl!!',
                                                                       'staff_assigned_code': '',
                                                                       'staff_key': 'createstaffuser'})
        usercount = myUser.objects.all()
        self.assertNotEqual(response.status_code, 302)  # No redirect to home, no user created
        self.assertEqual(usercount.count(), 0)

    def test_birth_day_missing(self):
        StaffAuthTable.objects.create(code='52gf3', key='createstaffuser', is_used=False)
        response = self.client.post(reverse('userpark:staff-create'), {'username': 'paola98', 'gender': 'F',
                                                                       'email': 'pv@gmail.com',
                                                                       'birth_date': '',
                                                                       'password1': 'Asdfghjkl!!',
                                                                       'password2': 'Asdfghjkl!!',
                                                                       'staff_assigned_code': '52gf3',
                                                                       'staff_key': 'createstaffuser'})
        usercount = myUser.objects.all()
        self.assertNotEqual(response.status_code, 302)  # No redirect to home, no user created
        self.assertEqual(usercount.count(), 0)

    def test_staff_key_missing(self):
        StaffAuthTable.objects.create(code='52gf3', key='createstaffuser', is_used=False)
        response = self.client.post(reverse('userpark:staff-create'), {'username': 'paola98', 'gender': 'F',
                                                                       'email': 'pv@gmail.com',
                                                                       'birth_date': '',
                                                                       'password1': 'Asdfghjkl!!',
                                                                       'password2': 'Asdfghjkl!!',
                                                                       'staff_assigned_code': '52gf3',
                                                                       'staff_key': ''})
        usercount = myUser.objects.all()
        self.assertNotEqual(response.status_code, 302)  # No redirect to home, no user created
        self.assertEqual(usercount.count(), 0)

    def test_wrong_staff_key(self):
        StaffAuthTable.objects.create(code='52gf3', key='createstaffuser', is_used=False)
        response = self.client.post(reverse('userpark:staff-create'), {'username': 'paola98', 'gender': 'F',
                                                                       'email': 'pv@gmail.com',
                                                                       'birth_date': '',
                                                                       'password1': 'Asdfghjkl!!',
                                                                       'password2': 'Asdfghjkl!!',
                                                                       'staff_assigned_code': '52gf3',
                                                                       'staff_key': 'fsdfsd'})
        usercount = myUser.objects.all()
        self.assertNotEqual(response.status_code, 302)  # No redirect to home, no user created
        self.assertEqual(usercount.count(), 0)
