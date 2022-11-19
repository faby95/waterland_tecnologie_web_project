from django.urls import path
from django.contrib.auth import views as auth_views
from userpark.views import UserCreateView, CustomerSignUpView, StaffSignUpView, UserLoginView, UserProfileView, UserUpdatePropicView, UserUpdateFirstNameView, UserUpdateLastNameView, UserUpdateGenderView, UserUpdateEmailView, UserUpdateBirthDateView, UserUpdatePasswordView, UserDeleteProfileView

from django.conf import settings
from django.conf.urls.static import static

app_name = 'userpark'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('user_create/', UserCreateView.as_view(), name='user-create'),
    path('user_create/customer_sign_in/', CustomerSignUpView.as_view(), name='customer-create'),
    path('user_create/staff_sign_in/', StaffSignUpView.as_view(), name='staff-create'),
    path('user_profile/', UserProfileView.as_view(), name='user-profile'),
    path('user_profile/<slug:slug>/update_propic/', UserUpdatePropicView.as_view(), name='user-profile-update-propic'),   # HERE
    path('user_profile/<slug:slug>/update_first_name/', UserUpdateFirstNameView.as_view(), name='user-profile-update-firstname'),
    path('user_profile/<slug:slug>/update_last_name/', UserUpdateLastNameView.as_view(), name='user-profile-update-lastname'),
    path('user_profile/<slug:slug>/update_gender/', UserUpdateGenderView.as_view(), name='user-profile-update-gender'),
    path('user_profile/<slug:slug>/update_email/', UserUpdateEmailView.as_view(), name='user-profile-update-email'),
    path('user_profile/<slug:slug>/update_birth_date/', UserUpdateBirthDateView.as_view(), name='user-profile-update-birthdate'),
    path('user_profile/<slug:slug>/update_password/', UserUpdatePasswordView.as_view(), name='user-profile-update-password'),
    path('user_profile/<slug:slug>/delete_profile/', UserDeleteProfileView.as_view(), name='user-profile-delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
