from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from userpark.models import User as myUser
from datetime import date, timedelta


class DateInput(forms.DateInput):
    input_type = 'date'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.setdefault('min', str(date.today()-timedelta(days=(365*100))))
        self.attrs.setdefault('max', str(date.today()-timedelta(days=(365*7))))


class CustomerSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = myUser
        fields = ['username', 'first_name', 'last_name', 'email', 'gender', 'birth_date']
        fields_required = ['username', 'email', 'gender', 'birth_date']
        widgets = {
            'birth_date': DateInput(),
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_staff_member = False
        user.staff_assigned_code = None
        user.save()
        return user


class StaffSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = myUser
        fields = ['username', 'first_name', 'last_name', 'email', 'gender', 'birth_date', 'staff_assigned_code']
        fields_required = ['username', 'email', 'staff_assigned_code', 'gender', 'birth_date']
        widgets = {
            'birth_date': DateInput(),
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_staff_member = True
        user.save()
        return user

# Update profile form


class UpdateBirthdateForm(forms.ModelForm):
    class Meta:
        model = myUser
        fields = ['birth_date']
        widgets = {
            'birth_date': DateInput(),
        }
