# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from waterlandmixins.mixins import CustomerRequiredMixin, StaffRequiredMixin
from waterpark.models import Tiket, SeasonPass
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView
from waterpark.forms import TiketForm, SeasonPassForm
from django.contrib import messages
from datetime import date

# Create your views here.

# Customer views


class CustomerServiceMenuView(LoginRequiredMixin, CustomerRequiredMixin, TemplateView):
    template_name = 'waterpark/customer/services_tiket_seasonpass.html'
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'


class CustomerBuyTiketView(LoginRequiredMixin, CustomerRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tiket
    form_class = TiketForm
    template_name = 'waterpark/customer/tikets/buy_tikets.html'
    success_url = reverse_lazy('waterpark:customer-tiket-list')
    success_message = 'Now you got the tiket, enjoy your journey to WaterLand'
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.customer = self.request.user
        if Tiket.objects.filter(customer=self.request.user, validity_day=self.object.validity_day):
            self.tiket_already_taken()
            return self.form_invalid(form)
        else:
            self.object.save()
            return super().form_valid(form)

    def tiket_already_taken(self):
        messages.warning(self.request, 'You already got a ticket for this date!')

    def form_invalid(self, form):
        return super().form_invalid(form)


class CustomerBuySeasonPassView(LoginRequiredMixin, CustomerRequiredMixin, SuccessMessageMixin, CreateView):
    model = SeasonPass
    form_class = SeasonPassForm
    template_name = 'waterpark/customer/seasonpass/buy_seasonpass.html'
    success_url = reverse_lazy('waterpark:customer-seasonpass-list')
    success_message = 'Now you got the SeasonPass, enjoy all the season to WaterLand'
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.customer = self.request.user
        if SeasonPass.objects.filter(customer=self.request.user, validity_from__year=date.today().year):
            return self.form_invalid(form)
        else:
            self.object.save()
            return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'You already got the season pass for this year!')
        return super().form_invalid(form)


class CustomerTiketListView(LoginRequiredMixin, CustomerRequiredMixin, ListView):
    model = Tiket
    template_name = 'waterpark/customer/tikets/my_tiket_list.html'
    context_object_name = "tiket_list"  # default is object_list
    paginate_by = 1
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        queryset = Tiket.objects.filter(customer=self.request.user).order_by('-validity_day').values()   # DESC date, default ASC
        return queryset


class CustomerSeasonPassListView(LoginRequiredMixin, CustomerRequiredMixin, ListView):
    model = SeasonPass
    template_name = 'waterpark/customer/seasonpass/my_seasonpass_list.html'
    context_object_name = "seasonpass_list"  # default is object_list
    paginate_by = 1
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        queryset = SeasonPass.objects.filter(customer=self.request.user).order_by('-date_of_purchase').values()
        return queryset

# Staff View


class StaffManageTiketMainView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'waterpark/staff/manage_tiket_menu.html'
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'


class StaffManageSeasonpassMainView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'waterpark/staff/manage_seasonpass_menu.html'
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'

# Search actions view


class SearchTiketByDateListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Tiket
    template_name = 'waterpark/staff/staff_search_tiket_list.html'
    context_object_name = "tiket_list"  # default is object_list
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        dateform = self.request.GET.get('dateform')
        tiket_list = Tiket.objects.filter(validity_day=dateform)
        messages.success(self.request, 'Results for {} date'.format(dateform))
        return tiket_list


class SearchTiketByYearListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Tiket
    template_name = 'waterpark/staff/staff_search_tiket_list.html'
    context_object_name = "tiket_list"  # default is object_list
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        yearform = self.request.GET.get('yearform')
        tiket_list = Tiket.objects.filter(validity_day__year=yearform).order_by('validity_day')
        messages.success(self.request, 'Results for {} year'.format(yearform))
        return tiket_list


class SearchTiketByRangeListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Tiket
    template_name = 'waterpark/staff/staff_search_tiket_list.html'
    context_object_name = "tiket_list"  # default is object_list
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        dateminform = self.request.GET.get('dateminform')
        datemaxform = self.request.GET.get('datemaxform')
        if dateminform < datemaxform:
            tiket_list = Tiket.objects.filter(validity_day__range=[dateminform, datemaxform]).order_by('validity_day')
            messages.success(self.request, 'Results for {} to {} range'.format(dateminform, datemaxform))
        else:
            tiket_list = None
            messages.warning(self.request, 'Wrong date range detected! no resultus to display')
        return tiket_list


class SearchSeasonpassByYearListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = SeasonPass
    template_name = 'waterpark/staff/staff_search_seasonpass_list.html'
    context_object_name = "seasonpass_list"  # default is object_list
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        yearform = self.request.GET.get('yearform')
        seasonpass_list = SeasonPass.objects.filter(validity_from__year=yearform)
        messages.success(self.request, 'Results for {} year'.format(yearform))
        return seasonpass_list


class SearchCustomerTiketView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'waterpark/staff/detail/staff_dtiket_form.html'
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'


class SearchCustomerSeasonpassView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'waterpark/staff/detail/staff_dseasonpass_form.html'
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'


class SearchCustomerTiketListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Tiket
    template_name = 'waterpark/staff/detail/staff_tiket_detail.html'
    context_object_name = "tiket_list"  # default is object_list
    paginate_by = 3
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        nameform = self.request.GET.get('nameform')
        tiket_list = Tiket.objects.filter(customer__username=nameform).order_by('-validity_day')
        if tiket_list.count():
            if 'page' not in self.request.GET.keys():
                messages.success(self.request, 'Tikets found for {} customer'.format(nameform))
        else:
            messages.warning(self.request, 'No results for {} customer'.format(nameform))
        return tiket_list


class SearchCustomerSeasonpassListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = SeasonPass
    template_name = 'waterpark/staff/detail/staff_seasonpass_detail.html'
    context_object_name = "seasonpass_list"  # default is object_list
    paginate_by = 1
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        nameform = self.request.GET.get('nameform')
        tiket_list = SeasonPass.objects.filter(customer__username=nameform).order_by('-validity_from')
        if tiket_list.count():
            if 'page' not in self.request.GET.keys():
                messages.success(self.request, 'SeasonPass found for {} customer'.format(nameform))
        else:
            messages.warning(self.request, 'No results for {} customer'.format(nameform))
        return tiket_list


class GetTiketTodayView(LoginRequiredMixin, CustomerRequiredMixin, ListView):
    model = Tiket
    template_name = 'waterpark/customer/tikets/my_tiket_list.html'
    context_object_name = "tiket_list"  # default is object_list
    paginate_by = 1
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        queryset = Tiket.objects.filter(customer=self.request.user, validity_day=date.today())
        if queryset.count():
            messages.success(self.request, 'You got the ticket today! Enjoy your day to Waterland')
        else:
            messages.warning(self.request,
                             'No ticket found, you should buy the ticket today if you wanna come to Waterland')
        return queryset


class GetTiketTodayStaffView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Tiket
    template_name = 'waterpark/staff/detail/staff_tiket_detail.html'
    context_object_name = "tiket_list"  # default is object_list
    paginate_by = 1
    login_url = 'userpark:login'  # Redirect Login needed
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        nameform = self.request.GET.get('nameform')
        queryset = Tiket.objects.filter(customer__username=nameform, validity_day=date.today())
        if queryset.count():
            messages.success(self.request, '({}) Ticket found for today'.format(nameform))
        else:
            messages.warning(self.request, '({}) No ticket found for today'.format(nameform))
        return queryset
