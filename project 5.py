import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
news_api_key = os.getenv("NEWS_API_KEY")

client= OpenAI(api_key=openai_api_key)



# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init() 
newsapi = ("NEWS_API_KEY")


def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

def aiProcess(command):
    client = OpenAI(api_key=openai_api_key)

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "news" in c.lower():
         get_news()    
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    


def get_news():
    try:
        url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            speak("Sorry, I could not get the news.")
            return

        parts = response.text.split("<item>")

        if len(parts) <= 1:
            speak("Sorry, I could not find any news.")
            return

        speak("Here are the latest news headlines from India.")

        count = 0

        for part in parts[1:]:
            if "<title>" in part and "</title>" in part:
                title = part.split("<title>")[1].split("</title>")[0]
                title = title.replace("&amp;", "&")

               
                speak(title)

                count += 1

                if count == 5:
                    break


    except Exception as e:
        print("News error:", e)
        speak("Sorry, I could not get the latest news.")


def processCommand(c):

    if "open google" in c.lower():
        webbrowser.open("https://google.com")

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")

    elif "news" in c.lower():
        get_news()


    else:
        # Let OpenAI handle the request
     output = aiProcess(c)
     speak(output) 





if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Ya")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))


