
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




# from flask import Flask, render_template, request, jsonify
# import datetime
# import requests
# import wikipedia
# import pyjokes

# app = Flask(__name__)

# API_KEY = "5c2daec77599d6992d18d8d10c9bfc85"


# def get_weather(city):
#     try:
#         url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
#         data = requests.get(url).json()

#         if data.get("cod") != 200:
#             return "Sorry, I couldn't find that city."

#         temp = data["main"]["temp"]
#         desc = data["weather"][0]["description"]

#         return f"The temperature in {city} is {temp} degree Celsius with {desc}."

#     except:
#         return "Unable to get weather information."


# @app.route("/")
# def home():
#     return render_template("index.html")


# @app.route("/assistant", methods=["POST"])
# def assistant():

#     text = request.json["text"].lower()

#     if "time" in text:
#         reply = "Current time is " + datetime.datetime.now().strftime("%I:%M %p")

#     elif "joke" in text:
#         reply = pyjokes.get_joke()

#     elif "who is" in text:
#         person = text.replace("who is", "").strip()

#         try:
#             reply = wikipedia.summary(person, 2)
#         except:
#             reply = "Sorry, I couldn't find information."

#     elif "weather" in text:

#         city = "Hyderabad"

#         words = text.split()

#         if "in" in words:
#             city = " ".join(words[words.index("in")+1:])

#         reply = get_weather(city)

#     elif "play" in text:

#         song = text.replace("play", "").strip()

#         youtube_url = (
#         f"https://www.google.com/search?q={song.replace(' ', '+')}+site:youtube.com&btnI=1"
#         )

#         return jsonify({
#         "reply": f"Playing {song}",
#         "youtube": youtube_url
#         })


#     else:

#         reply = "Sorry, I didn't understand."

#     return jsonify({"reply":reply})


# if __name__ == "__main__":
#     app.run(debug=True)





from flask import Flask, render_template, request, jsonify
import datetime
import requests
import wikipedia
import pyjokes

app = Flask(__name__)

# ==============================
# OpenWeather API Key
# ==============================
API_KEY = "5c2daec77599d6992d18d8d10c9bfc85"

# ==============================
# Weather Function
# ==============================
def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        response = requests.get(url, timeout=5)

        data = response.json()

        if response.status_code != 200:
            return "Sorry, I couldn't find that city."

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]

        return f"The temperature in {city.title()} is {temp}°C with {desc}."

    except:
        return "Unable to fetch weather information."


# ==============================
# Home Page
# ==============================
@app.route("/")
def home():
    return render_template("index.html")


# ==============================
# Voice Assistant
# ==============================
@app.route("/assistant", methods=["POST"])
def assistant():

    data = request.get_json()

    text = data.get("text", "").lower().strip()

    if text == "":
        return jsonify({"reply": "Please say something."})

    # ----------------------------
    # Greetings
    # ----------------------------
    if any(word in text for word in ["hello", "hi", "hey"]):

        reply = "Hello! How can I help you today?"

    # ----------------------------
    # Time
    # ----------------------------
    elif "time" in text:

        reply = "Current time is " + datetime.datetime.now().strftime("%I:%M %p")

    # ----------------------------
    # Date
    # ----------------------------
    elif "date" in text:

        reply = "Today is " + datetime.datetime.now().strftime("%A, %d %B %Y")

    # ----------------------------
    # Joke
    # ----------------------------
    elif "joke" in text:

        reply = pyjokes.get_joke()

    # # ----------------------------
    # # Wikipedia
    # # ----------------------------
    # elif "who is" in text or "what is" in text:

    #     person = (
    #         text.replace("who is", "")
    #         .replace("what is", "")
    #         .strip()
    #     )

    #     try:
    #         reply = wikipedia.summary(person, sentences=2)

    #     except:

    #         reply = "Sorry, I couldn't find information."



    elif "send email" in text:

        words = text.split()

        email = ""

        if "to" in words:
            email = words[words.index("to") + 1]

        subject = "Hello"
        body = "Sent from AI Voice Assistant"

        return jsonify({
            "reply": f"Opening email for {email}",
            "mail": f"mailto:{email}?subject={subject}&body={body}"
        })


    elif (
    "who is" in text or
    "what is" in text or
    "tell me about" in text or
    "search" in text or
    "explain" in text):

        query = text

        for word in [
            "who is",
            "what is",
            "tell me about",
            "search",
            "explain"
        ]:
            query = query.replace(word, "")

        query = query.strip()

        return jsonify({
            "reply": f"Searching Google for {query}",
            "google": f"https://www.google.com/search?q={query.replace(' ','+')}"
        })

    # ----------------------------
    # Weather
    # ----------------------------
    elif "weather" in text:

        city = "Hyderabad"

        if " in " in text:

            city = text.split(" in ", 1)[1].strip()

        reply = get_weather(city)

    # ----------------------------
    # Play Song
    # ----------------------------
    elif text.startswith("play"):

        song = text.replace("play", "").strip()

        return jsonify({

            "reply": f"Opening YouTube for {song}",

            "youtube":
            f"https://www.youtube.com/results?search_query={song.replace(' ','+')}"

        })
    

        # ----------------------------
    # Maps & Directions
    # ----------------------------
    elif "directions from" in text and "to" in text:

        # Example: directions from Hyderabad to Warangal
        try:
            route = text.split("directions from", 1)[1].strip()
            origin, destination = route.split(" to ", 1)

            maps_url = (
                "https://www.google.com/maps/dir/"
                f"{origin.strip().replace(' ', '+')}/"
                f"{destination.strip().replace(' ', '+')}"
            )

            return jsonify({
                "reply": f"Showing directions from {origin} to {destination}",
                "maps": maps_url
            })

        except:
            return jsonify({
                "reply": "Please say directions from place A to place B."
            })

    elif "directions to" in text or "navigate to" in text:

        # Example: navigate to Charminar
        destination = (
            text.replace("directions to", "")
            .replace("navigate to", "")
            .strip()
        )

        maps_url = (
            "https://www.google.com/maps/dir/?api=1"
            f"&destination={destination.replace(' ', '+')}"
        )

        return jsonify({
            "reply": f"Navigating to {destination}",
            "maps": maps_url
        })

    elif "maps" in text or "location" in text:

        place = (
            text.replace("map", "")
            .replace("location", "")
            .strip()
        )

        return jsonify({
            "reply": f"Opening Google Maps for {place}",
            "maps": f"https://www.google.com/maps/search/{place.replace(' ', '+')}"
        })

    # ----------------------------
    # Google Search
    # ----------------------------
    elif "search" in text:

        query = text.replace("search", "").strip()

        return jsonify({

            "reply": f"Searching Google for {query}",

            "google":
            f"https://www.google.com/search?q={query.replace(' ','+')}"

        })

    # ----------------------------
    # Maps
    # ----------------------------
    elif "map" in text or "location" in text:

        place = (
            text.replace("map", "")
            .replace("location", "")
            .strip()
        )

        return jsonify({

            "reply": f"Opening Google Maps for {place}",

            "maps":
            f"https://www.google.com/maps/search/{place.replace(' ','+')}"

        })

    # ----------------------------
    # Open Websites
    # ----------------------------
    elif "open youtube" in text:

        return jsonify({

            "reply":"Opening YouTube",

            "website":"https://youtube.com"

        })

    elif "open google" in text:

        return jsonify({

            "reply":"Opening Google",

            "website":"https://google.com"

        })

    elif "open github" in text:

        return jsonify({

            "reply":"Opening GitHub",

            "website":"https://github.com"

        })

    elif "open chatgpt" in text:

        return jsonify({

            "reply":"Opening ChatGPT",

            "website":"https://chatgpt.com"

        })

    # ----------------------------
    # Thank You
    # ----------------------------
    elif "thank" in text:

        reply = "You're welcome."

    # ----------------------------
    # Bye
    # ----------------------------
    elif "bye" in text or "goodbye" in text:

        reply = "Goodbye. Have a great day."

    # ----------------------------
    # Unknown
    # ----------------------------
    else:

        reply = (
            "Sorry, I don't understand that command yet."
        )

    return jsonify({"reply": reply})


# ==============================
# Run
# ==============================
if __name__ == "__main__":
    app.run(debug=True)