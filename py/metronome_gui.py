import streamlit as st
import sqlite3
import requests
from streamlit_autorefresh import st_autorefresh
import configparser

config = configparser.ConfigParser()
config.read("../etc/config.ini")
API_URL = config.get('metronome_srv', 'API_URL')

# --- Session State ---
if "bpm" not in st.session_state:
    st.session_state.bpm = 120

# --- Load Songs ---
def load_songs():
    conn = sqlite3.connect("../opt/songs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, songname, bpm FROM songs ORDER BY songname")
    songs = cursor.fetchall()
    conn.close()
    return songs

songs = load_songs()
song_options = {f"{songname} ({bpm} BPM)": (id, bpm) for id, songname, bpm in songs}
song_names = list(song_options.keys())

st.title("🎵 The Band Metronome")

# --- Song Selection ---
selected_song = st.selectbox("🎶 Select a song", ["None"] + song_names)
if selected_song != "None":
    _, selected_bpm = song_options[selected_song]
    st.session_state.bpm = selected_bpm

# BPM Slider
st.session_state.bpm = st.slider("🎚️ BP",40,140, st.session_state.bpm)
st.markdown(f"**🕒 BPM set to: `{st.session_state.bpm}`**")

# --- API Control ---
def start_metronome():
    requests.post(f"{API_URL}/start", json={"bpm": st.session_state.bpm})

def stop_metronome():
    requests.post(f"{API_URL}/stop")

def get_status():
    try:
        r = requests.get(f"{API_URL}/status")
        return r.json()
    except:
        return {"running": False}

col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Start"):
        start_metronome()
with col2:
    if st.button("⏹️ Stop"):
        stop_metronome()

status = get_status()
if status["running"]:
    st.success(f"Metronome is running at {status['bpm']} BPM")
else:
    st.info("Metronome is stopped.")

# Auto-refresh UI every 2s to reflect real-time state
st_autorefresh(interval=200, key="refresh")

