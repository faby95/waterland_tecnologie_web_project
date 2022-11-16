# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from waterlandmixins.mixins import CustomerRequiredMixin, StaffRequiredMixin, PurchaseRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from reviewpark.models import Feedback, Faq
from reviewpark.forms import FeedbackForm, FaqAskForm, FaqAnswareForm
from django.db.models import Q
from django.contrib import messages


# Create your views here.


class FeedbackCreateView(LoginRequiredMixin, CustomerRequiredMixin, SuccessMessageMixin, PurchaseRequiredMixin, CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'reviewpark/feedback/feedback_create.html'
    success_url = reverse_lazy('reviewpark:feedback-list')
    success_message = 'Feedback left, thanks for leaving your Feedback'
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.customer = self.request.user
        self.object.save()
        return super().form_valid(form)


class FeedbackListView(ListView):
    model = Feedback
    template_name = 'reviewpark/feedback/feedback_list.html'
    context_object_name = "feedback_list"  # default is object_list
    paginate_by = 5

    def get_queryset(self):
        queryset = Feedback.objects.all().order_by('-feedback_date')   # DESC date, default ASC
        return queryset


class FaqCreateView(LoginRequiredMixin, CustomerRequiredMixin, SuccessMessageMixin, CreateView):
    model = Faq
    form_class = FaqAskForm
    template_name = 'reviewpark/faq/faq_ask.html'
    success_url = reverse_lazy('reviewpark:faq-mine')
    success_message = 'FAQ sent'
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.customer = self.request.user
        self.object.save()
        return super().form_valid(form)


class FaqMineView(LoginRequiredMixin, CustomerRequiredMixin, ListView):
    model = Faq
    template_name = 'reviewpark/faq/faq_list.html'
    context_object_name = "faq_list"  # default is object_list
    paginate_by = 2
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        queryset = Faq.objects.filter(customer=self.request.user).order_by('-faq_date')   # DESC date, default ASC
        return queryset


class FaqListView(ListView):
    model = Faq
    template_name = 'reviewpark/faq/faq_list.html'
    context_object_name = "faq_list"  # default is object_list
    paginate_by = 5

    def get_queryset(self):
        queryset = Faq.objects.all().order_by('-faq_date')   # DESC date, default ASC
        return queryset

# Staff Faq Class


class FaqStaffListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Faq
    template_name = 'reviewpark/faq/faq_staff_list.html'
    context_object_name = "faq_list"  # default is object_list
    paginate_by = 2
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        queryset = Faq.objects.filter(answare=None).order_by('-faq_date')  # DESC date, default ASC
        return queryset


class FaqStaffDeleteView(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Faq
    template_name = 'reviewpark/faq/faq_staff_delete.html'
    success_url = reverse_lazy('reviewpark:faq-staff-list')
    success_message = 'Faq deleted'
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'


class FaqStaffAnswareView(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Faq
    form_class = FaqAnswareForm
    template_name = 'reviewpark/faq/faq_answer.html'
    success_url = reverse_lazy('reviewpark:faq-staff-list')
    success_message = 'Answare success'
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'


class FeedbackStaffDeleteView(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Feedback
    template_name = 'reviewpark/feedback/feedback_staff_delete.html'
    success_url = reverse_lazy('reviewpark:feedback-list')
    success_message = 'Feedback deleted'
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'


class SearchContextFaqView(ListView):
    model = Faq
    template_name = 'reviewpark/faq/faq_list.html'
    context_object_name = "faq_list"  # default is object_list
    paginate_by = 3

    def get_queryset(self):
        contextform = self.request.GET.get('contextform')
        faq_list = Faq.objects.filter(Q(ask__contains=contextform) | Q(answare__contains=contextform)).order_by('-faq_date')
        if faq_list.count():
            messages.success(self.request, 'Found {} Faq about context ({})'.format(faq_list.count(), contextform))
        else:
            messages.warning(self.request, 'No Faq found about context ({})'.format(contextform))
        return faq_list


class SearchFeedbackByStarsView(ListView):
    model = Feedback
    template_name = 'reviewpark/feedback/feedback_list.html'
    context_object_name = "feedback_list"  # default is object_list
    paginate_by = 3

    def get_queryset(self):
        try:
            starsform = int(self.request.GET.get('starsform'))
            if 1 <= starsform <= 5:
                feedback_list = Feedback.objects.filter(stars=starsform).order_by('-feedback_date')
                if feedback_list.count():
                    messages.success(self.request, 'Found {} Feedback with {} stars'.format(feedback_list.count(), starsform))
                else:
                    messages.warning(self.request, 'No Feedback found with {} stars'.format(starsform))
            else:
                messages.warning(self.request, '{} stars out of legal range (1 to 5 stars)'.format(starsform))
                feedback_list = Feedback.objects.all().order_by('-feedback_date')
            return feedback_list
        except:
            messages.warning(self.request, 'You cannot send nothing')
            return Feedback.objects.all().order_by('-feedback_date')
