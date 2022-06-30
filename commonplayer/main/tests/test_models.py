from django.test import TestCase
from django.test.utils import tag

from main.models import Playlist, MediaLink
from .util import create_test_user


class PlaylistTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        user = create_test_user()
        cls.user = user
        cls.media_link_1 = MediaLink(url='example.url', added_by=user)
        cls.media_link_1.save()
        cls.media_link_2 = MediaLink(url='example2.url', added_by=user)
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

        media_link = MediaLink(url='test.url', added_by=self.user)
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
        media_link = MediaLink(url='test.url', added_by=self.user)
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
        media_link = MediaLink(url='test.url', added_by=self.user)
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
        media_link = MediaLink(url='test.url', added_by=self.user)
        media_link.save()
        self.playlist.add_media_at(media_link)
    
        self.assertEqual(self.playlist.elements.get(position=0).media_link.pk,
                         media_link.pk)
        
    
class MediaLinkTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        user = create_test_user()
        cls.user = user
        cls.media_link_1 = MediaLink(url='example.url', added_by=user)
        cls.media_link_1.save()
        cls.media_link_2 = MediaLink(url='example2.url', added_by=user)
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
        media_link = MediaLink(url='test.url', added_by=self.user)
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
        media_link = MediaLink(url='test.url', added_by=self.user)
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
        media_link = MediaLink(url='test.url', added_by=self.user)
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
        media_link = MediaLink(url='test.url', added_by=self.user)
        media_link.save()
        media_link.add_to_playlist(self.playlist)
    
        self.assertEqual(self.playlist.elements.get(position=0).media_link.pk,
                         media_link.pk)
