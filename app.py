# -----------------------------------------------------------
# Spotify Analitics APP, made for CS50x 2022
#
# (C) 2022 Emiliano Giannoni, Buenos Aires, Argentina
# Released under GNU Public License (GPL)
# email emigiannonigmail.com
# -----------------------------------------------------------

import os
import pandas as pd
import numpy as np

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
        
        except:

            playlist_information = 0

        if playlist_information == 0:
                
            error = 1

            return render_template("playlist.html", error = error)
            
        else:
                
            return render_template("playlist-results.html", playlist_information)

    else:

        return render_template("playlist.html", error = 0)