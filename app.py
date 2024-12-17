import streamlit as st
import wikipediaapi
import webbrowser
from gtts import gTTS
from pydub import AudioSegment
import os
from wolframalpha import Client

# Konfigurasi Streamlit
st.set_page_config(page_title="Voice Assistant", layout="centered")

# Fungsi untuk berbicara
def assistant_speaks(output):
    st.markdown(f"**Assistant:** {output}")
    tts = gTTS(text=output, lang='id', slow=False)
    file_name = "response.mp3"
    tts.save(file_name)
    audio = AudioSegment.from_mp3(file_name)
    st.audio(file_name, format="audio/mp3")
    os.remove(file_name)

# Fungsi pencarian Wikipedia
def search(query):
    wiki = wikipediaapi.Wikipedia(language="en")
    page = wiki.page(query)
    if page.exists():
        summary = page.summary[:500]
        assistant_speaks(f"Here is the summary for {query}: {summary}")
    else:
        assistant_speaks(f"Sorry, I couldn't find a Wikipedia page for {query}.")

# Fungsi membuka website
def open_website(site_name):
    sites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "github": "https://www.github.com",
        "facebook": "https://www.facebook.com"
    }
    url = sites.get(site_name.lower(), f"https://{site_name.lower()}.com")
    assistant_speaks(f"Opening {site_name}.")
    webbrowser.open(url)

# Fungsi kalkulasi
def calculate(query):
    try:
        app_id = "V388XG-H2YTQW2J59"  # Ganti dengan App ID WolframAlpha Anda
        client = Client(app_id)
        res = client.query(query)
        answer = next(res.results).text
        assistant_speaks(f"The answer is {answer}")
    except Exception as e:
        assistant_speaks("I couldn't calculate that, please try again.")

# UI Streamlit
st.title("Voice Assistant")
st.markdown("Type your command below:")

user_input = st.text_input("Enter your command:", "")
if st.button("Submit"):
    if "search" in user_input:
        query = user_input.replace("search", "").strip()
        if query:
            search(query)
        else:
            assistant_speaks("Please specify what to search.")
    elif "open" in user_input:
        site_name = user_input.replace("open", "").strip()
        if site_name:
            open_website(site_name)
        else:
            assistant_speaks("Please specify the website.")
    elif "calculate" in user_input:
        query = user_input.replace("calculate", "").strip()
        if query:
            calculate(query)
        else:
            assistant_speaks("Please specify what to calculate.")
    else:
        assistant_speaks("I'm not sure how to respond to that.")
