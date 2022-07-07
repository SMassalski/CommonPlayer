from django.test import TestCase
from django.test.utils import tag

from main.models import Playlist, MediaLink, PlaylistElement
from tests.util import create_test_user


class PlaylistTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        user = create_test_user()
        cls.user = user
        cls.media_link_1 = MediaLink(source='example.url', added_by=user)
        cls.media_link_1.save()
        cls.media_link_2 = MediaLink(source='example2.url', added_by=user)
        cls.media_link_2.save()
        
    def setUp(self) -> None:
        
        # Retrieve django tags
        method = getattr(self, self._testMethodName)
        tags = getattr(method, 'tags', {})
        
        self.playlist = Playlist(name='test_playlist', added_by=self.user)
        self.playlist.save()
        if 'setup_empty_playlist' in tags:
            return
        self.playlist.elements.create(media_link=self.media_link_1, position=0)
        self.playlist.elements.create(media_link=self.media_link_2, position=1)
        
    def test_add_media_at_beginning(self):

        media_link = MediaLink(source='test.url', added_by=self.user)
        media_link.save()
        self.playlist.add_media_at(media_link, 0)

        # Added
        self.assertEqual(self.playlist.elements.get(position=0).media_link.pk,
                         media_link.pk)
        
        # Old
        self.assertEqual(self.playlist.elements.get(position=1).media_link.pk,
                         self.media_link_1.pk)
        self.assertEqual(self.playlist.elements.get(position=2).media_link.pk,
                         self.media_link_2.pk)
        
    def test_add_media_at_the_end(self):
        media_link = MediaLink(source='test.url', added_by=self.user)
        media_link.save()
        self.playlist.add_media_at(media_link, None)

        # Added
        self.assertEqual(self.playlist.elements.get(position=2).media_link.pk,
                         media_link.pk)
        
        # Old
        self.assertEqual(self.playlist.elements.get(position=0).media_link.pk,
                         self.media_link_1.pk)
        self.assertEqual(self.playlist.elements.get(position=1).media_link.pk,
                         self.media_link_2.pk)

    def test_add_media_in_the_middle(self):
        media_link = MediaLink(source='test.url', added_by=self.user)
        media_link.save()
        self.playlist.add_media_at(media_link, 1)
    
        # Added
        self.assertEqual(self.playlist.elements.get(position=1).media_link.pk,
                         media_link.pk)
    
        # Old
        self.assertEqual(self.playlist.elements.get(position=0).media_link.pk,
                         self.media_link_1.pk)
        self.assertEqual(self.playlist.elements.get(position=2).media_link.pk,
                         self.media_link_2.pk)

    @tag('setup_empty_playlist')
    def test_add_media_to_empty(self):
        media_link = MediaLink(source='test.url', added_by=self.user)
        media_link.save()
        self.playlist.add_media_at(media_link)
    
        self.assertEqual(self.playlist.elements.get(position=0).media_link.pk,
                         media_link.pk)
        
    
class MediaLinkTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        user = create_test_user()
        cls.user = user
        cls.media_link_1 = MediaLink(source='example.url', added_by=user)
        cls.media_link_1.save()
        cls.media_link_2 = MediaLink(source='example2.url', added_by=user)
        cls.media_link_2.save()
        
    def setUp(self) -> None:
        # Retrieve django tags
        method = getattr(self, self._testMethodName)
        tags = getattr(method, 'tags', {})
    
        self.playlist = Playlist(name='test_playlist', added_by=self.user)
        self.playlist.save()
        if 'setup_empty_playlist' in tags:
            return
        self.playlist.elements.create(media_link=self.media_link_1, position=0)
        self.playlist.elements.create(media_link=self.media_link_2, position=1)

    def test_add_media_at_beginning(self):
        media_link = MediaLink(source='test.url', added_by=self.user)
        media_link.save()
        media_link.add_to_playlist(self.playlist, 0)
    
        # Added
        self.assertEqual(self.playlist.elements.get(position=0).media_link.pk,
                         media_link.pk)
    
        # Old
        self.assertEqual(self.playlist.elements.get(position=1).media_link.pk,
                         self.media_link_1.pk)
        self.assertEqual(self.playlist.elements.get(position=2).media_link.pk,
                         self.media_link_2.pk)

    def test_add_media_at_the_end(self):
        media_link = MediaLink(source='test.url', added_by=self.user)
        media_link.save()
        media_link.add_to_playlist(self.playlist, None)
    
        # Added
        self.assertEqual(self.playlist.elements.get(position=2).media_link.pk,
                         media_link.pk)
    
        # Old
        self.assertEqual(self.playlist.elements.get(position=0).media_link.pk,
                         self.media_link_1.pk)
        self.assertEqual(self.playlist.elements.get(position=1).media_link.pk,
                         self.media_link_2.pk)

    def test_add_media_in_the_middle(self):
        media_link = MediaLink(source='test.url', added_by=self.user)
        media_link.save()
        media_link.add_to_playlist(self.playlist, 1)
    
        # Added
        self.assertEqual(self.playlist.elements.get(position=1).media_link.pk,
                         media_link.pk)
    
        # Old
        self.assertEqual(self.playlist.elements.get(position=0).media_link.pk,
                         self.media_link_1.pk)
        self.assertEqual(self.playlist.elements.get(position=2).media_link.pk,
                         self.media_link_2.pk)

    @tag('setup_empty_playlist')
    def test_add_media_to_empty(self):
        media_link = MediaLink(source='test.url', added_by=self.user)
        media_link.save()
        media_link.add_to_playlist(self.playlist)
    
        self.assertEqual(self.playlist.elements.get(position=0).media_link.pk,
                         media_link.pk)
        
        
class PlaylistElementSaveTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        user = create_test_user()
        cls.user = user
        cls.media_link_1 = MediaLink(source='example.url', added_by=user)
        cls.media_link_1.save()
        cls.playlist = Playlist(name='test_playlist', added_by=user)
        cls.playlist.save()
        
    def test_save_to_empty_playlist(self):
        playlist_element = PlaylistElement(playlist=self.playlist,
                                           media_link=self.media_link_1,
                                           position=0)
        playlist_element.save()
        db_playlist_element = PlaylistElement.objects\
            .get(pk=playlist_element.pk)
        self.assertIsNotNone(db_playlist_element)
    
    def test_save_same_element_at_the_same_position(self):
        playlist_element = PlaylistElement(playlist=self.playlist,
                                           media_link=self.media_link_1,
                                           position=0)
        playlist_element.save()
        media_link = MediaLink(source='test.url', added_by=self.user)
        media_link.save()
        playlist_element.media_link = media_link
        playlist_element.save()
        playlist_element = PlaylistElement.objects \
            .get(pk=playlist_element.pk)
        self.assertEqual(playlist_element.media_link.pk, media_link.pk)

    def test_save_different_element_at_the_same_position(self):
        playlist_element = PlaylistElement(playlist=self.playlist,
                                           media_link=self.media_link_1,
                                           position=0)
        playlist_element.save()
        media_link = MediaLink(source='test.url', added_by=self.user)
        media_link.save()
        playlist_element = PlaylistElement(playlist=self.playlist,
                                           media_link=media_link,
                                           position=0)
        with self.assertWarns(UserWarning):
            playlist_element.save()
        self.assertIsNone(playlist_element.pk)
            
    def test_save_warns_not_saved(self):
        playlist_element = PlaylistElement(playlist=self.playlist,
                                           media_link=self.media_link_1,
                                           position=0)
        playlist_element.save()
        media_link = MediaLink(source='test.url', added_by=self.user)
        media_link.save()
        playlist_element = PlaylistElement(playlist=self.playlist,
                                           media_link=media_link,
                                           position=0)
        with self.assertWarnsRegex(UserWarning, r'not saved'):
            playlist_element.save()
            
    def test_save_warns_shows_proper_usage(self):
        playlist_element = PlaylistElement(playlist=self.playlist,
                                           media_link=self.media_link_1,
                                           position=0)
        playlist_element.save()
        media_link = MediaLink(source='test.url', added_by=self.user)
        media_link.save()
        playlist_element = PlaylistElement(playlist=self.playlist,
                                           media_link=media_link,
                                           position=0)
        msg = r'Use Playlist.add_media_at\(\) or MediaLink.add_to_playlist\(\)'
        with self.assertWarnsRegex(UserWarning, msg):
            playlist_element.save()
            
