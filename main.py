import speech_recognition as sr
import pyttsx3
import pywhatkit
import pyautogui
import webbrowser
import datetime
import requests
import time
import os
import openai

# Initialize Text-to-Speech
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Change index for different voices
engine.setProperty('rate', 150)  # Speed of speech

import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="")  # Replace with your Gemini API key
model = genai.GenerativeModel('gemini-pro')

def speak(text):
    """Make JARVIS speak the given text"""
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Listen for voice commands using the microphone"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in').lower()
        print(f"You: {query}\n")
        return query
    except Exception as e:
        speak("Sorry, I didn't catch that. Can you repeat?")
        return ""

def greet():
    """Greet the user based on time of day"""
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        speak("Good morning! MASTER")
    elif 12 <= hour < 18:
        speak("Good afternoon! MASTER")
    else:
        speak("Good evening! MASTER")
    speak("I am JARVIS. How can I assist you today?")

def execute_command(query):
    """Execute tasks based on voice commands"""
    if 'open youtube' in query:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
        
    elif 'open google' in query:
        speak("Opening Google")
        webbrowser.open("https://google.com")
        
    elif 'search' in query:
        search_query = query.replace('search', '').strip()
        if search_query:
            speak(f"Searching for {search_query}")
            pywhatkit.search(search_query)
        else:
            speak("What would you like me to search?")
            
    elif 'play' in query:
        song = query.replace('play', '').strip()
        if song:
            speak(f"Playing {song}")
            pywhatkit.playonyt(song)
        else:
            speak("What song would you like to play?")
            
    elif 'time' in query:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"It's {current_time}")
        
    elif 'shutdown' in query:
        speak("Shutting down the system in 10 seconds")
        time.sleep(10)
        os.system("shutdown /s /t 1" if os.name == 'nt' else "shutdown -h now")
        
    elif 'restart' in query:
        speak("Restarting the system")
        os.system("shutdown /r /t 1" if os.name == 'nt' else "reboot")
        
    elif 'screenshot' in query:
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        speak("Screenshot saved")
        
    elif 'weather' in query:
        api_key = ""  # Get from https://openweathermap.org
        speak("Which city?")
        city = take_command()
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(weather_url)
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            speak(f"It's {temp}°C in {city}")
        else:
            speak("Couldn't fetch weather data")
            
    elif 'exit' in query or 'quit' in query:
        speak("Goodbye!")
        exit()
        
    elif 'ask gpt' in query or 'chatgpt' in query:
        question = query.replace('ask gpt', '').replace('chatgpt', '').strip()
        if question:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": question}]
                )
                answer = response.choices[0].message.content
                speak(answer)
            except Exception as e:
                speak("Sorry, I couldn't get a response from ChatGPT")
        else:
            speak("What would you like to ask ChatGPT?")
            
    else:
        speak("I don't understand that command yet")

if __name__ == "__main__":
    greet()
    while True:
        query = take_command()
        if query:
            execute_command(query)