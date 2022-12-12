from django.db import models
from django.utils import timezone
from userpark.models import User as myUser
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date, timedelta
from PIL import Image
from django.template.defaultfilters import slugify
import uuid as UUID_LIB

# Where to upload pics of the user into user directory


def media_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance, filename)

# Other def


def validity_delta():
    start_date = date(date.today().year, 1, 1)
    end_date = date.today()
    delta_diff = end_date - start_date
    return 365 - delta_diff.days

# Create your models here.


class Tiket(models.Model):
    customer = models.ForeignKey(myUser, on_delete=models.SET_NULL, null=True)    # ForeignKey many to one
    tiket_slug = models.SlugField(null=False, unique=True)            # Slug reference used for each tiket created
    date_of_purchase = models.DateTimeField(default=timezone.now, null=False, blank=False)
    validity_day = models.DateField(help_text="Choose the day you will come to Waterland", null=False,
                                  validators=[MinValueValidator(limit_value=date.today), MaxValueValidator(limit_value=date.today()+timedelta(days=365))],
                                    default=date.today, blank=False, verbose_name='Entry Waterland date')
    cost = models.IntegerField(default=15, null=False, blank=False)

    class Meta:
        verbose_name_plural = 'Tickets'

    def __str__(self):
        return f'{self.customer.username} - Ticket:{self.tiket_slug}'

    def save(self, *args, **kwargs):
        if not self.tiket_slug:
            self.tiket_slug = slugify(str(UUID_LIB.uuid1()))
        super().save(*args, **kwargs)   # Save all at database


class SeasonPass(models.Model):
    customer = models.ForeignKey(myUser, on_delete=models.SET_NULL, null=True)
    seasonpass_slug = models.SlugField(null=False, unique=True)
    date_of_purchase = models.DateTimeField(default=timezone.now, null=False, blank=False)
    validity_from = models.DateField(default=date.today, null=False, blank=False)
    validity_to = models.DateField(default=date.today()+timedelta(days=validity_delta()), null=False, blank=False)
    seasonpass_photo = models.ImageField(upload_to=media_directory_path, blank=False, null=False,
                                     help_text='Add your photo, it shall added to your season pass',
                                     verbose_name='SeasonPass Photo')
    cost = models.IntegerField(default=125, null=False, blank=False)

    class Meta:
        verbose_name_plural = 'SeasonPass'

    def __str__(self):
        return f'{self.customer.username} - Profile/SeasonPass'

    def save(self, *args, **kwargs):
        if not self.seasonpass_slug:
            self.seasonpass_slug = slugify(str(UUID_LIB.uuid1()))
        super().save(*args, **kwargs)   # Save all at database

        if self.seasonpass_photo:    # Using Pillow Package to resize the seasonpass photo
            img = Image.open(self.seasonpass_photo.path)
            if img.height > 200 or img.width > 200:
                output_size = (200, 200)
                img.thumbnail(output_size)
                img.save(self.seasonpass_photo.path)
