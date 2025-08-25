import streamlit as st

st.title("Creative Lab 🎨")

section = st.selectbox("Choose a module", ["Anime Editor", "Pop Art Filters", "Fantasy Overlay"])

if section == "Anime Editor":
    st.subheader("Anime Pet Companion 🐾")
    # Your image enhancer code

elif section == "Pop Art Filters":
    st.subheader("Pop Artify Your Image 💥")
    # Your stylization code

elif section == "Fantasy Overlay":
    st.subheader("Fantasy Style Generator 🧚")
    # Your dreamy edits
