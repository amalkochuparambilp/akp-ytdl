import streamlit as st
import yt_dlp
import os
from datetime import datetime

st.set_page_config(page_title="AKP YTDL", page_icon="🎬")
st.title("🎬 YTDL BY AKP (MP4 & MP3)")

url = st.text_input("🔗 Enter YouTube URL:")
format_choice = st.radio("Choose format:", ["MP4 (Video)", "MP3 (Audio)"])
download_button = st.button("Download")

# Initialize session state log
if "download_log" not in st.session_state:
    st.session_state.download_log = []

def download_video(url, is_audio):
    ydl_opts = {
        'outtmpl': 'download.%(ext)s',
        'quiet': True
    }

    if is_audio:
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        })
        filename = 'download.mp3'
        mime = 'audio/mpeg'
    else:
        ydl_opts.update({'format': 'best'})
        filename = 'download.mp4'
        mime = 'video/mp4'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return filename, mime

if url and download_button:
    try:
        is_audio = (format_choice == "MP3 (Audio)")
        st.info("Processing download...")
        filename, mime = download_video(url, is_audio)

        with open(filename, "rb") as f:
            st.download_button(
                label=f"⬇️ Download {format_choice.split()[0]}",
                data=f,
                file_name=filename,
                mime=mime
            )

        # Log the download
        log_entry = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "url": url,
            "type": format_choice,
            "status": "✅ Success"
        }
        st.session_state.download_log.append(log_entry)
        os.remove(filename)

    except Exception as e:
        st.error(f"Error: {e}")
        log_entry = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "url": url,
            "type": format_choice,
            "status": f"❌ Failed - {str(e)}"
        }
        st.session_state.download_log.append(log_entry)

# Show download log
st.subheader("📜 Download Log")
for entry in reversed(st.session_state.download_log[-10:]):  # Show last 10 entries
    st.markdown(
        f"{entry['time']} | {entry['type']} | [{entry['url']}]({entry['url']}) | {entry['status']}"
    )