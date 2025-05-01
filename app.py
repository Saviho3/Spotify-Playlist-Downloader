from flask import Flask, request, session, redirect, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import pandas as pd


username = "Saviho3" #Spotify Username
playlist_ID = "2TH8q5UJk7mmH1Afdc4wta" #string right after playlist/ in url

app = Flask(__name__)

app.secret_key = "sdhlkashge34d" #can be anything
app.config['Session_COOKIE_NAME'] = 'session'
TOKEN_INFO = "token_info"



@app.route('/')
def login():
    spotify_oauth = create_spotify_oauth()
    auth_url = spotify_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    spotify_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = spotify_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for("getTracks", _external = True))


@app.route('/getTracks')
def getTracks():
    try:
        token_info = get_token()
    except:
        print("User is not logged into Spotify (No Authorization)")
        return redirect("/")
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    all_tracks = []
    all_tracks_info = []
    itteration = 0
    #return str(sp.user_playlist_tracks(user=username, playlist_id=playlist_ID, fields=None, limit=100, offset=0, market=None))
    
    while True:
        current_tracks = sp.user_playlist_tracks(user=username, playlist_id=playlist_ID, fields=None, limit=100, offset=itteration*100, market=None)['items']
        all_tracks += current_tracks
        
        for i, item in enumerate(current_tracks):
            track = item['track']
            if track is not None:
                all_tracks_info += [track['name'] + " - " + str(track['artists'][0]['name'])]

            
        
        if len(current_tracks) < 100:
            break

        itteration += 1

    df = pd.DataFrame(all_tracks_info, columns=["song names"]) 
    df.to_csv('songs.csv', index=False)
    return all_tracks_info

    #return str(sp.current_user_saved_tracks(limit=50, offset=50)['items'])

def get_token():
    token_info = session.get(TOKEN_INFO)
    if not token_info:
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = "",
        client_secret = "",
        #Find the 2 above values in this link: https://developer.spotify.com/ 
        redirect_uri = url_for('redirectPage', _external = True),
        scope = "user-library-read"
        )

if __name__ in "__main__":
    app.run(debug=True)