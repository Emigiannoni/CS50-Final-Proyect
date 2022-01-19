# ---------------------------------------------------------------
# SPOTIFY API accessing and configuration using SPOTIFY library
# ---------------------------------------------------------------
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

release_date = []

for track in playlist_information:
    
    release_date.append(track["track"]["album"]["release_date"])

release_year = []

for date in release_date:

    release_year.append(date.split("'")[0].split("-")[0])

songsxyear = {}

for year in release_year:

    if year in songsxyear.keys():

        songsxyear[year] = songsxyear[year] + 1

    else:

        songsxyear[year] = 1

#Definimos una lista con anos como string

years = []

for year in songsxyear:

    years.append(year)

sorted_years = sorted(years)

#Definimos una lista con numero de canciones como entero

songs = []

for year in sorted_years:

    number = songsxyear[year]

    songs.append(number)

print(release_date)
print(release_year)
print(songsxyear)
print(sorted_years)
print(songs)
