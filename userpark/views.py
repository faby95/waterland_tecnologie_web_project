# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.hashers import check_password, make_password
from userpark.models import User as myUser, StaffAuthTable
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView
from userpark.forms import CustomerSignUpForm, StaffSignUpForm, UpdateBirthdateForm, UpdatePasswordForm
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver


@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    messages.add_message(request, messages.SUCCESS, 'Logged Out')


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

    def form_invalid(self, form):
        if form.cleaned_data.get('staff_assigned_code'):
            c = form.cleaned_data.get('staff_assigned_code')
            keys = StaffAuthTable.objects.filter(code=c)
            keys.update(is_used=False)
        return super().form_invalid(form)


# User profile view


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'userpark/profile/profile_detail.html'
    login_url = 'userpark:login'  # Redirect Login needed
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


class UserUpdatePasswordView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = myUser
    form_class = UpdatePasswordForm
    template_name = 'userpark/profile/update_password.html'
    success_url = reverse_lazy('userpark:user-profile')
    success_message = 'Password updated'
    slug_field = 'slug'
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        currentpassword = self.request.user.password
        currentpasswordentered = form.cleaned_data.get("current_password")
        matchcheck = check_password(currentpasswordentered, currentpassword)
        if matchcheck:
            self.object = form.save(commit=False)
            self.object.password = make_password(self.object.password)
            self.object.save()
            return super().form_valid(form)
        else:
            messages.warning(self.request, 'Current password is not the expected one!')
            return self.form_invalid(form)


# User delete view


class UserDeleteProfileView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = myUser
    template_name = 'userpark/profile/delete_profile.html'
    success_url = reverse_lazy('home')
    success_message = 'Profile deleted'
    slug_field = 'slug'
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'
