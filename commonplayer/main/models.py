from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# TODO: Think of a better class name
#   + On delete playlist element position update
# FEAT: Has player verification
class MediaLink(models.Model):
    """Model representing a site that contains a media player
    
    Fields:
    
    url : str
        The sites url.
    added_by : User
        The user that added the MediaLink
        
    """
    url = models.CharField(max_length=100)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.url
    
    def add_to_playlist(self, playlist, position=None):
        """Insert the MediaLink at a given position of a playlist.
        
        Parameters
        ----------
        playlist: Playlist
            Playlist into which the MediaLink will be inserted
        position: int or None
            Position at which the MediaLink will be inserted. If None
            the MediaLink will be appended at the end of the playlist.
        """
        playlist.add_media_at(self, position=position)

    
# FEAT: Per playlist domain permissions
class Playlist(models.Model):
    """Model representing a sequence of MediaLinks."""
    name = models.CharField(max_length=100, unique=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def add_media_at(self, media_link, position=None):
        """Insert a MediaLink at a given position of the playlist.
        
        Parameters
        ----------
        media_link: MediaLink
            MediaLink to be inserted. Must be already saved to database.
        position: int or None
            Position at which the MediaLink will be inserted. If None
            the MediaLink will be appended at the end of the playlist.
        """
        
        if position is None:
            position = self.elements \
                           .aggregate(models.Max('position'))['position__max']
            position = (position or -1) + 1  # End or 0 if playlist is empty
        
        self.elements\
            .filter(position__gte=position)\
            .update(position=models.F('position') + 1)
        self.elements.create(position=position, media_link=media_link)
        
    def __str__(self):
        return self.name
        

# TODO: On delete position update
class PlaylistElement(models.Model):
    """Model storing information about MediaLinks position in a playlist.
    
    """
    position = models.PositiveSmallIntegerField()
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE,
                                 related_name='elements')
    media_link = models.ForeignKey(MediaLink, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.playlist.name} #{self.position}'
    
    class Meta:
        
        unique_together = ('playlist', 'position')
        ordering = ('playlist', 'position')
