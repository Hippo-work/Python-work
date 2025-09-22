import streamlit as st
st.title("🛠️ Shell Script Editor")
uploaded_file = st.file_uploader("Upload your .sh script", type="sh")

if uploaded_file and "lines" not in st.session_state:
    content = uploaded_file.read().decode("utf-8")
    st.session_state.lines = content.splitlines()

if "delete_index" not in st.session_state:
    st.session_state.delete_index = None

if "lines" in st.session_state:
    # st.write(lines)

    #edit lines
    edited_lines = []
    st.subheader("Edit Script Lines")
    for i, line in enumerate(st.session_state.lines):
        col1, col2 = st.columns([10,1], vertical_alignment="bottom")
        with col1:
            st.session_state.lines[i] = st.text_input(f"Line {i}", value=line, key=f"line_{i}")
        with col2:
            if st.button("❌", key=f"delete_{i}"):
                st.session_state.lines.pop(i)
                st.rerun()

    if st.button("➕ Add Line"):
        st.session_state.lines.append("")
        st.rerun()

    script_text = "\n".join(st.session_state.lines)
    st.download_button(
        label="💾 Download .sh File",
        data=script_text,
        file_name="Edited_" + uploaded_file.name,
        mime="text/x-shellscript"
    )

