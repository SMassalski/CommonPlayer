from rest_framework import serializers

from .client import BrowserClient
from main.models import Playlist, PlaylistElement, MediaLink


class CommandSerializer(serializers.Serializer):
    """Serializer for browser lifecycle commands
    
    Fields:
    - Command: Command to be issued
    """
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    COMMAND_CHOICES = [
        (BrowserClient.START, 'Start'),
        (BrowserClient.EXIT, 'End'),
    ]
    command = serializers.ChoiceField(choices=COMMAND_CHOICES)
    

class NavigateSerializer(serializers.Serializer):
    """Serializer for browser navigation commands
    
    Fields:
    - url: The url the browser is to navigate to.
    """
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    url = serializers.CharField(max_length=128)


class ControlSerializer(serializers.Serializer):
    """Serializer for media controller commands

    Fields:
    - value: action to be performed by the controller.
    """
    
    def update(self, instance, validated_data):
        pass
    
    def create(self, validated_data):
        pass

    ACTION_CHOICES = [
        (BrowserClient.PLAY_PAUSE, 'Play / Pause'),
        (BrowserClient.AUTOPLAY, 'Autoplay'),
        (BrowserClient.FULLSCREEN, 'Fullscreen'),
        (BrowserClient.SUBTITLES, 'Subtitles'),
        (BrowserClient.HANDLE_COOKIE_POPUP, 'Accept cookies')
    ]
    action = serializers.ChoiceField(choices=ACTION_CHOICES)
    

# TODO: Two PlaylistElement serializers for different directions
#   (From MediaLink and Playlist)
#   + Hyperlinked relations


class MediaLinkSerializer(serializers.ModelSerializer):
    
    added_by = serializers.CharField(source='added_by.username',
                                     read_only=True)
    
    class Meta:
        model = MediaLink
        fields = ['source', 'added_by']


class PlaylistElementSerializer(serializers.HyperlinkedModelSerializer):
    media_link = MediaLinkSerializer(read_only=True)
    
    class Meta:
        model = PlaylistElement
        fields = ['position', 'media_link']


class PlaylistSerializer(serializers.HyperlinkedModelSerializer):
    elements = PlaylistElementSerializer(many=True, read_only=True)
    added_by = serializers.CharField(source='added_by.username',
                                     read_only=True)
    
    class Meta:
        model = Playlist
        fields = ['id', 'name', 'added_by', 'elements']
        depth = 2
