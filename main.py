# music_player_live.py
import streamlit as st
from yt_dlp import YoutubeDL

# ---- Page Configuration ----
st.set_page_config(page_title=" Music Player ", page_icon="🎵")




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
                    'noplaylist': True,
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
- 🧠 [App Source Code](https://github.com/anshk1234/Music-player)
- 📧 contact: anshkunwar3009@gmail.com                  
- 🌐 see other projects: [streamlit.io/ansh kunwar](https://share.streamlit.io/user/anshk1234)
                    
""")


# ---- Footer ----
st.markdown("<p style='text-align:center; color:white;'>© 2025 Music App | Powered by Youtube Streaming</p>", unsafe_allow_html=True)


