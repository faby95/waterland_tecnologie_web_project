from django.urls import path
from reviewpark.views import FeedbackCreateView, FeedbackListView, FaqCreateView, FaqMineView, FaqListView, FaqStaffListView, FaqStaffDeleteView, FaqStaffAnswareView, FeedbackStaffDeleteView, SearchContextFaqView, SearchFeedbackByStarsView

from django.conf import settings
from django.conf.urls.static import static

app_name = 'reviewpark'

urlpatterns = [

    path('leavefeedback/', FeedbackCreateView.as_view(), name='leave-feedback'),
    path('feedback/', FeedbackListView.as_view(), name='feedback-list'),
    path('feedback/staff/<int:pk>/delete_feedback/', FeedbackStaffDeleteView.as_view(), name='feedback-staff-delete'),
    path('faq/ask/', FaqCreateView.as_view(), name='faq-ask'),
    path('faq/mine/', FaqMineView.as_view(), name='faq-mine'),
    path('faq/', FaqListView.as_view(), name='faq'),
    path('faq/staff_list/', FaqStaffListView.as_view(), name='faq-staff-list'),
    path('faq/staff_list/<int:pk>/delete_faq/', FaqStaffDeleteView.as_view(), name='faq-staff-delete'),
    path('faq/staff_list/<int:pk>/answer_faq/', FaqStaffAnswareView.as_view(), name='faq-staff-answare'),
    path('faq/search/', SearchContextFaqView.as_view(), name='faq-search-context'),
    path('feedback/search/', SearchFeedbackByStarsView.as_view(), name='feedback-search-stars'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
