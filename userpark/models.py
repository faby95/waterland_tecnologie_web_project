from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date, timedelta
from PIL import Image
from django.template.defaultfilters import slugify
import uuid as UUID_LIB

AbstractUser._meta.get_field('email')._unique = True
AbstractUser._meta.get_field('email').blank = False
AbstractUser._meta.get_field('email').null = False
AbstractUser._meta.get_field('username')._unique = True

# Where to upload pics of the user into user directory


def media_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance, filename)


# Create your models here.


class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, help_text="Are you male or female?", null=True, default=None)
    birth_date = models.DateField(help_text="Place your birthday here", null=True,
                                  validators=[MaxValueValidator(limit_value=date.today()-timedelta(days=(365*7))),
                                              MinValueValidator(limit_value=date.today()-timedelta(days=(365*100)))], default=None)
    staff_assigned_code = models.CharField(max_length=5, help_text="Place your staff code here", null=True, unique=True, default=None)
    is_staff_member = models.BooleanField(default=False)
    propic = models.ImageField(upload_to=media_directory_path, blank=True, null=True,
                               default=None, help_text='Add your profile picture here', verbose_name='Picture Profile')
    slug = models.SlugField(null=False, unique=True)  # max length disabled

    def __str__(self):
        return f'{self.username} - Profile'

    def save(self, *args, **kwargs):
        if self.is_staff:
            self.is_staff_member = True

        if not self.slug:
            self.slug = slugify(str(UUID_LIB.uuid1()))
        super().save(*args, **kwargs)  # Save all at database

        if self.propic:    # Using Pillow Package to resize the propic
            img = Image.open(self.propic.path)
            if img.height > 200 or img.width > 200:
                output_size = (200, 200)
                img.thumbnail(output_size)
                img.save(self.propic.path)


class StaffAuthTable(models.Model):  # External populated table for hired staff
    code = models.CharField(max_length=5, null=False, blank=False, unique=True)
    key = models.CharField(max_length=20, null=False, blank=False, default='createstaffuser')
    is_used = models.BooleanField(blank=False, null=False, default=False)

    class Meta:
        verbose_name_plural = 'Staff-Auth-Table'

    def __str__(self):
        return f'{self.code}-{self.key}-{self.is_used}'
