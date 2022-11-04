# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from userpark.models import User as myUser

from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView
from userpark.forms import CustomerSignUpForm, StaffSignUpForm, UpdateBirthdateForm
from django.contrib.auth import views as auth_views


# Create your views here.

# User Sin-In and Log-In view


class UserCreateView(TemplateView):
    template_name = 'userpark/user_create.html'


class UserLoginView(SuccessMessageMixin, auth_views.LoginView):
    success_message = 'Logged In'


class CustomerSignUpView(SuccessMessageMixin, CreateView):
    model = myUser  # Where to save
    form_class = CustomerSignUpForm
    template_name = 'userpark/customer_signin.html'
    success_url = reverse_lazy('home')
    success_message = 'Your customer user has been created'


class StaffSignUpView(SuccessMessageMixin, CreateView):
    model = myUser  # Where to save
    form_class = StaffSignUpForm
    template_name = 'userpark/sfaff_signin.html'
    success_url = reverse_lazy('home')
    success_message = 'Your staff user has been created'

# User profile view


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'userpark/profile/profile_detail.html'
    login_url = 'userpark:login'          # Redirect Login needed
    redirect_field_name = 'redirect_to'

# Update user info view


class UserUpdatePropicView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = myUser
    fields = ['propic']
    template_name = 'userpark/profile/update_propic.html'
    success_url = reverse_lazy('userpark:user-profile')
    success_message = 'Profile picture updated'
    slug_field = 'slug'
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'


class UserUpdateFirstNameView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = myUser
    fields = ['first_name']
    template_name = 'userpark/profile/update_first_name.html'
    success_url = reverse_lazy('userpark:user-profile')
    success_message = 'First name updated'
    slug_field = 'slug'
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'


class UserUpdateLastNameView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = myUser
    fields = ['last_name']
    template_name = 'userpark/profile/update_last_name.html'
    success_url = reverse_lazy('userpark:user-profile')
    success_message = 'Last name updated'
    slug_field = 'slug'
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'


class UserUpdateEmailView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = myUser
    fields = ['email']
    template_name = 'userpark/profile/update_email.html'
    success_url = reverse_lazy('userpark:user-profile')
    success_message = 'Email updated'
    slug_field = 'slug'
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'


class UserUpdateGenderView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = myUser
    fields = ['gender']
    template_name = 'userpark/profile/update_gender.html'
    success_url = reverse_lazy('userpark:user-profile')
    success_message = 'Gender updated'
    slug_field = 'slug'
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'


class UserUpdateBirthDateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = myUser
    form_class = UpdateBirthdateForm
    template_name = 'userpark/profile/update_birth_date.html'
    success_url = reverse_lazy('userpark:user-profile')
    success_message = 'Birth date updated'
    slug_field = 'slug'
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'


class UserDeleteProfileView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = myUser
    template_name = 'userpark/profile/delete_profile.html'
    success_url = reverse_lazy('home')
    success_message = 'Profile deleted'
    slug_field = 'slug'
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'
