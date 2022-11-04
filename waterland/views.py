from django.views.generic import TemplateView


class HomeView(TemplateView):

    template_name = 'home.html'


class WaterlandParkView(TemplateView):

    template_name = 'waterland_park.html'


class AboutUsView(TemplateView):

    template_name = 'about_us.html'
