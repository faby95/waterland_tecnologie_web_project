from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from userpark.models import User as myUser
from userpark.models import StaffAuthTable
from datetime import date, timedelta
from django.contrib.auth.password_validation import validate_password


class DateInput(forms.DateInput):
    input_type = 'date'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.setdefault('min', str(date.today() - timedelta(days=(365 * 100))))
        self.attrs.setdefault('max', str(date.today() - timedelta(days=(365 * 7))))


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
    staff_key = forms.CharField(max_length=20, help_text='Write here the key to create your staff account',
                                widget=forms.PasswordInput())

    class Meta(UserCreationForm.Meta):
        model = myUser
        fields = ['username', 'first_name', 'last_name', 'email', 'gender', 'birth_date', 'staff_assigned_code',
                  'staff_key']
        fields_required = ['username', 'email', 'staff_assigned_code', 'gender', 'birth_date', 'staff_key']
        widgets = {
            'birth_date': DateInput(),
        }

    def clean(self):
        cleaned_data = super(StaffSignUpForm, self).clean()
        code = cleaned_data.get('staff_assigned_code')  # retrive staff assigned code from the form
        keystaff = cleaned_data.get('staff_key')  # retrive staff key from the form
        auth = StaffAuthTable.objects.filter(code=code, key=keystaff,
                                             is_used=False)  # get instance, must be just one result
        if auth.count():
            auth_dict = auth.values('code', 'key')[0]  # get dict of the instance
            if keystaff == auth_dict['key'] and code == auth_dict['code']:
                if cleaned_data.get('password1') == cleaned_data.get('password2') and self.is_valid():
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
            'birth_date': DateInput(),  # Complete range
        }


class UpdatePasswordForm(forms.ModelForm):
    current_password = forms.CharField(max_length=4096, widget=forms.PasswordInput(),
                                       help_text='Type your current password here')  # 4096 django password length
    repeat_new_password = forms.CharField(max_length=4096, widget=forms.PasswordInput(),
                                          help_text='Type your new password again here')  # 4096 django password length

    class Meta:
        model = myUser
        fields = ['current_password', 'password', 'repeat_new_password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super(UpdatePasswordForm, self).clean()
        old_p = cleaned_data.get('current_password')
        p = cleaned_data.get('password')
        pp = cleaned_data.get('repeat_new_password')
        if old_p == p:
            self.add_error('current_password', u'Cannot use the current password as the new one')
            self.add_error('password', u'Cannot use the current password as the new one')
        if p != pp:
            self.add_error('password', u'Different password typing')
            self.add_error('repeat_new_password', u'Different password typing')
        else:
            validate_password(p)
        return cleaned_data
