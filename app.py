# -----------------------------------------------------------
# Spotify Analitics APP, made for CS50x 2022
#
# (C) 2022 Emiliano Giannoni, Buenos Aires, Argentina
# Released under GNU Public License (GPL)
# email emigiannonigmail.com
# -----------------------------------------------------------

import os
import matplotlib.pyplot as plt
import operator

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


# ---------------------------------------------------------------
# Server configuration and server side logic using FLASK
# ---------------------------------------------------------------

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():

    return render_template("index.html")


@app.route("/playlist", methods=["GET", "POST"])
def playlist():

    if request.method == "POST":
        
        # Get input provided by user
        playlist_link = request.form.get("url")

        # Try to extract the play list URI
        playlist_URI = playlist_link.split("/")[-1].split("?")[0]

        # Calls API and get playlist information
        try:
            
            playlist_information = sp.playlist_tracks(playlist_URI)["items"]

            src = "https://open.spotify.com/embed/playlist/" +playlist_URI+ "?utm_source=generator"

            cover = sp.playlist_cover_image(playlist_URI)[0]['url']
        
        except:

            playlist_information = 1

        if playlist_information == 1:
                
            error = 'Invalid URL, please try again!'

            return render_template("playlist.html", error = error)
            
        else:

            time = 0

            for track in playlist_information:

                time = time + (track["track"]["duration_ms"] / 60000)

            timef = round(time, 2)

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

            fig, ax = plt.subplots()

            #Colocamos una etiqueta en el eje Y

            ax.set_ylabel('Songs')

            #Colocamos una etiqueta en el eje X

            ax.set_title('Year')

            #Creamos la grafica de barras utilizando 'paises' como eje X y 'ventas' como eje y.

            plt.bar(sorted_years, songs)

            plt.savefig('static/barras_simple.png')
            
            #Funcion artistas principales e info

            artists = []

            for track in playlist_information:

                if len(track["track"]["artists"]) > 1:
                
                    for artist in track["track"]["artists"]:

                        artists.append(artist["id"])
                
                else:

                    artists.append(track["track"]["artists"][0]["id"])

            top_artist = {}

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


            return render_template("playlist-results.html", info = playlist_information, src = src, cover = cover, time = timef, artist_information = artist_information)

    else:

        return render_template("playlist.html")