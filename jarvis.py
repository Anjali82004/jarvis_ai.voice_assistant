import webbrowser
import smtplib
import pyttsx3
import speech_recognition as sr
import pywhatkit
import datetime
import os
from openai import OpenAI
from dotenv import load_dotenv
# ========== SETUP ==========
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

engine = pyttsx3.init()

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print("You:", command)
        return command.lower()
    except:
        speak("Sorry, I didn't catch that.")
        return ""

# ========== AI CHAT ==========
def chat_with_ai(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# ========== EMAIL FUNCTION ==========
def send_email():
    speak("What should I say?")
    content = listen()

    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"
    receiver_email = "receiver_email@gmail.com"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, content)
    server.quit()

    speak("Email sent successfully.")

# ========== CALCULATOR ==========
def calculate(expression):
    try:
        result = eval(expression)
        speak(f"The result is {result}")
    except:
        speak("Invalid calculation")

# ========== MAIN JARVIS ==========
def jarvis():
    speak("Hello Sir, I am Jarvis. How can I help you?")

    while True:
        command = listen()

        if "open youtube" in command:
            webbrowser.open("https://youtube.com")
            speak("Opening YouTube")

        elif "open google" in command:
            webbrowser.open("https://google.com")
            speak("Opening Google")

        elif "open website" in command:
            speak("Tell me the website name")
            site = listen()
            webbrowser.open(f"https://{site}.com")
            speak(f"Opening {site}")

        elif "send email" in command:
            send_email()

        elif "send whatsapp" in command:
            speak("Tell me the phone number with country code")
            number = input("Enter number: ")
            speak("What is the message?")
            message = listen()
            pywhatkit.sendwhatmsg_instantly(number, message)
            speak("WhatsApp message sent")

        elif "calculate" in command:
            speak("Tell me the calculation")
            expression = listen()
            calculate(expression)

        elif "time" in command:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {now}")

        elif "exit" in command or "stop" in command:
            speak("Goodbye Sir")
            break

        elif command != "":
            reply = chat_with_ai(command)
            speak(reply)

# ========== RUN ==========
jarvis()