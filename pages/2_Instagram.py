import streamlit as st
import yt_dlp
import os
from datetime import datetime

st.set_page_config(page_title="Instagram Downloader", page_icon="📸")
st.title("📸 Instagram Reels Downloader by AKP")

insta_url = st.text_input("🔗 Enter Instagram Reels URL:")
insta_format = st.radio("Choose format:", ["MP4 (Video)", "MP3 (Audio)"])
insta_button = st.button("Download Reel")

if "insta_log" not in st.session_state:
    st.session_state.insta_log = []

def download_instagram(url, is_audio):
    ydl_opts = {
        'quiet': True,
        'outtmpl': 'insta.%(ext)s',
    }

    if is_audio:
        ydl_opts.update({
            'format': 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        })
        filename = 'insta.mp3'
        mime = 'audio/mpeg'
    else:
        ydl_opts.update({'format': 'best'})
        filename = 'insta.mp4'
        mime = 'video/mp4'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return filename, mime

if insta_url and insta_button:
    try:
        is_audio = (insta_format == "MP3 (Audio)")
        st.info("Downloading reel...")
        filename, mime = download_instagram(insta_url, is_audio)

        with open(filename, "rb") as f:
            st.download_button(
                label=f"⬇️ Download {insta_format.split()[0]}",
                data=f,
                file_name=filename,
                mime=mime
            )

        # Add to download log
        st.session_state.insta_log.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "url": insta_url,
            "type": insta_format,
            "status": "✅ Success"
        })

        os.remove(filename)

    except Exception as e:
        st.error(f"❌ Failed to download: {e}")
        st.session_state.insta_log.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "url": insta_url,
            "type": insta_format,
            "status": f"❌ Failed - {str(e)}"
        })

# Show logs
st.subheader("📜 Reels Download Log")
for entry in reversed(st.session_state.insta_log[-10:]):
    st.markdown(
        f"{entry['time']} | {entry['type']} | "
        f"[{entry['url']}]({entry['url']}) | {entry['status']}"
    )