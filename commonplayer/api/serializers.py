from rest_framework import serializers

from .client import BrowserClient


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
        ('con', 'Connect')
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
        (BrowserClient.PLAY, 'Play'),
        (BrowserClient.AUTOPLAY, 'Autoplay'),
        (BrowserClient.FULLSCREEN, 'Fullscreen'),
        (BrowserClient.SUBTITLES, 'Subtitles'),
        (BrowserClient.HANDLE_COOKIE_POPUP, 'Accept cookies')
    ]
    action = serializers.ChoiceField(choices=ACTION_CHOICES)
    
