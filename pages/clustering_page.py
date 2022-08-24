from warnings import catch_warnings
import streamlit as st
import pandas as pd
import numpy as np
import spotify_utils as su
import matplotlib.pyplot as plt

# page set up
st.set_page_config(layout="wide")

# title and input section
st.title("Spotify Clustering v0.1")
st.write(
    "This program allows you to cluster your favorite artists and compare them to the 'This is: <Artist>' playlists created by Spotify. This page requires 1 csv files formatted in the following: "
)
st.write(
    "artist_name | personal_artist_playlist_link |spotify_this_is_artist_playlist_link",
)
st.write("Do not add headers to the csv")

# file upload and format
# decorator stores matrix in cache
file = st.file_uploader(label="Upload formatted csv here")


@st.experimental_memo(show_spinner=False)
def read_file():
    if file is not None:
        df = pd.read_csv(file, header=None)
        personaldf, spotifydf = su.format_artist_csv_to_uri(df=df)
        with st.spinner(
            "Creating personal artist matrix. May take a while depending on playlist size"
        ):
            pmatrix = su.create_feature_matrix(personaldf)
        with st.spinner(
            "Creating spotify artist matrix. May take a while depending on playlist size"
        ):
            smatrix = su.create_feature_matrix(spotifydf)
    return pmatrix, smatrix


pmat, smat = read_file()

# initialize clustering
input = st.slider(label="Enter number of clusters", min_value=2, max_value=6)
pkm, _ = su.custom_kmean(data=pmat, k=input)
skm, _ = su.custom_kmean(data=smat, k=input)
personal = pd.concat([pd.DataFrame(pmat.index), pd.DataFrame(pkm)], axis=1)
personal = personal.set_index("artist_name")
spotify = pd.concat([pd.DataFrame(smat.index), pd.DataFrame(skm)], axis=1)
spotify = spotify.set_index("artist_name")
col1, col2 = st.columns(2)
with col1:
    st.write("Personal Clusters")
    st.dataframe(personal)
with col2:
    st.write("Spotify Clusters")
    st.dataframe(spotify)
st.write(
    "For visualization purposes, we use two principal components which explain about 64% of the variance. Note that to visualize the components,"
)

# PCA and visualize
personal_cluster_graph = su.pca_for_viz(data=pmat, ncomps=2, k=input)
spotify_cluster_graph = su.pca_for_viz(data=smat, ncomps=2, k=input)
col1, col2 = st.columns(2)
with col1:
    st.write("Personal Clusters")
    st.plotly_chart(personal_cluster_graph, use_container_width=True)
with col2:
    st.write("Spotify Clusters")
    st.plotly_chart(spotify_cluster_graph, use_container_width=True)
