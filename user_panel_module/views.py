from django.shortcuts import render
from django.views.generic import TemplateView, View, DetailView
from account_module.models import User
from .forms import EditProfileStudModelForm


# Create your views here.

class UserPanelDashboardView(TemplateView):
    template_name = 'user_panel_module/user_panel_dashboard_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.kwargs['pk'] == self.request.user.id:
            context['current_user'] = User.objects.filter(id=self.request.user.id).first()
        else:
            context['second_user'] = User.objects.filter(id=self.kwargs['pk']).first()
        return context


#class UserProfileView(DetailView):
#    model = User
#    template_name = 'user_panel_module/user_profile_view.html'
#    context_object_name = 'user'

#    def get_queryset(self):
#        query = User.objects.filter(pk=self.kwargs['pk'])
#        return query




