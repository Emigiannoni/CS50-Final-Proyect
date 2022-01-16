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

playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

playlist_information = sp.playlist_tracks(playlist_URI)["items"]

information = []

songs = {
    'track_name' : 0,
    'track_uri' : 0,
    'artist_name' : 0,
    'artist_uri' : 0,
    'album' : 0
}

i = 0

for track in playlist_information:

    information.append(songs)

    #Track name
    track_name = track["track"]["name"]
    track_uri = track["track"]["uri"]
    
    #Main Artist
    artist_uri = track["track"]["artists"][0]["uri"]
    artist_name = track["track"]["artists"][0]["name"]
    
    #Album
    album = track["track"]["album"]["name"]

    information[i]['track_name'] = track_name
    information[i]['track_uri'] = track_uri
    information[i]['artist_name'] = artist_name
    information[i]['artist_uri'] = artist_uri
    information[i]['album'] = album

    cover = playlist_cover_image(playlist_URI)

    i = i + 1

    print(cover)



