from django.contrib import admin
from reviewpark.models import Feedback, Faq

# Register your models here.
# admin.site.register


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (Feedback.__str__, 'customer', 'feedback_date', 'stars')
    list_filter = (('feedback_date', admin.DateFieldListFilter),
                   ('stars', admin.ChoicesFieldListFilter),
                   )


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = (Faq.__str__, 'customer', 'faq_date', 'answare_date')
    list_filter = (('faq_date', admin.DateFieldListFilter),)
