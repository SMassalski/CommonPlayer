"""Tests of api views associated with browser control functionality."""
import sys

import mock
from django.http import QueryDict
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework.response import Response


sys.path.append("..")

START = "start"
EXIT = "exit"
GOTO = "go_to"
GET = "get_url"
CONTROL = "control"

# Media controller actions
PLAY = "play"
AUTOPLAY = "autoplay"
FULLSCREEN = "fullscreen"
SUBTITLES = "subtitles"
HANDLE_COOKIE_POPUP = "cookie"

# TODO: Mock server


@mock.patch("api.views.browser_views.BrowserClientView.send_to_browser_server")
class NavViewTests(APITestCase):
    """Navigate view tests"""

    # docstr-coverage:inherited
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse("api-nav")

    def test_get_url(self, mock_send):
        """
        GET request to NavigateView sends correct command to browser
        server.
        """
        mock_send.return_value = Response()
        self.client.get(self.url)
        mock_send.assert_called_with({"command": GET})

    def test_go_to_url(self, mock_send):
        """
        POST request to NavigateView sends correct command to browser
        server.
        """
        mock_send.return_value = Response()
        self.client.post(self.url, data=dict(url="fake_url"))
        mock_send.assert_called_with({"command": GOTO, "value": "fake_url"})


@mock.patch("api.views.browser_views.BrowserClientView.send_to_browser_server")
class LifecycleViewTests(APITestCase):
    """Lifecycle view tests"""

    # docstr-coverage:inherited
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse("api-lifecycle")

    def test_post_command(self, mock_send):
        """
        POST request to LifecycleView sends command to browser server.
        """
        mock_send.return_value = Response()
        data = dict(command="test")
        self.client.post(self.url, data=data)
        q_dict = QueryDict("", mutable=True)
        q_dict.update(data)
        mock_send.assert_called_with(q_dict)


@mock.patch("api.views.browser_views.BrowserClientView.send_to_browser_server")
class ControlViewTests(APITestCase):
    """Control view tests"""

    # docstr-coverage:inherited
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse("api-control")

    def test_post_media_action(self, mock_send):
        """
        POST request to ControlView sends control command with action
        value.
        """
        mock_send.return_value = Response()
        self.client.post(self.url, data=dict(action="test_action"))
        called_with = {"command": CONTROL, "value": "test_action"}
        mock_send.assert_called_with(called_with)
