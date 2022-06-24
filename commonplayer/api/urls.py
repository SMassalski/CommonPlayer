from django.urls import path

from .views import NavigateView, ControlView


urlpatterns = [
    path('play/', NavigateView.as_view(), name='api-play'),
    path('command/', ControlView.as_view(), name='api-control')
]
