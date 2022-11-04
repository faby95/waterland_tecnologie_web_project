from django import forms
from reviewpark.models import Feedback, Faq
from django.db import transaction
from django.utils import timezone


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['stars', 'feedback_text']
        fields_required = ['stars', 'feedback_text']


class FaqAskForm(forms.ModelForm):
    class Meta:
        model = Faq
        fields = ['ask']
        fields_required = ['ask']


class FaqAnswareForm(forms.ModelForm):
    class Meta:
        model = Faq
        fields = ['answare']
        fields_required = ['answare']

    @transaction.atomic
    def save(self):
        answare_f = super().save(commit=False)
        answare_f.answare_date = timezone.now()
        answare_f.save()
        return answare_f
