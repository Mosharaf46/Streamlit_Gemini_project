import streamlit as st 
from api_calling import note_generator,audio_transcription,quize_generator
from PIL import Image
from gtts import gTTS


#title
st.title("Note Summary and Quize Generator",anchor=False)
st.markdown("Upload atmax 3 images to generate note Summary and Quizes")
st.divider()
#images
with st.sidebar:
    images=st.file_uploader("Upload the photos of your notes"
                     ,type=["jpg","png","jpeg"],accept_multiple_files=True)
    
    pil_image=[Image.open(img) for img in images]
    
    if images:
        if len(images)>3:
            st.error("Upload at max 3 images")
        else:
            st.subheader("Uploaded images")
            col=st.columns(len(images))
            for i,img in enumerate(images):
                with col[i]:
                    st.image(img)
        
    selected_option=st.selectbox("Select the difficality level of quizes",
                                 ("Easy","Medium","Hard"),index=None)

    
    pressed=st.button("Clicked to initiate Ai",type="primary")

if pressed:
    
    if not images:
        st.error("You must upload atleast 1 photo")
    if not selected_option:
        st.error("You must select a difficulity")
    
    if images and selected_option:
        #note 
        with st.container(border=True):
            st.subheader("Your Note",anchor=False)
            
            with st.spinner("Generating Notes..."):
                generated_notes=note_generator(pil_image)
                st.markdown(generated_notes)
            
            
        #audio transcription
        
        with st.container(border=True):
            st.subheader("Audio Transcription",anchor=False)
            with st.spinner("Generating audio transcription..."):
                #clearing markdown
                generated_notes=generated_notes.replace("#","")
                generated_notes=generated_notes.replace("*","")
                generated_notes=generated_notes.replace("-","")
                generated_notes=generated_notes.replace(",","")
                audio_transcription=audio_transcription(generated_notes)
                st.audio(audio_transcription)
            
        #quize 
        
        with st.container(border=True):
            st.subheader(f"Quize({selected_option}) Difficulty",anchor=False)
            with st.spinner("Generating quizes..."):
                quizes=quize_generator(pil_image,selected_option)
                st.markdown(quizes)
        