from django.contrib import admin

from waterpark.models import Tiket, SeasonPass

# Register your models here.
# admin.site.register


@admin.register(Tiket)
class TiketAdmin(admin.ModelAdmin):
    list_display = (Tiket.__str__, 'customer', 'tiket_slug', 'date_of_purchase', 'validity_day', 'cost')
    list_filter = (('validity_day', admin.DateFieldListFilter),
                   ('date_of_purchase', admin.DateFieldListFilter),)


@admin.register(SeasonPass)
class SeasonPassAdmin(admin.ModelAdmin):
    list_display = (SeasonPass.__str__, 'customer', 'seasonpass_slug', 'date_of_purchase', 'validity_from',
                    'validity_to', 'cost')
    list_filter = (('date_of_purchase', admin.DateFieldListFilter),)
