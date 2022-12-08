"""
Welcome to Liked Songs Automation!
This program is useful to people who have artist 
playlists and want to be able to automatically transfer
songs from their Liked Songs into these artist playlists

To use
------
1. Edit the playlists.json file. Make sure 
    to spell the artist name exactly how it
    shows up on Spotify. Then paste each playlist
    uri into the corresponding value. The URI is
    after "list" in the URL and before the "?". You
    can also use spotify_utils.extract_uri to capture
    each uri

2. Edit the date.json file to specify the cutoff date.
    Songs before this date will not be sorted.

3. Create a private key file with the structure and name it
    priv.json
    {
        client id: 
        client id secret:
        scope:
    }
    TODO: allow user to just log in 

3. Run the program and watch songs appear in your playlists
"""

######################################################################## JSON reading ####################################################################################
import json

# keys
with open("json_settings/priv.json") as private:
    priv = json.load(private)
# playlists
with open("json_settings/playlists.json") as data:
    artist_playlists = json.load(data)
# cutoff date
with open("json_settings/date.json") as cutoff:
    cutoff = json.load(cutoff)

######################################################################## Program start ####################################################################################
import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

cid = priv["cid"]
cids = priv["cids"]
scope = priv["scope"]
credentials = SpotifyClientCredentials(client_id=cid, client_secret=cids)
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=cid,
        client_secret=cids,
        scope=scope,
        redirect_uri="http://google.com/callback/",
    )
)
import spotify_utils as su


def get_all_saved_tracks(limit_step=50):
    """
    A way to pull more than 50 tracks from 'Liked
    Songs' on Spotify. This is a similar function to
    su.extract_tracks_from_playlist. However, they cannot
    be interchanged because 'Liked Songs' is not technically
    considered a playlist

    Parameters
    ==========
    limit_step: int
        How many tracks to pull at once. This should
        stay at 50 unless you want to pull a subset

    Returns
    =======
    tracks: list
        List of all tracks and their information. Each
        list contains dict entries of the songs
    """

    tracks = []
    for offset in range(0, 100000, limit_step):
        response = sp.current_user_saved_tracks(
            limit=limit_step,
            offset=offset,
        )
        if len(response) == 0:
            break
        tracks.extend(response["items"])
    return tracks


def get_artists(song_info):
    """
    A way to pull artist(s) information
    from the JSON format

    Paramters
    =========
    song_info: dict
        The song entry in the tracklist

    Returns
    =======
    artist: str or list
        Either a string of the artist name
        or a list containing all artists
    """

    num_artists = len(song_info["track"]["artists"])
    if num_artists > 1:
        alist = []
        for j in range(0, num_artists):
            alist.append(song_info["track"]["artists"][j]["name"])
        return alist
    else:
        return song_info["track"]["artists"][0]["name"]


# get liked songs
tracks = get_all_saved_tracks(limit_step=50)

# check date of songs
#   append valid songs that meet date cuttoff
valid_songs = []
for i in range(0, len(tracks)):
    date = datetime.datetime.strptime(tracks[i]["added_at"].split("T")[0], "%Y-%m-%d")
    if date > datetime.datetime(
        year=cutoff["year"], month=cutoff["month"], day=cutoff["day"]
    ):
        valid_songs.append(tracks[i])

# check artists of each song
#   if artist name exists, add to valid list
#   if not, add song to non_valid list
artist_exist = []
artist_not_exist = []
for i in range(0, len(valid_songs)):
    num_artists = len(valid_songs[i]["track"]["artists"])
    if num_artists > 1:
        alist = []
        for j in range(0, num_artists):
            alist.append(valid_songs[i]["track"]["artists"][j]["name"])
        # check if alist contains any values in keys
        if any(artists in artist_playlists.keys() for artists in alist):
            artist_exist.append(valid_songs[i])
        else:
            artist_not_exist.append(valid_songs[i])
    else:
        name = valid_songs[i]["track"]["artists"][0]["name"]
        if name in artist_playlists.keys():
            artist_exist.append(valid_songs[i])
        else:
            artist_not_exist.append(valid_songs[i])

# adding songs to artist playlists
#   first check if the song already exists
#   if not then add to playlist
for i in range(0, len(artist_exist)):
    print(i)
    target_artist = get_artists(artist_exist[i])
    print(target_artist)
    if isinstance(target_artist, list):
        for a in target_artist:
            if a in artist_playlists.keys():
                target_playlist = artist_playlists[a]
    else:
        target_playlist = artist_playlists[target_artist]
        print(target_playlist)

    tracks_of_target = sp.playlist(playlist_id=target_playlist, fields="tracks,next")
    uris_of_target = []
    for j in range(0, len(tracks_of_target["tracks"]["items"])):
        uris_of_target.append(tracks_of_target["tracks"]["items"][j]["track"]["uri"])

    bool = artist_exist[i]["track"]["uri"] in uris_of_target

    if bool:
        print("Song already exists in playlist")
    else:
        sp.user_playlist_add_tracks(
            user="ishandhanani2234",
            playlist_id=target_playlist,
            tracks=[artist_exist[i]["track"]["uri"]],
        )
        print("Song added")

#return songs that are not sorted 
for i in range(0, len(artist_not_exist)):
    print(artist_not_exist[i]['track']['name'])
        

#update the date in JSON for next time
cutoff['year'] = datetime.date.today().year
cutoff['month'] = datetime.date.today().month
cutoff['day'] = datetime.date.today().day
with open("json_settings/date.json", 'w') as outfile:
    json.dump(cutoff, outfile)
