
# install venv, SpeechRecognition, pip, gtts, soundevice wavio
# pyttsx3, pydub, ffmpeg, vosk, wget, pyautogui + pillow, pynput


from vosk import Model, KaldiRecognizer
import json
import wave
from gtts import gTTS
import os
import datetime
import sounddevice as sd
import wavio
import webbrowser
import pyautogui
import time
from pynput import keyboard

vosk_model_path = "/Users/juliebelfor/Documents/Ai-Helper/Ai-Helper/vosk-model-small-en-us-0.15"

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

def verify_audio_file(filepath):
    try:
        wf = wave.open(filepath, "rb")
        channels = wf.getnchannels()
        rate = wf.getframerate()
        print(f"Audio file properties: Channels = {channels}, Sample Rate = {rate}")
        if channels != 1 or rate != 16000:
            raise ValueError("Audio file must be mono and have a sample rate of 16000")
        wf.close()
        return True
    except Exception as e:
        print(f"Audio file verification failed: {e}")
        return False

def recognize_speech():
    wf = wave.open("audio.wav", "rb")
    if wf.getnchannels() != 1:
        raise ValueError("Audio file must be mono")
    if wf.getframerate() != 16000:
        raise ValueError("Sample rate must be 16000")

    print("Loading Vosk model...")
    model = Model(vosk_model_path)
    rec = KaldiRecognizer(model, wf.getframerate())
    print("Vosk model loaded")

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            break

    result = rec.FinalResult()
    result_json = json.loads(result)
    recognized_text = result_json.get('text', '')
    print(f"Recognized speech: {recognized_text}")
    return recognized_text

def openGoogle():
    webbrowser.open_new_tab("https://www.google.com/?safe=active&ssui=on")
    time.sleep(5)

def type_in_google(query):
    time.sleep(2)
    pyautogui.write(query)
    pyautogui.press('enter')

def openSafari():
    webbrowser.get("safari").open("https://www.google.com")
    time.sleep(5)

def searchInSafari(query):
    time.sleep(2)
    pyautogui.write(query)
    pyautogui.press('enter')

def sortCommand(recognized_text):
    if recognized_text:
        print(f"Received command: {recognized_text}")
        recognized_text = recognized_text.lower()
        if "google" in recognized_text or "look up" in recognized_text:
            openGoogle()
            search_query = recognized_text.replace("google", "").replace("look up", "").strip()
            if search_query:
                type_in_google(search_query)
        elif "safari" in recognized_text:
            search_query = recognized_text.replace("safari", "").strip()
            openSafari()
            if search_query:
                searchInSafari(search_query)
        elif "goodbye" in recognized_text or "quit" in recognized_text:
            speak("Bye")
            return True
        else:
            speak("I did not understand that. Please try again.")
    return False

class EscKeyPressed:
    def __init__(self):
        self.recording = False
        self.audio = None

    def on_press(self, key):
        if key == keyboard.Key.esc:
            if not self.recording:
                print("Start recording...")
                self.recording = True
                self.audio = sd.rec(int(5 * 16000), samplerate=16000, channels=1, dtype='int16')

    def on_release(self, key):
        if key == keyboard.Key.esc:
            if self.recording:
                print("Stop recording...")
                self.recording = False
                sd.stop()
                wavio.write("audio.wav", self.audio, 16000, sampwidth=2)
                recognized_text = recognize_speech()
                sortCommand(recognized_text)

def main():
    wishMe()
    keyClickAlert = EscKeyPressed()
    listener = keyboard.Listener(on_press=keyClickAlert.on_press, on_release=keyClickAlert.on_release)
    listener.start()
    listener.join()

if __name__ == "__main__":
    main()

