"""Tests of api views associated with playlist functionality."""
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status

from tests.util import create_test_user
from main.models import Playlist, MediaLink, PlaylistElement


class PlaylistViewGetTests(APITestCase):
    """Tests for PlaylistView GET requests"""

    # docstr-coverage:inherited
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("api-playlist")
        cls.user = create_test_user()
        cls.playlist = Playlist.objects.create(name="test_playlist", added_by=cls.user)
        cls.media_link_1 = MediaLink.objects.create(
            source="test.url", added_by=cls.user
        )
        cls.media_link_2 = MediaLink.objects.create(
            source="test.url2", added_by=cls.user
        )

    def test_get_response_fields(self):
        """Playlist view GET request response has correct fields."""
        response = self.make_request()
        self.assertIn("name", response.data[0])
        self.assertIn("url", response.data[0])
        self.assertIn("added_by", response.data[0])
        self.assertIn("length", response.data[0])

    def test_get_response_field_order(self):
        """
        Playlist view GET request response fields have the correct
        order.
        """
        response = self.make_request()
        field_order = tuple(response.data[0])
        self.assertEqual(field_order, ("url", "name", "added_by", "length"))

    def test_get_response_includes_all_elements(self):
        """Playlist view GET request response lists all playlists."""
        self.add_to_playlist(self.media_link_1, 0)
        response = self.make_request()
        self.assertEqual(response.data[0]["length"], 1)
        self.add_to_playlist(self.media_link_1, 1)
        response = self.make_request()
        self.assertEqual(response.data[0]["length"], 2)

    def add_to_playlist(self, media_link, position):
        """Add a MediaLink to the test playlist.

        Parameters
        ----------
        media_link : MediaLink
            MediaLink to be added.
        position : int
            Position in the playlist at which the MediaLink will be
            inserted
        """
        self.playlist.elements.create(media_link=media_link, position=position)

    def make_request(self):
        """Send a GET request to PlaylistView

        Returns
        -------
        rest_framework.response.Response
            The response to the request.
        """
        return self.client.get(self.url)


class PlaylistViewPostTests(APITestCase):
    """Tests for PlaylistView POST requests"""

    # docstr-coverage:inherited
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("api-playlist")
        cls.username = "test_user"
        cls.password = "test_pass"
        cls.user = create_test_user(cls.username, cls.password)

    def test_post_authenticated_response_code(self):
        """An authenticated POST request response code is correct."""
        self.client.login(username=self.username, password=self.password)
        response = self.make_request(dict(name="test_playlist"))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_creates_playlist(self):
        """An authenticated POST request creates a playlist."""
        self.client.login(username=self.username, password=self.password)
        self.make_request(dict(name="test_playlist"))

        self.assertTrue(Playlist.objects.filter(name="test_playlist").exists())

    def test_post_unauthenticated_response_code(self):
        """An unauthenticated POST request response code is correct."""
        response = self.make_request(dict(name="test_playlist"))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_unauthenticated_doesnt_create_playlist(self):
        """An unauthenticated POST request doesn't create a playlist."""
        self.make_request(dict(name="test_playlist"))

        self.assertFalse(Playlist.objects.filter(name="test_playlist").exists())

    def make_request(self, data=None):
        """Send a POST request to PlaylistView

        Parameters
        ----------
        data : dict
            Data to be sent with the request.

        Returns
        -------
        rest_framework.response.Response
            The response to the request.
        """
        return self.client.post(self.url, data=data)


class PlaylistDetailViewTests(APITestCase):
    """Tests for PlaylistDetailView requests"""

    # docstr-coverage:inherited
    @classmethod
    def setUpTestData(cls):
        cls.view_name = "api-playlist-detail"
        cls.user = create_test_user()
        cls.playlist = Playlist.objects.create(name="test_playlist", added_by=cls.user)
        cls.media_link_1 = MediaLink.objects.create(
            source="test.url", added_by=cls.user
        )

    def test_get_playlist_detail_fields(self):
        """Playlist detailed view has correct fields."""
        response = self.client.get(reverse(self.view_name, args=[self.playlist.pk]))
        self.assertIn("id", response.data)
        self.assertIn("name", response.data)
        self.assertIn("added_by", response.data)
        self.assertIn("length", response.data)
        self.assertIn("elements", response.data)

    def test_get_playlist_detail_field_order(self):
        """Playlist detailed view response has correct field order."""
        response = self.client.get(reverse(self.view_name, args=[self.playlist.pk]))
        field_order = tuple(response.data)
        self.assertEqual(field_order, ("id", "name", "added_by", "length", "elements"))

    def test_get_playlist_detail_element_fields(self):
        """Playlists elements have correct fields."""
        self.playlist.elements.create(position=0, media_link=self.media_link_1)
        response = self.client.get(reverse(self.view_name, args=[self.playlist.pk]))
        self.assertIn("position", response.data["elements"][0])
        self.assertIn("source", response.data["elements"][0])
        self.assertIn("url", response.data["elements"][0])

    def test_get_playlist_detail__element_field_order(self):
        """Playlists elements have correct field order."""
        self.playlist.elements.create(position=0, media_link=self.media_link_1)
        response = self.client.get(reverse(self.view_name, args=[self.playlist.pk]))
        field_order = tuple(response.data["elements"][0])
        self.assertEqual(field_order, ("url", "position", "source"))

    def test_get_playlist_detail_status_code(self):
        """
        Playlist detail view GET request response status code is
        correct.
        """
        response = self.client.get(reverse(self.view_name, args=[self.playlist.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_playlist_detail(self):
        """Playlist detail view DELETE request deletes the playlist."""
        self.client.delete(reverse(self.view_name, args=[self.playlist.pk]))

        self.assertFalse(Playlist.objects.filter(name="test_playlist").exists())

    def test_delete_playlist_detail_status_code(self):
        """
        Playlist detail view DELETE request response status code is
        correct.
        """
        response = self.client.delete(reverse(self.view_name, args=[self.playlist.pk]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_put_playlist_detail(self):
        """Playlist detail view PUT request updates playlist."""
        self.client.put(
            reverse(self.view_name, args=[self.playlist.pk]), data={"name": "new_name"}
        )

        self.playlist.refresh_from_db()
        self.assertEqual(self.playlist.name, "new_name")

    def test_put_playlist_detail_status_code(self):
        """
        Playlist detail view PUT request response status code is
        correct.
        """
        response = self.client.put(
            reverse(self.view_name, args=[self.playlist.pk]), data={"name": "new_name"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MediaLinkViewGetTests(APITestCase):
    """Tests for MediaLinkView GET requests"""

    # docstr-coverage:inherited
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("api-media_link")
        cls.user = create_test_user()
        cls.media_link_1 = MediaLink.objects.create(
            source="test.url", added_by=cls.user
        )
        cls.media_link_2 = MediaLink.objects.create(
            source="test.url2", added_by=cls.user
        )

    def test_get_response_media_link_fields(self):
        """MediaLink view GET request response has correct fields."""
        response = self.make_request()
        self.assertIn("url", response.data[0])
        self.assertIn("source", response.data[0])
        self.assertIn("added_by", response.data[0])

    def test_get_response_lists_all(self):
        """MediaLink GET request response contains all media_links."""
        response = self.make_request()
        self.assertEqual(len(response.data), 2)

    def make_request(self):
        """Send a GET request to MediaLinkView.

        Returns
        -------
        rest_framework.response.Response
            The response to the request.
        """
        return self.client.get(self.url)


class MediaLinkPostTests(APITestCase):
    """Tests for MediaLinkView POST requests"""

    # docstr-coverage:inherited
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("api-media_link")
        cls.username = "test_user"
        cls.password = "test_pass"
        cls.user = create_test_user(cls.username, cls.password)

    def test_post_authenticated_response_code(self):
        """
        An authenticated POST request to media link view returns with
        correct status code.
        """
        self.client.login(username=self.username, password=self.password)
        response = self.make_request(dict(source="test.url"))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_creates_media_link(self):
        """
        A POST request to media link view creates a new MediaLink entry.
        """
        self.client.login(username=self.username, password=self.password)
        self.make_request(dict(source="test.url"))

        self.assertTrue(MediaLink.objects.filter(source="test.url").exists())

    def test_post_unauthenticated_response_code(self):
        """
        An unauthenticated POST request to media link view returns with
        correct status code.
        """
        response = self.make_request(dict(source="test.url"))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_unauthenticated_doesnt_create_media_link(self):
        """
        An unauthenticated POST request to media link view doesn't
        create a new MediaLink entry.
        """
        self.make_request(dict(source="test.url"))

        self.assertFalse(MediaLink.objects.filter(source="test.url").exists())

    def make_request(self, data=None):
        """Send a POST request to MediaLinkView

        Parameters
        ----------
        data : dict
            Data to be sent with the request.

        Returns
        -------
        rest_framework.response.Response
            The response to the request.
        """
        return self.client.post(self.url, data=data)


class MediaLinkDetailViewTests(APITestCase):
    """Tests for MediaLinkDetailView requests"""

    # docstr-coverage:inherited
    @classmethod
    def setUpTestData(cls):
        cls.view_name = "api-media_link-detail"
        cls.user = create_test_user()
        cls.media_link_1 = MediaLink.objects.create(
            source="test.url", added_by=cls.user
        )

    def test_get_media_link_detail_fields(self):
        """
        MediaLink detail view GET request response has correct fields.
        """
        response = self.client.get(reverse(self.view_name, args=[self.media_link_1.pk]))
        self.assertIn("source", response.data)
        self.assertIn("added_by", response.data)
        self.assertIn("playlists", response.data)

    def test_get_media_link_playlists_field(self):
        """
        MediaLink detail view GET request response playlist listing
        has correct fields.
        """

        playlist = Playlist.objects.create(name="test_playlist", added_by=self.user)
        PlaylistElement.objects.create(
            playlist=playlist, position=0, media_link=self.media_link_1
        )
        response = self.client.get(reverse(self.view_name, args=[self.media_link_1.pk]))
        self.assertIn("url", response.data["playlists"][0])
        self.assertIn("position", response.data["playlists"][0])

    def test_get_media_link_detail_status_code(self):
        """
        MediaLink detail view GET request response status code is
        correct.
        """
        response = self.client.get(reverse(self.view_name, args=[self.media_link_1.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_media_link_detail(self):
        """
        MediaLink detail view DELETE request deletes MediaLink entry."""
        self.client.delete(reverse(self.view_name, args=[self.media_link_1.pk]))

        self.assertFalse(MediaLink.objects.filter(pk=self.media_link_1.pk).exists())

    def test_delete_media_link_detail_status_code(self):
        """
        MediaLink detail view DELETE request response status code is
        correct.
        """
        response = self.client.delete(
            reverse(self.view_name, args=[self.media_link_1.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_put_media_link_detail(self):
        """MediaLink detail view PUT request updates MediaLink entry."""
        self.client.put(
            reverse(self.view_name, args=[self.media_link_1.pk]),
            data={"source": "new_url"},
        )

        self.media_link_1.refresh_from_db()
        self.assertEqual(self.media_link_1.source, "new_url")

    def test_put_media_link_detail_status_code(self):
        """
        MediaLink detail view PUT request response status code is
        correct.
        """
        response = self.client.put(
            reverse(self.view_name, args=[self.media_link_1.pk]),
            data={"source": "new_url"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
