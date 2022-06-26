from django.urls import path

from .views import NavigateView, LifecycleView, ControlView


urlpatterns = [
    path('nav/', NavigateView.as_view(), name='api-nav'),
    path('window/', LifecycleView.as_view(), name='api-lifecycle'),
    path('control/', ControlView.as_view(), name='api-control')
]
