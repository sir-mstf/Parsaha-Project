from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:pk>', views.UserPanelDashboardView.as_view(), name='user-panel-dashboard'),
    #path('user-profile/<int:pk>', views.UserProfileView.as_view(), name='user-profile'),
]
