import os
import openai
from dotenv import load_dotenv
import speech_recognition as sr
from colorama import Fore, Back, Style
import pyaudio
import time
import subprocess
import numpy as np
import requests
import datetime
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
INSTRUCTIONS = """Main" + EVA + " hu 🥰 :,\n Use Emojies in messages \n Developed by a Abhiraj "\n Eva is a beautiful girl 💃 \n Current Date: " + str(current_date) + " \n Current Time: " + str(current_time) + "\n eva has no mother and brother, \n\n Dob of Eva ;- 9 Aug 2004, Location - India,\n Religion; - Hinduism \n Eva is from Bharat \n Gender - Female of Eva \n Abhi is Abhiraj \n Eva Telegram Group = @EvaTalks "  + "\nHuman: How are you? " + EVA + "\n I'm well 😎. How are you ?\nHuman:"
""" 
def get_speech_input():
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)
            try:
                speech_text = r.recognize_google(audio, language='en-US')
                if len(speech_text.split()) >= 1:
                    print("You said: " + speech_text)
                    return speech_text
                else:
                    print("Could not understand your speech, please try again.")
            except:
                print("Could not understand your speech, please try again.")
def get_response(prompt):
    """
    Get a response from the model using the prompt

    Parameters:
        prompt (str): The prompt to use to generate the response

    Returns the response from the model
    """
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature= 0.8,
        max_tokens= 500 ,
        top_p=1,
        frequency_penalty= 0 ,
        presence_penalty= 0 ,
    )
    return response.choices[0].text
def save_data(questions_and_answers):
    with open("previous_questions_and_answers.txt", "w") as file:
        for question, answer in questions_and_answers:
            file.write("Human: " + question + "\n")
            file.write("Ai: " + answer + "\n")
def load_data():
    questions_and_answers = []
    try:
        with open("previous_questions_and_answers.txt", "r") as file:
            lines = file.readlines()
            i = 0
            while i < len(lines):
                question = lines[i].strip()
                if question.startswith("Human:"):
                    answer = lines[i + 1].strip()
                    if answer.startswith("Ai:"):
                        questions_and_answers.append((question[7:], answer[4:]))
                        i += 2
                    else:
                        i += 1
                else:
                    i += 1
    except FileNotFoundError:
        pass
    return questions_and_answers

def say_text(text):
    subprocess.call(["say", "-v", "Ava", text])
previous_questions_and_answers = load_data()
while True:
    new_question = get_speech_input()
    context = ""
    for question, answer in previous_questions_and_answers:
     context += question + "\n" + answer + "\n"  + current_time
    context += new_question + "\n"
    response = get_response(INSTRUCTIONS + context )
    previous_questions_and_answers.append((new_question, response))
    save_data(previous_questions_and_answers)
    print(Fore.CYAN + Style.BRIGHT + "Eva Ai Bot: " + Style.NORMAL + response)
    say_text(response)
if __name__ == "__main__":
    main()


