from django.urls import path

from .views import browser_views, playlist_views


urlpatterns = [
    
    # Browser views
    path('nav/', browser_views.NavigateView.as_view(), name='api-nav'),
    path('window/', browser_views.LifecycleView.as_view(),
         name='api-lifecycle'),
    path('control/', browser_views.ControlView.as_view(), name='api-control'),
    
    # Playlist views
    path('playlists/', playlist_views.PlaylistView.as_view(),
         name='api-playlist'),
    path('playlists/<int:pk>', playlist_views.PlaylistDetailView.as_view(),
         name='api-playlist-detail'),
    path('media_links/', playlist_views.MediaLinkView.as_view(),
         name='api-media_link'),
    path('media_links/<int:pk>', playlist_views.MediaLinkDetailView.as_view(),
         name='api-media_link-detail'),
]
