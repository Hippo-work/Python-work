import streamlit as st

st.title("Multi Dropdown")

section = st.selectbox("Choose a module", ["Page 1", "Page 2", "Page 3"])

if section == "1":
    st.subheader("123 🐾")
    # Your image enhancer code

elif section == "2":
    st.subheader("234 💥")
    # Your stylization code

elif section == "3":
    st.subheader("345 🤣")
    # Your dreamy edits
