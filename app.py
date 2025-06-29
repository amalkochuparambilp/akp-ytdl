import streamlit as st

st.set_page_config(page_title="AKP Downloader", page_icon="🌀")

st.title("🌀 Welcome to AKP Downloader")

st.markdown("Choose a downloader:")

if st.button("🎬 YouTube Downloader"):
    st.switch_page("1_Home")

if st.button("📸 Instagram Reels Downloader"):
    st.switch_page("2_Instagram")