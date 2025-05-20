from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.


class HomePageView(TemplateView):
    template_name = 'home_module/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['current_user'] = self.request.user
        return context

#def site_footer_component(request):
#    return render(request, 'shared/site_footer_component.html')

def site_header_component(request):
    context = {
        'current_user': request.user,
    }

    return render(request, 'shared/site_header_component.html', context)
