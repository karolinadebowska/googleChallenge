"""A video player class."""

from .video_library import VideoLibrary
import random
import operator

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._currently_played = None
        self._paused = False
        self._playlists = {}

    def get_all(self):
      videos = sorted(self._video_library.get_all_videos(), key=operator.attrgetter('title'))
      return videos
      
    def number_of_videos(self):
        num_videos = len(self.get_all())
        print(f"{num_videos} videos in the library")
        
    def return_video_info(self, video):
      return (f"{video.title} ({video.video_id}) ["+ (' '.join(video.tags))+"]")
    
    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")
        videos = self.get_all()
        for video in videos:
          print(self.return_video_info(video))

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        if self._video_library.get_video(video_id) != None:
          video = self._video_library.get_video(video_id)
          video_title = video.title
          self._paused = False
        else: 
          print("Cannot play video: Video does not exist")
          return
          
        """None video is currently played"""  
        if self._currently_played is None:
          self._currently_played = video
          print("Playing video: "+ self._currently_played.title) 
        else:
          self.stop_video()
          self.play_video(video_id)

    def stop_video(self):
        """Stops the current video."""
        if self._currently_played is not None:
          print("Stopping video: " + self._currently_played.title)
          self._paused = False
          self._currently_played = None;
        else: 
          print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        if len(self.get_all())>0:
          random_index = random.randint(0,len(self.get_all())-1)
          random_video = self.get_all()[random_index]
          self.play_video(random_video.video_id)
        else: 
          print("No videos available")

    def pause_video(self):
        """Pauses the current video."""
        if self._currently_played is None: 
          print("Cannot pause video: No video is currently playing")
        else: 
          if not self._paused:
            print("Pausing video: " + self._currently_played.title)
            self._paused = True
          else:
            print("Video already paused: " + self._currently_played.title)

    def continue_video(self):
        """Resumes playing the current video."""
        if not self._currently_played: 
          print("Cannot continue video: No video is currently playing")
        elif not self._paused: 
          print("Cannot continue video: Video is not paused")
        else: 
          self._paused = False
          print("Continuing video: " + self._currently_played.title)

    def show_playing(self):
        """Displays video currently playing."""
        if self._currently_played is None:
          print("No video is currently playing")
        elif self._paused:
          print("Currently playing: " + self.return_video_info(self._currently_played)+" - PAUSED")
        else: 
          print("Currently playing: " + self.return_video_info(self._currently_played))
    
    def get_original_playlist_name(self, playlist_name):
      originalName = ''
      for key in self._playlists.keys():
        if playlist_name.lower()==key.lower():
          originalName = key
      return originalName
    
    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.
        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() != self.get_original_playlist_name(playlist_name).lower():
          self._playlists[playlist_name] = []
          print("Successfully created new playlist: "+ playlist_name)
        else:
          print("Cannot create playlist: A playlist with the same name already exists")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        video = self._video_library.get_video(video_id)
        if playlist_name.lower()!= self.get_original_playlist_name(playlist_name).lower():
          print("Cannot add video to "+ playlist_name +": Playlist does not exist")
        elif video is None:
          print("Cannot add video to "+ playlist_name +": Video does not exist")          
        elif video in self._playlists[self.get_original_playlist_name(playlist_name)]:
          print("Cannot add video to "+ playlist_name +": Video already added")
        else:
          self._playlists[self.get_original_playlist_name(playlist_name)].append(video)
          print("Added video to "+ playlist_name+": "+video.title)
          
    def show_all_playlists(self):
        """Display all playlists."""
        if len(self._playlists)==0:
          print("No playlists exist yet")
        else:
          print("Showing all playlists:")
          for key in sorted(self._playlists.keys()):
            print(key)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() != self.get_original_playlist_name(playlist_name).lower():
          print("Cannot show playlist "+playlist_name+": Playlist does not exist")
        else:
          print("Showing playlist: "+playlist_name)
          if len(self._playlists[self.get_original_playlist_name(playlist_name)])==0:
            print("No videos here yet")
          else:
            for video in self._playlists[self.get_original_playlist_name(playlist_name)]:
              print(self.return_video_info(video))

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        video = self._video_library.get_video(video_id)

        if video is None:
          print("Cannot remove video from "+ playlist_name+": Video does not exist")
        elif playlist_name.lower() != self.get_original_playlist_name(playlist_name).lower():
          print("Cannot remove video from "+playlist_name+": Playlist does not exist")
        elif video not in self._playlists[self.get_original_playlist_name(playlist_name)]:
          print("Cannot remove video from "+playlist_name+": Video is not in playlist")
        elif video in self._playlists[self.get_original_playlist_name(playlist_name)]:
          self._playlists[self.get_original_playlist_name(playlist_name)].remove(video)
          print("Removed video from "+playlist_name+": "+video.title)

        
    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        
        if playlist_name.lower() !=self.get_original_playlist_name(playlist_name).lower():
          print("Cannot clear playlist "+playlist_name+": Playlist does not exist")
        else:
          self._playlists[self.get_original_playlist_name(playlist_name)]=[]
          print("Successfully removed all videos from "+playlist_name)
        
    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() not in (key.lower() for key in self._playlists.keys()):
          print("Cannot delete playlist "+playlist_name+": Playlist does not exist")
        else:
          del self._playlists[self.get_original_playlist_name(playlist_name)]
          print("Deleted playlist: "+playlist_name)

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        videos = self.get_all()
        search_videos = []
        for video in videos: 
          if search_term.lower() in video.title.lower():
            search_videos.append(video)
        if len(search_videos)==0:
          print("No search results for "+search_term)
        else: 
          for video in search_videos:
            print(self.return_video_info(video))
          self.ask_to_play(search_videos)
          
    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        videos = self.get_all()
        search_videos = []
        for video in videos: 
          if search_term.lower() in video.tags.lower():
            search_videos.append(video)
        if len(search_videos)==0:
          print("No search results for "+search_term)
        else: 
          for video in search_videos:
            print(return_video_info(video))
          print('\n')
          self.ask_to_play(search_videos)

    def ask_to_play(self, videos):
      val = input("Would you like to play any of the above?"+'\n'+"If yes, specify the number of video. If your answer is not a valid number, we will assume it's a no. \n")
      if val.isnumeric() and int(val) <= (len(videos)-1):
        self.play_video(videos[int(val)].video_id)
      
    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        print("flag_video needs implementation")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")
