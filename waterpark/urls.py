from django.urls import path
from waterpark.views import CustomerServiceMenuView, CustomerBuyTiketView, CustomerBuySeasonPassView, CustomerTiketListView, CustomerSeasonPassListView, StaffManageTiketMainView, StaffManageSeasonpassMainView, SearchTiketByDateListView, SearchTiketByYearListView, SearchTiketByRangeListView, SearchSeasonpassByYearListView, SearchCustomerTiketView, SearchCustomerSeasonpassView, SearchCustomerTiketListView, SearchCustomerSeasonpassListView

from django.conf import settings
from django.conf.urls.static import static

app_name = 'waterpark'

urlpatterns = [

    path('tikets&seasonpass/', CustomerServiceMenuView.as_view(), name='customerservices'),
    path('tikets&seasonpass/buy_a_tiket/', CustomerBuyTiketView.as_view(), name='customer-buy-tiket'),
    path('tikets&seasonpass/buy_a_seasonpass/', CustomerBuySeasonPassView.as_view(), name='customer-buy-seasonpass'),
    path('tikets&seasonpass/my_tikets/', CustomerTiketListView.as_view(), name='customer-tiket-list'),
    path('tikets&seasonpass/my_seasonpass/', CustomerSeasonPassListView.as_view(), name='customer-seasonpass-list'),
    path('tiket_management/', StaffManageTiketMainView.as_view(), name='staff-manage-tiket-main'),
    path('seasonpass_management/', StaffManageSeasonpassMainView.as_view(), name='staff-manage-seasonpass-main'),
    path('tiket_management/search_by_date/', SearchTiketByDateListView.as_view(), name='staff-manage-tiket-by-day'),
    path('tiket_management/search_by_year/', SearchTiketByYearListView.as_view(), name='staff-manage-tiket-by-year'),
    path('tiket_management/search_by_range/', SearchTiketByRangeListView.as_view(), name='staff-manage-tiket-by-range'),
    path('seasonpass_management/search_by_year/', SearchSeasonpassByYearListView.as_view(), name='staff-manage-seasonpass-by-year'),
    path('customer_search_tiket/', SearchCustomerTiketView.as_view(), name='staff-search-tiket-for-user'),
    path('customer_search_tiket/customer/', SearchCustomerTiketListView.as_view(), name='staff-search-tiket-for-user-results'),
    path('customer_search_seasonpass/', SearchCustomerSeasonpassView.as_view(), name='staff-search-seasonpass-for-user'),
    path('customer_search_seasonpass/customer/', SearchCustomerSeasonpassListView.as_view(), name='staff-search-seasonpass-for-user-results'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
