import streamlit as st

st.set_page_config(
    page_title="AKP DL",
    page_icon="📥",
    layout="centered",
    initial_sidebar_state="auto",
)

st.title("🌀 Welcome to AKP Downloader")
st.markdown("Choose a downloader:")

if st.button("🎬 YouTube Downloader"):
    st.switch_page("1_Home")

if st.button("📸 Instagram Reels Downloader"):
    st.switch_page("2_Instagram")