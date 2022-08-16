"""
Utility functions used to pull the URI from a song 
or playlist 
"""

import pandas as pd
import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st
cid = 'c417c830b1364214913582abdf8717c3'
cids = '9cbf646564b6496f93c59e7e7853ec13'
credentials = SpotifyClientCredentials(client_id= cid, client_secret=cids)
sp = spotipy.Spotify(client_credentials_manager = credentials)


def extract_uri(link, song=True):
    """
    Function to extract the URI from a spotify link
    
    Paramters
    =========
    link: str
        The spotify url

    Returns
    =======
    uri: str
        The uri from the link
    """
    if song == True:
        uri = link.split('track/')[1].split('?')[0]
    else:
        uri = link.split('list/')[1].split('?')[0]
    return uri


def extract_tracks_from_playlist(uri_plist):
    """
        Function that extracts track information for
        all songs in a playlist
        
        Paramters
        =========
        uri_plist: str
            The spotify url

        Returns
        =======
        tracklist: list
            A list with JSON formatted entries of track information
        """
    results = sp.playlist_tracks(uri_plist)
    tracklist = results["items"] #items removes my data to make dataset
    while results['next']:
        results = sp.next(results)
        tracklist.extend(results['items'])
    return tracklist

def extract_features(song = False, uri = None, tracklist = None):
    """
    Function that extracts all numerical data for each song in a playlist and returns 
    a dataframe for further visualization

    Paramters
    =========
    song: bool
        Boolean value to determine if only 1 song is
        being analyzed
    
    uri: str
        URI of song being analyzed
    
    tracklist: list
        A list of JSON formatted entries of track information 

    Returns
    =======
    features_df: DataFrame
        A dataframe containing numerical features for each song 
        in the playlist
    """
    if song == False and uri:
        raise ValueError("Cannot provide playlist uri. Please input a song uri and set song to True")
    elif song == True and not uri:
        raise ValueError("Please input a uri for the song")

    feat_list = []
    numeric_features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness','instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']
    if song == True and uri:
        for vals in numeric_features:
                value = sp.audio_features(uri)[0][vals]
                feat_list.append(value)    
        features_df = pd.DataFrame()
        features_df = pd.concat([features_df, pd.Series(feat_list)], axis=0, ignore_index=True).T
        features_df.columns = numeric_features
    else:
        # pulling track names and uri's
        track_uris = []
        track_names = []
        for tracks in tracklist:
            track_uris.append(tracks['track']['uri'])
            track_names.append(tracks['track']['name'])
        features_df = pd.DataFrame() 
        if tracklist:
            for idx, uri in enumerate(track_uris):
                feat_list = []
                print(uri)
                for vals in numeric_features:
                    value = sp.audio_features(uri)[0][vals]
                    feat_list.append(value)
                feat_s = pd.Series(feat_list).T
                features_df = pd.concat([features_df, feat_s], axis=1)
            features_df.index = numeric_features
            features_df.columns = track_names
            features_df = features_df.T
            #adding the popularity score
            pop_score = []
            for t in range(0, len(tracklist)):
                pop_score.append(tracklist[t]['track']['popularity'])
            pop_score = pd.DataFrame(pop_score, columns=['popularity'], index = track_names)
            features_df = pd.concat([features_df, pop_score], axis=1)
        else:
            raise ValueError("Please specify if entry is a song or provide a tracklist")
    return features_df

def grapher_utils(features_df, selection):
    """
    Function that generates the graphs 
    for playlists and songs

    Parameters
    ==========
    features_df: pd.DataFrame
        The dataframe holding the data used 
        to generate graphs
    
    selection: list
        Which features to graph. Must 
        be columns from the dataframe
    """
    import matplotlib.pyplot as plt
    c = "#FF4B4B"
    if len(selection) >= 0 and len(selection) <= 3:
        fig,ax = plt.subplots(1,3,figsize=(16,6))
        fig.subplots_adjust(wspace=0.1)
        i = 0
        for i in range(0, len(selection)):
            ax[i].bar(range(0,len(features_df.index)), features_df[selection[i]], color = c)
            ax[i].set_title(selection[i])

        return fig

    elif len(selection) > 3 and len(selection) <=6:
        fig,ax = plt.subplots(2,3,figsize=(16,6))
        fig.subplots_adjust(wspace=0.1)
        i,j = 0,0
        #row 1
        for i in range(0,3):
            ax[0,i].bar(range(0,len(features_df.index)), features_df[selection[i]], color = c)
            ax[0,i].set_title(selection[i])
        
        selection = selection[3:] 

        #row 2
        for j in range(0, len(selection)):
            ax[1,j].bar(range(0,len(features_df.index)), features_df[selection[j]], color = c)
            ax[1,j].set_title(selection[j])

        return fig

    elif len(selection) > 6 and len(selection) <= 9:
        fig,ax = plt.subplots(3,3,figsize=(16,10))
        fig.subplots_adjust(wspace=0.3, hspace=0.4)
        i,j,k = 0,0,0
        #row 1
        for i in range(0,3):
            ax[0,i].bar(range(0,len(features_df.index)), features_df[selection[i]], color = c)
            ax[0,i].set_title(selection[i])
        
        selection = selection[3:]

        #row 2
        for j in range(0, 3):
            ax[1,j].bar(range(0,len(features_df.index)), features_df[selection[j]], color = c)
            ax[1,j].set_title(selection[j])
        
        selection = selection[3:]
        
        #row 3
        for k in range(0, len(selection)):
            ax[2,k].bar(range(0,len(features_df.index)), features_df[selection[k]], color = c)
            ax[2,k].set_title(selection[k])

        return fig

    elif len(selection) > 9 and len(selection) <= 12:
        fig,ax = plt.subplots(4,3,figsize=(16,10))
        fig.subplots_adjust(wspace=0.3, hspace=0.4)
        i,j,k,l = 0,0,0,0
        #row 1
        for i in range(0,3):
            ax[0,i].bar(range(0,len(features_df.index)), features_df[selection[i]], color = c)
            ax[0,i].set_title(selection[i])

        selection = selection[3:]

        #row 2
        for j in range(0, 3):
            ax[1,j].bar(range(0,len(features_df.index)), features_df[selection[j]], color = c)
            ax[1,j].set_title(selection[j])
        
        selection = selection[3:]
        
        #row 3
        for k in range(0, 3):
            ax[2,k].bar(range(0,len(features_df.index)), features_df[selection[k]], color = c)
            ax[2,k].set_title(selection[k])
        
        selection = selection[3:]
        
        #row 4
        for l in range(0, len(selection)):
            ax[3,l].bar(range(0,len(features_df.index)), features_df[selection[l]], color = c)
            ax[3,l].set_title(selection[l])

        return fig

    elif len(selection) > 12 and len(selection) <= 14:
        fig,ax = plt.subplots(5,3,figsize=(16,16))
        fig.subplots_adjust(wspace=0.3, hspace=0.4)
        i,j,k,l,m = 0,0,0,0,0
        #row 1
        for i in range(0,3):
            ax[0,i].bar(range(0,len(features_df.index)), features_df[selection[i]], color = c)
            ax[0,i].set_title(selection[i])
        
        selection = selection[3:]
        
        #row 2
        for j in range(0, 3):
            ax[1,j].bar(range(0,len(features_df.index)), features_df[selection[j]], color = c)
            ax[1,j].set_title(selection[j])
        
        selection = selection[3:]
        
        #row 3
        for k in range(0, 3):
            ax[2,k].bar(range(0,len(features_df.index)), features_df[selection[k]], color = c)
            ax[2,k].set_title(selection[k])
        
        selection = selection[3:]
        
        #row 4
        for l in range(0, 3):
            ax[3,l].bar(range(0,len(features_df.index)), features_df[selection[l]], color = c)
            ax[3,l].set_title(selection[l])
        
        selection = selection[3:]
        
        #row 5
        for m in range(0, 2):
            ax[4,m].bar(range(0,len(features_df.index)), features_df[selection[m]], color = c)
            ax[4,m].set_title(selection[m])
            # ax[4][0].set_position([0.24,0.125,0.228,0.343])
            # ax[4][1].set_position([0.55,0.125,0.228,0.343])
            ax[4,2].set_visible(False)
        
        return fig 

def format_artist_csv_to_uri(df):
    """
    Takes in a csv with artist_name | personal_playlist_link | spotify_playlist_link
    and creates 2 formatted dataframes with names and uri's of playlists for further
    analysis

    TODO: Create a loop to remove repeated code for spotify and personal df
    
    Parameters
    ==========
    df: pd.DataFrame
        The dataframe with specified columns
    
    Returns
    =======
    df_dict: dictionary
        A dictionary of dataframes. One is
        personal and one is spotify
    """
    df.columns = ['artist_name', 'personal_playlist_link', 'spotify_playlist_link']
    personal = df[['artist_name', 'personal_playlist_link']]
    spotify = df[['artist_name', 'spotify_playlist_link']]
    ap_uris = []
    for link in personal.personal_playlist_link:
        uri = extract_uri(link, song=False)
        ap_uris.append(uri)
    personal['uri'] = ap_uris
    personal.drop('personal_playlist_link',axis=1,inplace=True)
    ap_uris = []
    for link in spotify.spotify_playlist_link:
        uri = extract_uri(link, song=False)
        ap_uris.append(uri)
    spotify['uri'] = ap_uris
    spotify.drop('spotify_playlist_link',axis=1,inplace=True)
    
    return personal, spotify

def create_feature_matrix(df):
    """
    This is an extension of the `extract_features` function
    
    This function pulls each song from the playlist uri and
    saves it into a tracklist. Features are extracted from 
    each song in the tracklist and averaged to create a feature
    series for each artist. The output provides a dataframe with 
    the average numerical scores for each artist for further use

    Parameters
    ==========
    df: pd.DataFrame
        A dataframe with artist_name and uri for 
        the playlist. This can be created via the 
        `format_artist_csv_to_uri` function
    
    Returns
    =======
    feature_matrix: pd.DataFrame
        A dataframe with average features for 
        each artist
    """

    artist_data = pd.DataFrame()
    numeric_features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness','instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']

    for idxx,uril in enumerate(df['uri']):
        # create tracklist and extract uris and names
        tracklist = extract_tracks_from_playlist(uril)
        track_uris = []
        #track_names = []
        for tracks in tracklist:
            track_uris.append(tracks['track']['uri'])
            #track_names.append(tracks['track']['name'])

        # popularity score for each song
        pop_score=[]
        for t in range(0, len(tracklist)):
            pop_score.append(tracklist[t]['track']['popularity'])
        pop_score = pd.DataFrame(pop_score, columns=['popularity'])
        
        # creating the feature matrix 
        features_df = pd.DataFrame()
        print('Starting track parsing process for', df.iloc[idxx,0])
        for idx,uri in enumerate(track_uris):
            feat_list = []
            for vals in numeric_features:
                value = sp.audio_features(uri)[0][vals]
                feat_list.append(value)
            feat_s = pd.Series(feat_list).T
            features_df = pd.concat([features_df, feat_s], axis=1)
            if idx % 10 == 0 and idx != 0:
                print('Data from ', idx, 'songs have been parsed')
        print("All data from", df.iloc[idxx,0], "has been added to the feature matrix")
        
        # Format the features for each artist and take means to add it to the artist_data matrix
        features_df.index = numeric_features
        #features_df.columns = track_names
        features_df = features_df.T.reset_index(drop=True)
        print(features_df.head(2))
        print(pop_score.head(2))
        features_df = pd.concat([features_df, pop_score], axis=1, ignore_index=True)
        means = pd.DataFrame(features_df.mean()).T.reset_index(drop=True)
        artist_data = pd.concat([artist_data,means])
        print("Added to artist_data. Running loop again...\n")
    artist_data.index = df['artist_name']
    return artist_data
    
