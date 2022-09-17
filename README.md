# Spotify Utility Suite

Welcome to the Spotify Utility Suite (SUS). This is a personal project that I've create to experiment with Spotify and interact with my music in a novel way. This project started as a simple data mining exercise and developed into a web application, automation, and utility suite 

### Web Application
The web application consists of two parts
1. A program that can be used to visualize statistics of certain songs or playlists 
2. A clustering algorithm that can compare personal "artist" playlists and Spotify's "This is <Artist>" playlists.

I've always been really interested in why and how Spotify chooses the songs in the "This is `Artist`" playlists. I have a lot of my own artist playlists and decided
to use clustering methods to see if their selection of songs lines up with mine. The clustering page uses data from part 1 and provides an interactive visualization 
via plotly. 

Find the web app at bit.ly/susuite

### Automation
It's extremely hard to keep my artist playlists updated as I listen to new music all the time. This automation adds each song to its corresponding artist
playlist so I don't have to worry about it. The framework can be applied to different playlist types. This can be found in `auto_arrange.py`

### Utility Suite
With these projects, I had to combine API calls and existing methods and create new functions that I used throughout this project. All of these can be found in the
`spotify_utils.py`. `Import spotify_utils as su` refers to these methods

Features I'll be working on next

1. Recommendation system that uses the data from (1)
2. Multiprocessing (2) to decrease runtime for large collections of playlists
3. Finishing the TODO items on auto_arrange.py

Feel free to create PR's if you'd like to see any features or want to contribute!

Enjoy!
