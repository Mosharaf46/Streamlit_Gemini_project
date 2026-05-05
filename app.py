import streamlit as st
from api_calling import note_generator, audio_transcription, quize_generator
from PIL import Image

# Title
st.title("Note Summary and Quiz Generator", anchor=False)
st.markdown("Upload at most 3 images to generate a Note Summary and Quizzes")
st.divider()

# Sidebar
with st.sidebar:
    images = st.file_uploader(
        "Upload the photos of your notes",
        type=["jpg", "png", "jpeg"],
        accept_multiple_files=True
    )

    pil_images = []
    if images:
        if len(images) > 3:
            st.error("Upload at most 3 images")
        else:
            pil_images = [Image.open(img) for img in images]
            st.subheader("Uploaded Images")
            cols = st.columns(len(images))
            for i, img in enumerate(images):
                with cols[i]:
                    st.image(img)

    selected_option = st.selectbox(
        "Select the difficulty level of quizzes",
        ("Easy", "Medium", "Hard"),
        index=None
    )

    pressed = st.button("Click to initiate AI", type="primary")

# Main logic
if pressed:
    if not images:
        st.error("You must upload at least 1 photo")
    elif len(images) > 3:
        st.error("Upload at most 3 images")
    elif not selected_option:
        st.error("You must select a difficulty level")
    else:
        # Note generation
        with st.container(border=True):
            st.subheader("Your Note", anchor=False)
            with st.spinner("Generating Notes..."):
                generated_notes = note_generator(pil_images)
                st.markdown(generated_notes)

        # Audio transcription
        with st.container(border=True):
            st.subheader("Audio Transcription", anchor=False)
            with st.spinner("Generating audio transcription..."):
                clean_notes = generated_notes.replace("#", "").replace("*", "").replace("-", "").replace(",", "")
                audio_bytes = audio_transcription(clean_notes)
                st.audio(audio_bytes)

        # Quiz generation
        with st.container(border=True):
            st.subheader(f"Quiz ({selected_option}) Difficulty", anchor=False)
            with st.spinner("Generating quizzes..."):
                quizes = quize_generator(pil_images, selected_option)
                st.markdown(quizes)
