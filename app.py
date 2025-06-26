import streamlit as st
from pytube import YouTube
import os
from moviepy.editor import AudioFileClip

st.set_page_config(page_title="AKP.ytdl", page_icon="🎬")

st.title("🎬 Ydl By AKP")
st.markdown("Download **MP4** (Video) or **MP3** (Audio) from any YouTube link.")

# Input
url = st.text_input("🔗 Enter YouTube URL:")

format_choice = st.radio("Choose format:", ["MP4 (Video)", "MP3 (Audio)"])
download_button = st.button("Download")

if url and download_button:
    try:
        yt = YouTube(url)
        title = yt.title
        st.success(f"Video Title: {title}")

        # For MP4
        if format_choice == "MP4 (Video)":
            stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
            if stream:
                st.info("Downloading MP4...")
                stream.download(filename="video.mp4")
                with open("video.mp4", "rb") as f:
                    st.download_button("📥 Download MP4", f, file_name=f"{title}.mp4", mime="video/mp4")
                os.remove("video.mp4")
            else:
                st.error("No MP4 stream available.")

        # For MP3
        elif format_choice == "MP3 (Audio)":
            st.info("Downloading and converting to MP3...")
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_stream.download(filename="audio.mp4")
            audioclip = AudioFileClip("audio.mp4")
            audioclip.write_audiofile("audio.mp3")
            audioclip.close()
            with open("audio.mp3", "rb") as f:
                st.download_button("🎧 Download MP3", f, file_name=f"{title}.mp3", mime="audio/mpeg")
            os.remove("audio.mp4")
            os.remove("audio.mp3")

    except Exception as e:
        st.error(f"❌ Error: {e}")
