"""
Using Streamlit to host this project

Features
=========
The user can provide a song or playlist link and get
a dataframe of numerical features corresponding to the song
or playlist. 

Future releases
===============
v0.2 - User can provide a link to multiple artist playlists and
        compare their selection of an artists songs to the spotify
        "This is <Artist>" playlist. It requires the user to give a 
        csv with 3 columns
        artist name | personal playlist link | spotify "this is" link

        The user will be able to select between different clustering
        methods to compare how it changes based on the algorithm

v0.2.1 - User's will be able to visualize in depth data through the 
          audio analysis feature in the spotify API 

v0.3 - User can input a playlist and recieve customized recommendations
        for the playlist. This will be an extension of the recommendation
        algorithm that I build for lofi rap
"""
import streamlit as st
import pandas as pd
import numpy as np
import spotify_utils as su
import matplotlib.pyplot as plt

#page set up
st.set_page_config(layout="wide")
nf = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness','instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature', 'popularity'] 
run_button_click = False

#refresh visualizations
def refresh_viz(df, selected):
        plot = su.grapher_utils(features_df=df, selection=selected)
        return plot


# title and input section
st.title("Spotify Visualizer v0.1")
st.write("Welcome to the Spotify Visualizer v0.1. This application is designed to visualize songs or playlists")
st.write("Note: If the link given is a playlist and song is selected, the first song from the playlist will be analyzed")
input = st.text_input(label="Enter spotify url here")
ckbox = st.selectbox(label="Select if you are viewing a song or a playlist: ",options=[" ","Song", "Playlist"])
container = st.container()
#st.multiselect(label="Select features to visualize", options=nf)
check_all = st.checkbox(label="Select all", value=False)
if check_all:
        multisel = container.multiselect("Select features to visualize", nf, nf) 
else:
        multisel = container.multiselect("Select features to visualize", nf)
run_button = st.button("Run")
if run_button and ckbox == " ":
        st.error("Please select song or playlist")
elif run_button:
        if ckbox == "Song":
                uri = su.extract_uri(input, song=True)
                features_df = su.extract_features(uri=uri, song=True)
                st.success("Features extracted from track")
                run_button_click = True
        elif ckbox == "Playlist":
                uri = su.extract_uri(input, song=False)
                tracklist = su.extract_tracks_from_playlist(uri)
                with st.spinner("Extracting features from playlist. May take a while depending on playlist size"):
                        features_df = su.extract_features(tracklist=tracklist)
                        #TODO: Informative output saying how many songs are left in the loop
                st.success("All tracks were parsed")
                run_button_click = True
if run_button_click == True:
        st.dataframe(features_df)
        st.pyplot(refresh_viz(features_df, selected=multisel))


