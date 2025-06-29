import streamlit as st
from streamlit.source_util import get_pages

st.set_page_config(page_title="AKP Downloader", page_icon="🌀")

st.title("🌀 Welcome to AKP Downloader")
st.markdown("Choose a downloader:")

# 👇 Debug page detection
st.write("🧭 Pages detected by Streamlit:")
for key, page in get_pages("").items():
    st.write(f"➡️ {page['page_name']} — key: {key}")

# 👇 Buttons
if st.button("🎬 YouTube Downloader"):
    st.switch_page("1_Home")

if st.button("📸 Instagram Reels Downloader"):
    st.switch_page("2_Instagram")