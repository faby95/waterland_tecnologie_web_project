from django.db import models
from django.utils import timezone
from userpark.models import User as myUser

# Create your models here.


class Feedback(models.Model):
    STARS_CHOICES = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )
    customer = models.ForeignKey(myUser, on_delete=models.SET_NULL, null=True)
    feedback_date = models.DateTimeField(default=timezone.now, null=False, blank=False)
    stars = models.PositiveIntegerField(choices=STARS_CHOICES, null=False, blank=False,
                                        help_text='Rate your expericence at WaterLand, from 1 to 5 stars')
    feedback_text = models.TextField(max_length=300, null=False, blank=False, help_text='Tell your experience here, max 300 characters')

    class Meta:
        verbose_name_plural = 'Feedback'

    def __str__(self):
        return f'Feedback - n°{self.id}'


class Faq(models.Model):
    customer = models.ForeignKey(myUser, on_delete=models.SET_NULL, null=True)
    faq_date = models.DateTimeField(default=timezone.now, null=False, blank=False)
    ask = models.TextField(max_length=300, null=False, blank=False, help_text='Write your question here, max 300 characters', verbose_name='FAQ')
    answare = models.TextField(max_length=500, null=True, default=None,
                               help_text='Answare to the customer\'s question here, max 500 characters')
    answare_date = models.DateTimeField(null=True, default=None)

    class Meta:
        verbose_name_plural = 'FAQ'

    def __str__(self):
        return f'FAQ - n°{self.id}'
