import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="AKP YTDL", page_icon="🎬")
st.title("🎬 YTDL BY AKP (MP4 & MP3)")

url = st.text_input("🔗 Enter YouTube URL:")
format_choice = st.radio("Choose format:", ["MP4 (Video)", "MP3 (Audio)"])
download_button = st.button("Download")

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
        os.remove(filename)

    except Exception as e:
        st.error(f"Error: {e}")