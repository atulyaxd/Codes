from __future__ import print_function
from os import path
import os.path
from urllib.parse import quote
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import io
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import time
import wolframalpha
import requests
import pywhatkit

engine = pyttsx3.init()
engine.setProperty("rate",178)#speed of speech
voices = engine.getProperty('voices')
print(voices[1].id)
engine.setProperty('voice', voices[1].id)

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
def drive():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    path = "idea-drive.json" #relative path
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=1, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    filei=[]
    filen = []
    for item in items:
        filei.append(item['id'])
        filen.append(item['name'])
    file_id = ("".join(filei))
    filename= ("".join(filen))
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    print ("Download %d%%." % int(status.progress() * 100))
    speak("Downloaded")

def pomodoror():
    speak("Pomodoro starts now! focus for 25 minutes play for 5 minutes")
    for i in range(4):
        t = 25*60
        while t: 
            mins = t // 60 
            secs = t % 60
            timer = '{:02d}:{:02d}'.format(mins, secs) 
            print(timer, end="\r") # overwrite previous line 
            time.sleep(1)
            t -= 1 
        speak("Break Time!!")

        t = 5*60 
        while t: 
            mins = t // 60 
            secs = t % 60
            timer = '{:02d}:{:02d}'.format(mins, secs) 
            print(timer, end="\r") # overwrite previous line 
            time.sleep(1)
            t -= 1 
        speak("Work Time!!")

def summary(query):
    topic = query.replace("wikipedia","")
    results=wikipedia.summary(topic, sentences=2)
    speak(results)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r=sr.Recognizer()
    my_mic_device = sr.Microphone()
    with my_mic_device as source:
            #speak("Listening")
            audio = r.listen(source)

    try:
        query = r.recognize_google(audio)
        print(query)
    
    except:
        exit()
    return query

def commands():
    query = takeCommand().lower()
    if "how are you" in query:
        speak("I'm fine, how about you")

    elif "test" in query:
        speak("downloading test files")
        drive()

    elif "study" in query:
        pomodoror()

    elif "who was" in query:
        query = query.replace("who was","")
        summary(query)

    elif "who is" in query:
        query = query.replace("who is","")
        summary(query)

    elif "exit" in query:
        exit()

if __name__ == "__main__":    
    while True:
        try:
            commands()
        except:
            speak("i ran into an error. kindly retry in a while.")
            exit()