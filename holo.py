# Gemini Voice Assistant
#
# This program listens for a specific key press ('a'), records an audio command,
# sends it to the Gemini Flash model for a response, and then uses text-to-speech
# to voice the reply.
#
# Author: Gemini
# Date: 2024-05-21

# --- Installation ---
# Before running, you need to install the required Python libraries.
# Open your terminal or command prompt and run the following command:
# pip install google-generativeai speechrecognition keyboard gtts playsound==1.2.2 PyAudio

import os
import google.generativeai as genai
import speech_recognition as sr
import keyboard
from gtts import gTTS
from playsound import playsound

# --- Configuration ---
# IMPORTANT: Replace "YOUR_API_KEY" with your actual Google API key.
# You can get an API key from Google AI Studio.
GOOGLE_API_KEY = "AIzaSyD0KRgGK9SPt67KS_F_fFdzTHjxaLS-gNU"

genai.configure(api_key=GOOGLE_API_KEY)


# --- Model and TTS Configuration ---
MODEL_NAME = "gemini-1.5-flash"
TTS_LANGUAGE = "en"  # Language for the Google Text-to-Speech
OUTPUT_FILENAME = "response.mp3"

# --- Initialize Gemini Model ---
# Add a system instruction to guide the AI's behavior
system_instruction = "You are a helpful and friendly AI assistant. Your goal is to provide accurate, concise, and useful information to the user's voice commands."
model = genai.GenerativeModel(
    MODEL_NAME,
    system_instruction=system_instruction
)
chat = model.start_chat(history=[])

# --- Text-to-Speech Function ---
def speak(text):
    """
    Converts text to speech using Google's Text-to-Speech service (gTTS) and plays it.
    """
    print("🤖 Speaking...")
    try:
        # Create a gTTS object
        tts = gTTS(text=text, lang=TTS_LANGUAGE, slow=False)
        # Save the audio file
        tts.save(OUTPUT_FILENAME)

        # Use playsound to play the generated audio file
        playsound(OUTPUT_FILENAME)
    except Exception as e:
        print(f"Error during text-to-speech: {e}")
    finally:
        # Clean up the audio file after playing
        if os.path.exists(OUTPUT_FILENAME):
            os.remove(OUTPUT_FILENAME)

# --- Speech Recognition Function ---
def listen_for_command():
    """
    Captures audio from the microphone and converts it to text using
    Google's Web Speech API.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Listening... (press 'a' to start)")
        # Adjust for ambient noise to improve recognition accuracy
        recognizer.adjust_for_ambient_noise(source)
        try:
            # The wait_for function waits for the key press before listening
            keyboard.wait('a')
            print("🔴 Recording...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            print("👂 No speech detected. Please try again.")
            return ""

    try:
        print("🔍 Recognizing speech...")
        # Recognize speech using Google Web Speech API
        command = recognizer.recognize_google(audio)
        print(f"👤 You said: {command}")
        return command
    except sr.UnknownValueError:
        print("🤔 Sorry, I could not understand the audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

# --- Main Application Logic ---
def main():
    """
    The main function that runs the assistant's loop.
    """
    print("🚀 Gemini Voice Assistant is running.")
    print("Press the 'a' key firmly when you want to speak your command.")

    while True:
        command = listen_for_command()

        if command:
            try:
                print("🧠 Gemini is thinking...")
                # Send the user's command to the Gemini model
                response = chat.send_message(command)
                bot_response_text = response.text
                print(f"🤖 Gemini: {bot_response_text}")

                # Speak the response
                speak(bot_response_text)
            except Exception as e:
                print(f"An error occurred while interacting with Gemini: {e}")
                error_message = "I'm sorry, I encountered an error while processing your request."
                speak(error_message)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Assistant stopped by user. Goodbye!")
    except Exception as e:
        # This will catch errors like permission denied for keyboard listener
        print(f"\nA critical error occurred: {e}")
        print("If you are on Linux, you may need to run this script with sudo.")

