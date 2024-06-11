
#install SpeechRecognition, pip, gtts, soundevice wavio, pyttsx3, pydub, ffmpeg

from gtts import gTTS
import os
import datetime
import speech_recognition as sr
import sounddevice as sd
import wavio
import webbrowser
from pydub import AudioSegment


def speak(audio):
    tts = gTTS(text=audio, lang='en')
    tts.save("audio.mp3")
    os.system("afplay audio.mp3")

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("I am Bex. What can I do for you?")

def record_audio(duration, fs=44100):
    print("Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    wavio.write("audio.wav", audio, fs, sampwidth=2)
    print("Recording complete")

def convert_wav_to_flac(input_wav, output_flac):
    audio = AudioSegment.from_wav(input_wav)
    audio.export(output_flac, format="flac")

def takeCommand():
    record_audio(5)  
    convert_wav_to_flac("audio.wav", "audio.flac")

    r = sr.Recognizer()
    with sr.AudioFile('audio.flac') as source:
        audio = r.record(source) 
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Repeat that please")
        return "None"
    return query
    

def openGoogle():
    webbrowser.open_new_tab("http://www.google.com")

def openSafari():
    os.system("open -a Safari")


def sortCommand(command):
     if command:
        command = command.lower()
        if "google" in command:
            openGoogle()
        elif "safari" in command:
            openSafari()
        elif "bye" in command or "quit" in command:
            speak("Bye")
            return True
        else:
            speak("I did not understand that. Please try again.")
        return False


def main():
    wishMe()
    while True:
        command = takeCommand()
        if sortCommand(command):
            break

if __name__ == "__main__":
    main()

"""
#install SpeechRecognition, pip, , pyttsx3
import pyttsx3
import datetime
import speech_recognition as sr
from gtts import gTTS


engine = pyttsx3.init("nsss")
voices = engine.getProperty("voices")
#print(voices[0].id)
engine.setProperty("voice", voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")

    speak("I am Bex. What can I do for you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognising...")
        query = r.recognise_google(audio, language = "en-in")
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)
        print("Repeat that please")
        return "None"
    return query
    

if __name__ == "__main__":
    wishMe()
    takeCommand()
"""


