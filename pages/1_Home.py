import streamlit as st
import yt_dlp
import os
from datetime import datetime

st.set_page_config(page_title="YouTube Downloader", page_icon="🎬")
st.title("🎬 YTDL BY AKP (MP4 & MP3)")

url = st.text_input("🔗 Enter YouTube URL:")
format_choice = st.radio("🎞️ Choose format:", ["MP4 (Video)", "MP3 (Audio)"])
download_button = st.button("Download")

if "download_log" not in st.session_state:
    st.session_state.download_log = []

def get_video_info(url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return {
        'title': info.get('title'),
        'thumbnail': info.get('thumbnail'),
        'uploader': info.get('uploader'),
        'duration': info.get('duration'),
        'webpage_url': info.get('webpage_url')
    }

def download_video(url, is_audio):
    ydl_opts = {
        'outtmpl': 'download.%(ext)s',
        'quiet': True,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
    }

    if is_audio:
        ydl_opts.update({
            'format': 'bestaudio[ext=m4a]/bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        })
        filename = 'download.mp3'
        mime = 'audio/mpeg'
    else:
        filename = 'download.mp4'
        mime = 'video/mp4'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return filename, mime

# Show video preview
if url:
    try:
        info = get_video_info(url)
        st.subheader("📺 Video Preview")
        st.image(info['thumbnail'], width=480)
        st.markdown(f"**Title:** {info['title']}")
        st.markdown(f"**Channel:** {info['uploader']}")
        mins, secs = divmod(info['duration'], 60)
        st.markdown(f"**Duration:** {mins}:{secs:02d}")
        st.markdown(f"[🔗 Watch on YouTube]({info['webpage_url']})")
    except Exception as e:
        st.warning(f"Could not fetch video info: {e}")

# Handle download
if url and download_button:
    try:
        is_audio = (format_choice == "MP3 (Audio)")
        st.info("⏳ Downloading...")
        filename, mime = download_video(url, is_audio)

        with open(filename, "rb") as f:
            st.download_button(
                label=f"⬇️ Download {format_choice.split()[0]}",
                data=f,
                file_name=filename,
                mime=mime
            )

        st.session_state.download_log.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "url": url,
            "type": format_choice,
            "status": "✅ Success"
        })

        os.remove(filename)

    except Exception as e:
        st.error(f"❌ Download failed: {e}")
        st.session_state.download_log.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "url": url,
            "type": format_choice,
            "status": f"❌ Failed - {str(e)}"
        })

# Show log
st.subheader("📜 Download Log")
for entry in reversed(st.session_state.download_log[-10:]):
    st.markdown(
        f"{entry['time']} | {entry['type']} | "
        f"[{entry['url']}]({entry['url']}) | {entry['status']}"
    )