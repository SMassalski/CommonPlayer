"""Views for controlling the browser."""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.client import BrowserClient
from api import serializers


class BrowserClientView(APIView):
    """Base class for views that interact with the browser server."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = BrowserClient()

    # TODO: Handling server failures ({'ok': False} responses)
    #   + Probably shouldn't return a response
    def send_to_browser_server(self, data):
        """Send data to the browser server.

        Parameters
        ----------
        data : dict

        Returns
        -------
        Response
            Api response generated from the browser server's response.
        """
        with self.client:
            browser_response = self.client.send(data)
        if not browser_response.get("ok"):
            return Response(browser_response, status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(browser_response)


class NavigateView(BrowserClientView):
    """Navigate to or get current url.
    https://www.youtube.com/watch?v=AvtVuHMqOOM"""

    # Added url for easy access when manually testing

    serializer_class = serializers.NavigateSerializer

    def get(self, _):
        """Get the current url of the browser."""
        data = {"command": BrowserClient.GET}
        return self.send_to_browser_server(data)

    def post(self, request):
        """Go to a url."""
        data = {
            "command": BrowserClient.GOTO,
            "value": request.data.get("url"),
        }
        return self.send_to_browser_server(data)


class LifecycleView(BrowserClientView):
    """Control the browser's lifecycle."""

    serializer_class = serializers.CommandSerializer

    def post(self, request):
        """Send a command to the server.

        Available commands:
        - Start: start a browser
        - End: close a browser
        """

        return self.send_to_browser_server(request.data)


class ControlView(BrowserClientView):
    """Issue commands to the media controller."""

    serializer_class = serializers.ControlSerializer

    def post(self, request):
        """Send a media controller command to the server.

        Available commands:
        - Play / Pause: Toggle play / pause
        - Fullscreen: Toggle fullscreen
        - Autoplay: Toggle autoplay
        - Subtitles: Toggle subtitles
        - Accept cookies: Accept cookies if popup opened. Left here in
        case automatic closing fails.
        """
        data = dict(command=BrowserClient.CONTROL)
        data["value"] = request.data.get("action")
        return self.send_to_browser_server(data)
