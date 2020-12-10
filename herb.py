import datetime
import time
import threading
import pyttsx3
import speech_recognition as sr
import wikipedia
import wolframalpha
import sys
import os
import requests

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
#API_ID for wolframalpha
app_id = "E346QG-769KKVYGUE"


#takes command via mic
def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")
        r.pause_threshold = .6
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)
        print("Unable to Recognize your voice.")
        return "None"

    return query


#This just speaks through speakers
#example: speak("what is a fish")
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


#This is where most of the definitions for performing user directed tasks reside
def start_in():
    print('')
    init_listen = takeCommand().lower()
    print(init_listen)
    if "herb" in init_listen:
        speak("what?")
        try:

            user_in = takeCommand()
            user_split = user_in.split()

            # Definitions that you want to add

            def alarm_pre(x, y, z):
                alarm_time = x + y + z
                time.sleep(alarm_time)
                speak("ALARM SOUND, ALARM SOUND, ALARM SOUND")
                return


            def alarm():
                speak('how many hours')
                x = int(takeCommand()) * 3600

                speak('how many minutes')
                y = int(takeCommand()) * 60

                speak('how many seconds')
                z = int(takeCommand())

                thread = threading.Thread(target=alarm_pre, args=(x, y, z,))
                thread.start()
                start_in()



            def calc():
                client = wolframalpha.Client(app_id)
                indx = user_in.lower().split().index('solve')
                query = user_in.split()[indx + 1:]
                res = client.query(' '.join(query))
                answer = next(res.results).text
                print(answer)
                speak("The answer is " + answer)
                return


            def wiki():
                print('Searching Wikipedia...')
                xre = user_in.replace('what', '').replace('who', '')
                results = wikipedia.summary(xre, sentences=1)
                print("According to Wikipedia")
                speak(results)
                return


            def what():
                speak('what do you want to stick in that dumb head of yours')
                user_in = takeCommand()
                client = wolframalpha.Client(app_id)
                res = client.query(user_in)

                try:
                    print(next(res.results).text)
                    speak(next(res.results).text)
                except StopIteration:
                    print("No results")
                    speak("No results")


            def shut_down():
                sys.exit(0)


            #no definitions should be set past this point


            lisx = ['what', 'who', 'is',
            'set','an' 'alarm',
            'solve',
            'use', 'wolf',
            'shut', 'down' ]
            c = []

            for string in user_split:
                if string in lisx:
                    if string not in c:
                        c.append(string)

            for string in user_split:
                if string in lisx:
                    if string not in c:
                        c.append(string)


            x = c[0:3]


            # Function to convert
            def listToString(x):
                # initialize an empty string
                str1 = " "

                # return string
                return str1.join(x)

            # this has what you are going to be saying to call the functions
            diction = {
                'what is': wiki,
                'who is': wiki,
                'use wolf': what,
                'set an alarm': alarm,
                'shut down': shut_down,
                'solve': calc
                }

            # Driver code
            y = listToString(x)
            diction[y].__call__()

            start_in()

        except KeyError:
            speak('excuse me, are you stupid?')
            start_in()
        except SystemExit:
            sys.exit()
        except:
            speak("just gonna sit there?")
            start_in()
    else:
        start_in()


#main call for starting up the application
def start():
    speak("hey nerd my names herb")
    speak("what do you want?")
    start_in()



start()
