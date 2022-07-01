from django.urls import path

from .views import browser_views


urlpatterns = [
    
    # Browser views
    path('nav/', browser_views.NavigateView.as_view(), name='api-nav'),
    path('window/', browser_views.LifecycleView.as_view(),
         name='api-lifecycle'),
    path('control/', browser_views.ControlView.as_view(), name='api-control'),

]
