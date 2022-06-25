from django.urls import path

from .views import NavigateView, CommandView, ControlView


urlpatterns = [
    path('play/', NavigateView.as_view(), name='api-play'),
    path('command/', CommandView.as_view(), name='api-command'),
    path('control/', ControlView.as_view(), name='api-control')
]
