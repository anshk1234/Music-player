# music_player_live.py
import streamlit as st
from yt_dlp import YoutubeDL
import time
import json
from streamlit_lottie import st_lottie
import base64

# ---- Page Configuration ----
st.set_page_config(page_title=" Music Player ", page_icon="🎵")

# --- Splash Animation ---
def load_lottiefile(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

if "show_intro" not in st.session_state:
    st.session_state.show_intro = True

if st.session_state.show_intro:
    lottie_intro = load_lottiefile("music.json")
    splash = st.empty()
    with splash.container():
        st.markdown("<h1 style='text-align:center;'>Welcome to MUSIC HUB!</h1>", unsafe_allow_html=True)
        st_lottie(lottie_intro, height=280, speed=0.5, loop=True)
        time.sleep(2)
    splash.empty()
    st.session_state.show_intro = False

# ---- Set Background & Neon Sidebar ----
def set_local_background(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()
    css = f"""
    <style>
    html, body, .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stVerticalBlock"],
    .main, .block-container,
    .css-1d391kg, .css-18ni7ap {{
        background: transparent !important;
    }}
    section[data-testid="stSidebar"] {{
        background-color: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(12px);
        box-shadow: inset 0 0 10px #00ffff60, 0 0 20px #00ffff88;
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }}
    section[data-testid="stSidebar"] * {{
        background-color: transparent !important;
    }}
    button:hover {{
        border: 1px solid #00ffff !important;
        box-shadow: 0 0 12px #00ffff60;
        color: #00ffff !important;
        transition: all 0.3s ease-in-out;
    }}
    #inspo-quote {{
        position: fixed;
        bottom: 12px;
        right: 18px;
        font-size: 14px;
        font-style: italic;
        color: #ffffffcc;
        background: rgba(0,0,0,0.25);
        padding: 6px 12px;
        border-radius: 8px;
        z-index: 999;
        pointer-events: none;
    }}
    </style>
    <div id="inspo-quote">“Where words fail, music speaks.” 🎧</div>
    """
    st.markdown(css, unsafe_allow_html=True)

set_local_background("wallpaper.jpg")

# app title
st.title("🎵 Music app (Live Streaming)")
# Search box
query = st.text_input("Search for a song:", "")

if query:
    st.info("Searching on YouTube...")

    # Search top 5 results using yt-dlp
    ydl_opts_search = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,  # Only get info, no download
    }
    with YoutubeDL(ydl_opts_search) as ydl:
        search_results = ydl.extract_info(f"ytsearch5:{query}", download=False)['entries']

    if search_results:
        st.subheader("Results:")
        for i, video in enumerate(search_results):
            st.write(f"{i+1}. {video['title']}")

            if st.button(f"Play '{video['title']}'", key=f"play{i}"):
                st.info("Fetching live audio stream...")

                # Extract the direct audio URL
                ydl_opts_audio = {
                    'format': 'bestaudio/best',
                    'quiet': True,
                    'nocheckcertificate': True,
                    'cookies': 'cookies.txt'
                }
                with YoutubeDL(ydl_opts_audio) as ydl:
                    info = ydl.extract_info(video['url'], download=False)
                    audio_url = info['url']  # Direct streaming URL

                # Play the audio directly from URL
                st.audio(audio_url)

                # Optional: provide the original YouTube link to open in browser
                st.markdown(f"[Open on YouTube]({video['url']})")
    else:
        st.warning("No results found.")

with st.sidebar:


    st.sidebar.title("About this App...")
st.sidebar.markdown("""
  
This is a music player app that streams audio directly from YouTube.  
It supports live playback from links and is designed for demo purposes.

**Features:**
- search and play songs which stream directly from YouTube.
- No Ads and open-source.                    
- More features coming soon...                                         

**Credits:**  
- 👨‍💻 Developed and Designed by: Ansh Kunwar   
- ⚙️ Built with: Streamlit + yt-dlp
- 🖼️ Animation by: LottieFiles
- 🧠 [App Source Code](https://github.com/anshk1234/Music-player)
- 📧 contact: anshkunwar3009@gmail.com                  
- 🌐 see other projects: [streamlit.io/ansh kunwar](https://share.streamlit.io/user/anshk1234)
                    
""")


# ---- Footer ----
st.markdown("<p style='text-align:center; color:white;'>© 2025 Music App | Powered by Youtube Streaming</p>", unsafe_allow_html=True)




