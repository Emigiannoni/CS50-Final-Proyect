# ---------------------------------------------------------------
# SPOTIFY API accessing and configuration using SPOTIFY library
# ---------------------------------------------------------------
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import operator
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API client configuration
SPOTIPY_CLIENT_ID='a15508df1c4d4a1bb809c3d4b93909d0'
SPOTIPY_CLIENT_SECRET='255b7974b8c04da9beb0c7aa2ba8589e'
SPOTIPY_REDIRECT_URI='http://127.0.0.1:5000/'

# Accessing API
client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
scope = "user-library-read"
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) 
sp.trace=False

playlist_link = "https://open.spotify.com/playlist/2kZRc4eOwonZVY2oSibdKd"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]

            
playlist_information = sp.playlist_tracks(playlist_URI)["items"]

artists = []

for track in playlist_information:

    if len(track["track"]["artists"]) > 1:
    
        for artist in track["track"]["artists"]:

            artists.append(artist["id"])
    
    else:

        artists.append(track["track"]["artists"][0]["id"])
 
top_artist = {} #artista y numero de apariciones

for artist in artists:

    if artist in top_artist:

        top_artist[artist] = top_artist[artist] + 1

    else:

        top_artist[artist] = 1

top_artist_sorted = sorted(top_artist.items(), key=operator.itemgetter(1), reverse=True)

top10_artist_sorted = []

i = 0

for artist in top_artist_sorted:

    if i < 10:

        top10_artist_sorted.append(artist)

        i = i + 1

    else:

        pass

id_top_artist = []

for artist in top10_artist_sorted:

    id_top_artist.append(artist[0])

artist_information = []

for artist_id in id_top_artist:

    artist_information.append(sp.artist(artist_id))

for i in range(len(artist_information)):

    artist_information[i]['apariciones'] = top10_artist_sorted[i][1]

print(artist_information)