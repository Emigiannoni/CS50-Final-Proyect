# ---------------------------------------------------------------
# SPOTIFY API accessing and configuration using SPOTIFY library
# ---------------------------------------------------------------

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

playlist_link = "asd"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]

try:
            
    playlist_information = sp.playlist_tracks(playlist_URI)["items"]
        
except:

    playlist_information = 1

if playlist_information == 1:
                
    error = 1


print(error)

