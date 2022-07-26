"""
Utility functions used to pull the URI from a song 
or playlist 
"""


import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials


cid = 'x'
cids = 'x'
credentials = SpotifyClientCredentials(client_id= cid, client_secret=cids)
sp = spotipy.Spotify(client_credentials_manager = credentials)


# Extract the URI from a single playlist link
def uri_from_playlist(link):
    uri = link.split('list/')[1].split('?')[0]
    return uri

# Extract URI from a song
#   returns in the form 'spotify:track:uri'
def uri_from_song(link):
    uri = link.split('track/')[1].split('?')[0]
    uri_formatted = 'spotify:track:'+uri
    return uri_formatted

#Extract track URIs from the given playlist URI (returns list with URIs)
#   this is an upgrade of the original track_output_from_playlist to return 
#   all songs of a dataset not just 100
def track_output_from_playlist_100(uri_plist):
    results = sp.playlist_tracks(uri_plist)
    tracks = results["items"] #items removes my data to make dataset
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks
