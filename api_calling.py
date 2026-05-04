from google import genai
from dotenv import load_dotenv
import os
from gtts import gTTS
import streamlit as st
#loading the environment variable
load_dotenv()
import io
my_api_key=os.getenv("GEMINI_API_KEY")

#initializing the api key
client=genai.Client(api_key=my_api_key)

def note_generator(images):
    prompt="""Summarize the pictures in note format at max 120 words
              make sure to add necessary markdown to differentiate different section"""
    
    response=client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[images,prompt]
    )
    
    return response.text 

def audio_transcription(text):
    speech=gTTS(text,lang='en',slow=False)
   # speech.save("welcome.mp3")
    audio_buffer=io.BytesIO()
    speech.write_to_fp(audio_buffer)
    return audio_buffer

def quize_generator(image,difficulty):
    prompt=f"""Generate the three quizes based on {difficulty} use necessary markdown to differentiate the different options
                add corrrect answer too at the end"""
    
    response=client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[image,prompt]
    )
    
    return response.text 
    
