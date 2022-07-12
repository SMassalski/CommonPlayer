from rest_framework import serializers

from .client import BrowserClient
from main.models import Playlist, PlaylistElement, MediaLink


class CommandSerializer(serializers.Serializer):
    """Serializer for browser lifecycle commands

    Fields:
        - Command: Command to be issued
    """

    # docstr-coverage:inherited
    def update(self, instance, validated_data):
        pass

    # docstr-coverage:inherited
    def create(self, validated_data):
        pass

    COMMAND_CHOICES = [
        (BrowserClient.START, "Start"),
        (BrowserClient.EXIT, "End"),
    ]
    command = serializers.ChoiceField(choices=COMMAND_CHOICES)


class NavigateSerializer(serializers.Serializer):
    """Serializer for browser navigation commands

    Fields:
        - url: The url the browser is to navigate to.
    """

    # docstr-coverage:inherited
    def update(self, instance, validated_data):
        pass

    # docstr-coverage:inherited
    def create(self, validated_data):
        pass

    url = serializers.CharField(max_length=128)


class ControlSerializer(serializers.Serializer):
    """Serializer for media controller commands

    Fields:
        - value: action to be performed by the controller.
    """

    # docstr-coverage:inherited
    def update(self, instance, validated_data):
        pass

    # docstr-coverage:inherited
    def create(self, validated_data):
        pass

    ACTION_CHOICES = [
        (BrowserClient.PLAY_PAUSE, "Play / Pause"),
        (BrowserClient.AUTOPLAY, "Autoplay"),
        (BrowserClient.FULLSCREEN, "Fullscreen"),
        (BrowserClient.SUBTITLES, "Subtitles"),
        (BrowserClient.HANDLE_COOKIE_POPUP, "Accept cookies"),
    ]
    action = serializers.ChoiceField(choices=ACTION_CHOICES)


# PlaylistElement model serializers


class FromMediaLinkElementSerializer(serializers.ModelSerializer):
    """PlaylistElement model serializer exposing Playlist information.

    Fields:
        - url: link to playlist
        - position: position of the element in playlist
    """

    url = serializers.HyperlinkedRelatedField(
        source="playlist", read_only=True, view_name="api-playlist-detail"
    )

    # docstr-coverage:inherited
    class Meta:
        model = PlaylistElement
        fields = [
            "url",
            "position",
        ]


class FromPlaylistElementSerializer(serializers.HyperlinkedModelSerializer):
    """PlaylistElement model serializer exposing MediaLink information.

    Fields:
        - url: link to MediaLink
        - position: position of the element in the playlist
        - source: MediaLink source
    """

    source = serializers.CharField(read_only=True, source="media_link.source")
    url = serializers.HyperlinkedRelatedField(
        source="media_link", read_only=True, view_name="api-media_link-detail"
    )

    # docstr-coverage:inherited
    class Meta:
        model = PlaylistElement
        fields = [
            "url",
            "position",
            "source",
        ]


# MediaLink model serializers


class MediaLinkSerializer(serializers.HyperlinkedModelSerializer):
    """MediaLink model serializer

    Fields:
        - url
        - source
        - added_by
    """

    url = serializers.HyperlinkedIdentityField(view_name="api-media_link-detail")
    added_by = serializers.CharField(source="added_by.username", read_only=True)

    # docstr-coverage:inherited
    class Meta:
        model = MediaLink
        fields = [
            "url",
            "source",
            "added_by",
        ]


class MediaLinkDetailSerializer(serializers.ModelSerializer):
    """Detailed MediaLink model serializer.

    Fields:
        - source
        - added_by
        - playlists: playlists that contain the MediaLink
    """

    added_by = serializers.CharField(source="added_by.username", read_only=True)
    playlists = FromMediaLinkElementSerializer(many=True, read_only=True)

    # docstr-coverage:inherited
    class Meta:
        model = MediaLink
        fields = ["source", "added_by", "playlists"]


# Playlist model serializers


class PlaylistSerializer(serializers.HyperlinkedModelSerializer):
    """Playlist model serializer

    Fields:
        - url
        - name
        - added_by
        - length
    """

    url = serializers.HyperlinkedIdentityField(view_name="api-playlist-detail")
    added_by = serializers.CharField(source="added_by.username", read_only=True)

    # docstr-coverage:inherited
    class Meta:
        model = Playlist
        fields = ["url", "name", "added_by", "length"]


class PlaylistDetailSerializer(serializers.ModelSerializer):
    """Detailed Playlist model serializer

    Fields:
        - id
        - name
        - added_by
        - length
        - elements
    """

    elements = FromPlaylistElementSerializer(many=True, read_only=True)
    added_by = serializers.CharField(source="added_by.username", read_only=True)

    # docstr-coverage:inherited
    class Meta:
        model = Playlist
        fields = ["id", "name", "added_by", "length", "elements"]
