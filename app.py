
# # import speech_recognition as sr
# # import pyttsx3
# # import pywhatkit
# # import datetime
# # import wikipedia
# # import pyjokes
# # import requests
# # import json
# # import sys

# # # Required Libraries:
# # # pip install SpeechRecognition pyttsx3 pywhatkit wikipedia pyjokes requests pyaudio

# # listener = sr.Recognizer()

# # engine = pyttsx3.init()

# # voices = engine.getProperty("voices")
# # engine.setProperty("voice", voices[1].id)


# # def engine_talk(text):
# #     engine.say(text)
# #     engine.runAndWait()


# # def weather(cit):
# #     api_key = "5c2daec77599d6992d18d8d10c9bfc85"
# #     base_url = "http://api.openweathermap.org/data/2.5/weather?"

# #     city_name = cit

# #     # Correct API URL
# #     complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&units=metric"

# #     # Correct requests object
# #     response = requests.get(complete_url)

# #     x = response.json()

# #     if str(x["cod"]) != "404":
# #         y = x["main"]
# #         current_temperature = y["temp"]
# #         return str(current_temperature)
# #     else:
# #         return "City not found"


# # def user_commands():
# #     command = ""

# #     try:
# #         with sr.Microphone() as source:
# #             print("Start Speaking...")

# #             # Optional: Reduce background noise
# #             listener.adjust_for_ambient_noise(source, duration=1)

# #             voice = listener.listen(source)

# #             command = listener.recognize_google(voice)

# #             command = command.lower()

# #             if "alexa" in command:
# #                 command = command.replace("alexa", "")

# #             print(command)

# #     except Exception as e:
# #         print(e)

# #     return command.strip()


# # def run_alexa():
# #     command = user_commands()

# #     if "play" in command:
# #         song = command.replace("play", "")
# #         engine_talk("Playing " + song)
# #         pywhatkit.playonyt(song)

# #     elif "time" in command:
# #         time = datetime.datetime.now().strftime("%I:%M %p")
# #         print(time)
# #         engine_talk("The current time is " + time)

# #     elif "who is" in command:
# #         name = command.replace("who is", "")

# #         try:
# #             info = wikipedia.summary(name, 1)
# #             print(info)
# #             engine_talk(info)

# #         except Exception:
# #             engine_talk("Sorry, I couldn't find information.")

# #     elif "joke" in command:
# #         joke = pyjokes.get_joke()
# #         print(joke)
# #         engine_talk(joke)

# #     elif "weather" in command:
# #         engine_talk("Please tell the name of the city")

# #         city = user_commands()

# #         if city != "":
# #             weather_api = weather(city)
# #             print(weather_api)

# #             if weather_api == "City not found":
# #                 engine_talk("City not found.")
# #             else:
# #                 engine_talk(
# #                     "The temperature in "
# #                     + city
# #                     + " is "
# #                     + weather_api
# #                     + " degree Celsius"
# #                 )
# #         else:
# #             engine_talk("I could not hear the city name.")

# #     elif "stop" in command or "exit" in command:
# #         engine_talk("Goodbye")
# #         sys.exit()

# #     else:
# #         engine_talk("I could not hear you properly")


# # while True:
# #     run_alexa()


# from flask import Flask, render_template, request
# import warnings
# warnings.filterwarnings("ignore")

# import speech_recognition as sr
# import pyttsx3
# import pywhatkit
# import datetime
# import pyjokes
# import wikipedia
# import requests
# import sys

# app = Flask(__name__)

# listener = sr.Recognizer()



# def engine_talk(text):
#     engine = pyttsx3.init()

#     voices = engine.getProperty("voices")
#     engine.setProperty("voice", voices[1].id)

#     engine.say(text)
#     engine.runAndWait()
#     engine.stop()


# def user_commands():
#     command = ""

#     try:
#         with sr.Microphone() as source:
#             print("Listening...")
#             listener.adjust_for_ambient_noise(source)
#             voice = listener.listen(source)

#             command = listener.recognize_google(voice)
#             command = command.lower()

#             if "alexa" in command:
#                 command = command.replace("alexa", "").strip()

#             print(command)

#     except Exception as e:
#         print(e)

#     return command


# def weather(city):
#     api_key = "5c2daec77599d6992d18d8d10c9bfc85"

#     url = f"http://api.openweathermap.org/data/2.5/weather?appid={api_key}&q={city}"

#     response = requests.get(url)

#     data = response.json()

#     if data.get("cod") != "404":
#         temp = data["main"]["temp"] - 273.15
#         return round(temp, 1)

#     return None


# def run_alexa():

#     command = user_commands()

#     if command == "":
#         engine_talk("I didn't hear anything.")
#         return

#     if "play a song" in command:
#         engine_talk("Playing music")
#         pywhatkit.playonyt("Arijit Singh")

#     elif "play" in command:
#         song = command.replace("play", "")
#         engine_talk("Playing " + song)
#         pywhatkit.playonyt(song)

#     elif "time" in command:
#         time = datetime.datetime.now().strftime("%I:%M %p")
#         engine_talk("Current time is " + time)

#     elif "joke" in command:
#         joke = pyjokes.get_joke()
#         engine_talk(joke)

#     elif "who is" in command:
#         person = command.replace("who is", "")

#         try:
#             info = wikipedia.summary(person, 1)
#             engine_talk(info)

#         except:
#             engine_talk("Sorry, I could not find that person.")

#     elif "weather" in command:
#         city = "Hong Kong"

#         temp = weather(city)

#         if temp:
#             engine_talk(f"The temperature in {city} is {temp} degree Celsius")

#     elif "stop" in command:
#         engine_talk("Good Bye")
#         sys.exit()

#     else:
#         engine_talk("Please say it again.")


# @app.route("/", methods=["GET", "POST"])
# def home():

#     if request.method == "POST":
#         run_alexa()

#     return render_template("index.html")


# if __name__ == "__main__":
#     app.run(debug=False)


from flask import Flask, render_template, request, jsonify
import datetime
import requests
import wikipedia
import pyjokes

app = Flask(__name__)

API_KEY = "YOUR_OPENWEATHER_API_KEY"


def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()

        if data.get("cod") != 200:
            return "Sorry, I couldn't find that city."

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]

        return f"The temperature in {city} is {temp} degree Celsius with {desc}."

    except:
        return "Unable to get weather information."


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/assistant", methods=["POST"])
def assistant():

    text = request.json["text"].lower()

    if "time" in text:
        reply = "Current time is " + datetime.datetime.now().strftime("%I:%M %p")

    elif "joke" in text:
        reply = pyjokes.get_joke()

    elif "who is" in text:
        person = text.replace("who is", "").strip()

        try:
            reply = wikipedia.summary(person, 2)
        except:
            reply = "Sorry, I couldn't find information."

    elif "weather" in text:

        city = "Hyderabad"

        words = text.split()

        if "in" in words:
            city = " ".join(words[words.index("in")+1:])

        reply = get_weather(city)

    elif "play" in text:

        song = text.replace("play", "").strip()

        return jsonify({
            "reply":"Opening YouTube",
            "youtube":f"https://www.youtube.com/results?search_query={song}"
        })

    else:

        reply = "Sorry, I didn't understand."

    return jsonify({"reply":reply})


if __name__ == "__main__":
    app.run(debug=True)