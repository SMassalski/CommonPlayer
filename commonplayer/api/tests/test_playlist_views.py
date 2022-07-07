from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status

from tests.util import create_test_user
from main.models import Playlist, MediaLink


class PlaylistViewGetTests(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('api-playlist')
        cls.user = create_test_user()
        cls.playlist = Playlist.objects.create(name='test_playlist',
                                               added_by=cls.user)
        cls.media_link_1 = MediaLink.objects.create(source='test.url',
                                                    added_by=cls.user)
        cls.media_link_2 = MediaLink.objects.create(source='test.url2',
                                                    added_by=cls.user)
        
    def test_get_response_includes_name(self):
        response = self.make_request()
        name = response.data[0]['name']
        self.assertEqual(name, 'test_playlist')
    
    def test_get_response_includes_all_elements(self):
        self.add_to_playlist(self.media_link_1, 0)
        response = self.make_request()
        self.assertEqual(len(response.data[0]['elements']), 1)
        self.add_to_playlist(self.media_link_1, 1)
        response = self.make_request()
        self.assertEqual(len(response.data[0]['elements']), 2)
        
    def test_get_response_media_link_representation(self):
        self.add_to_playlist(self.media_link_1, 0)
        response = self.make_request()
        media_link_dict = response.data[0]['elements'][0]['media_link']
        self.assertIn('url', media_link_dict)
        self.assertIn('added_by', media_link_dict)
        
    def test_get_response_playlist_element_representation(self):
        self.add_to_playlist(self.media_link_1, 0)
        response = self.make_request()
        element_dict = response.data[0]['elements'][0]
        self.assertIn('position', element_dict)
        self.assertIn('media_link', element_dict)
        
    def add_to_playlist(self, media_link, position):
        self.playlist.elements.create(media_link=media_link, position=position)
        
    def make_request(self):
        return self.client.get(self.url)


class PlaylistViewPostTests(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('api-playlist')
        cls.username = 'test_user'
        cls.password = 'test_pass'
        cls.user = create_test_user(cls.username, cls.password)

    def test_post_authenticated_response_code(self):
        self.client.login(username=self.username, password=self.password)
        response = self.make_request(dict(name='test_playlist'))
    
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_post_creates_playlist(self):
        self.client.login(username=self.username, password=self.password)
        self.make_request(dict(name='test_playlist'))
    
        self.assertTrue(
            Playlist.objects.filter(name='test_playlist').exists()
        )

    def test_post_unauthenticated_response_code(self):
        response = self.make_request(dict(name='test_playlist'))
    
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_unauthenticated_doesnt_create_playlist(self):
        self.make_request(dict(name='test_playlist'))
    
        self.assertFalse(
            Playlist.objects.filter(name='test_playlist').exists()
        )
    
    def make_request(self, data=None):
        return self.client.post(self.url, data=data)
    
    
class PlaylistDetailViewTests(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.view_name = 'api-playlist-detail'
        cls.user = create_test_user()
        cls.playlist = Playlist.objects.create(name='test_playlist',
                                               added_by=cls.user)
        cls.media_link_1 = MediaLink.objects.create(source='test.url',
                                                    added_by=cls.user)

    def test_get_playlist_detail_fields(self):
        response = self.client.get(reverse(self.view_name,
                                           args=[self.playlist.pk]))
        self.assertIn('id', response.data)
        self.assertIn('name', response.data)
        self.assertIn('added_by', response.data)
        self.assertIn('elements', response.data)

    def test_get_playlist_detail_element_fields(self):
        self.playlist.elements.create(position=0, media_link=self.media_link_1)
        response = self.client.get(reverse(self.view_name,
                                           args=[self.playlist.pk]))
        self.assertIn('position', response.data['elements'][0])
        self.assertIn('media_link', response.data['elements'][0])
        self.assertIn('source', response.data['elements'][0]['media_link'])
        self.assertIn('added_by', response.data['elements'][0]['media_link'])
        
    def test_get_playlist_detail_status_code(self):
        response = self.client.get(reverse(self.view_name,
                                           args=[self.playlist.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_delete_playlist_detail(self):
        self.client.delete(reverse(self.view_name, args=[self.playlist.pk]))

        self.assertFalse(
            Playlist.objects.filter(name='test_playlist').exists()
        )
        
    def test_delete_playlist_detail_status_code(self):
        response = self.client.delete(reverse(self.view_name,
                                              args=[self.playlist.pk]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_put_playlist_detail(self):
        self.client.put(reverse(self.view_name, args=[self.playlist.pk]),
                        data={'name': 'new_name'})
        
        self.playlist.refresh_from_db()
        self.assertEqual(self.playlist.name, 'new_name')

    def test_put_playlist_detail_status_code(self):
        response = self.client\
            .put(reverse(self.view_name, args=[self.playlist.pk]),
                 data={'name': 'new_name'})
    
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MediaLinkViewGetTests(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('api-media_link')
        cls.user = create_test_user()
        cls.media_link_1 = MediaLink.objects.create(source='test.url',
                                                    added_by=cls.user)
        cls.media_link_2 = MediaLink.objects.create(source='test.url2',
                                                    added_by=cls.user)
    
    def test_get_response_media_link_fields(self):
        response = self.make_request()
        self.assertIn('source', response.data[0])
        self.assertIn('added_by', response.data[0])
    
    def test_get_response_lists_all(self):
        response = self.make_request()
        self.assertEqual(len(response.data), 2)

    def make_request(self):
        return self.client.get(self.url)


class MediaLinkPostTests(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('api-media_link')
        cls.username = 'test_user'
        cls.password = 'test_pass'
        cls.user = create_test_user(cls.username, cls.password)
    
    def test_post_authenticated_response_code(self):
        self.client.login(username=self.username, password=self.password)
        response = self.make_request(dict(source='test.url'))
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_post_creates_media_link(self):
        self.client.login(username=self.username, password=self.password)
        self.make_request(dict(source='test.url'))
        
        self.assertTrue(
            MediaLink.objects.filter(source='test.url').exists()
        )
    
    def test_post_unauthenticated_response_code(self):
        response = self.make_request(dict(source='test.url'))
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_post_unauthenticated_doesnt_create_media_link(self):
        self.make_request(dict(source='test.url'))
        
        self.assertFalse(
            MediaLink.objects.filter(source='test.url').exists()
        )
    
    def make_request(self, data=None):
        return self.client.post(self.url, data=data)


class MediaLinkDetailViewTests(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.view_name = 'api-media_link-detail'
        cls.user = create_test_user()
        cls.media_link_1 = MediaLink.objects.create(source='test.url',
                                                    added_by=cls.user)
    
    def test_get_playlist_detail_fields(self):
        response = self.client.get(reverse(self.view_name,
                                           args=[self.media_link_1.pk]))
        self.assertIn('source', response.data)
        self.assertIn('added_by', response.data)
    
    def test_get_playlist_detail_status_code(self):
        response = self.client.get(reverse(self.view_name,
                                           args=[self.media_link_1.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_playlist_detail(self):
        self.client.delete(reverse(self.view_name,
                                   args=[self.media_link_1.pk]))
        
        self.assertFalse(
            MediaLink.objects.filter(pk=self.media_link_1.pk).exists()
        )
    
    def test_delete_media_link_detail_status_code(self):
        response = self.client.delete(reverse(self.view_name,
                                              args=[self.media_link_1.pk]))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_put_media_link_detail(self):
        self.client.put(reverse(self.view_name, args=[self.media_link_1.pk]),
                        data={'source': 'new_url'})
        
        self.media_link_1.refresh_from_db()
        self.assertEqual(self.media_link_1.source, 'new_url')
    
    def test_put_media_link_detail_status_code(self):
        response = self.client \
            .put(reverse(self.view_name, args=[self.media_link_1.pk]),
                 data={'source': 'new_url'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
