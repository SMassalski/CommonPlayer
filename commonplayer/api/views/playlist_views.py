from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from main.models import Playlist, MediaLink
from api import serializers


class PlaylistView(ListCreateAPIView):
    """List or create playlists"""
    queryset = Playlist.objects.all()
    serializer_class = serializers.PlaylistSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class PlaylistDetailView(RetrieveUpdateDestroyAPIView):
    """Show a specific playlist"""
    queryset = Playlist.objects.all()
    serializer_class = serializers.PlaylistSerializer


class MediaLinkView(ListCreateAPIView):
    """List or create MediaLinks"""
    queryset = MediaLink.objects.all()
    serializer_class = serializers.MediaLinkSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        """Create MediaLink with added_by set to user that made the
         request.
        """
        serializer.save(added_by=self.request.user)


class MediaLinkDetailView(RetrieveUpdateDestroyAPIView):
    """Show a specific MediaLink"""
    queryset = MediaLink.objects.all()
    serializer_class = serializers.MediaLinkSerializer
