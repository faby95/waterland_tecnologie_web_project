from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from userpark.models import User as myUser
from userpark.models import StaffAuthTable
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
    staff_key = forms.CharField(max_length=20, help_text='Write here the key to create your staff account')

    class Meta(UserCreationForm.Meta):
        model = myUser
        fields = ['username', 'first_name', 'last_name', 'email', 'gender', 'birth_date', 'staff_assigned_code', 'staff_key']
        fields_required = ['username', 'email', 'staff_assigned_code', 'gender', 'birth_date', 'staff_key']
        widgets = {
            'birth_date': DateInput(),
        }

    def clean(self):
        cleaned_data = super(StaffSignUpForm, self).clean()
        code = cleaned_data.get('staff_assigned_code')  # retrive staff assigned code from the form
        keystaff = cleaned_data.get('staff_key')        # retrive staff key from the form
        auth = StaffAuthTable.objects.filter(code=code, key=keystaff, is_used=False)  # get instance, must be just one result
        if auth.count():
            auth_dict = auth.values('code', 'key')[0]  # get dict of the instance
            if keystaff == auth_dict['key'] and code == auth_dict['code']:
                auth.update(is_used=True)
            else:
                self.add_error('staff_key', u'Invalid combination!')
                self.add_error('staff_assigned_code', u'Invalid combination!')
        else:
            self.add_error('staff_key', u'Invalid combination!')
            self.add_error('staff_assigned_code', u'Invalid combination!')
        return cleaned_data

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
