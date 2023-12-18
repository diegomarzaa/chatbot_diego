from gtts import gTTS
import streamlit as st
import time
import pygame
from playsound import playsound

pygame.mixer.init()

def create_audio(text, filename='audio.mp3', language='es'):
    audio = gTTS(text=text, lang=language, slow=False)
    audio.save(filename)
    return filename

def play_audio2(filename='audio.mp3'):
    html_string = """
            <audio controls autoplay>
              <source src="https://www.orangefreesounds.com/wp-content/uploads/2022/04/Small-bell-ringing-short-sound-effect.mp3" type="audio/mp3">
            </audio>
            """

    sound = st.empty()
    sound.markdown(html_string, unsafe_allow_html=True)  # will display a st.audio with the sound you specified in the "src" of the html_string and autoplay it
    time.sleep(2)  # wait for 2 seconds to finish the playing of the audio
    sound.empty()  # optionally delete the element afterwards

def play_audio3(filename='audio.mp3'):
    playsound('audio.mp3')

def play_audio(filename='audio.mp3'):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

def stop_audio():
    pygame.mixer.music.stop()