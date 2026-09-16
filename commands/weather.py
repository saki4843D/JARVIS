import requests
from config import DEFAULT_CITY, USER_NAME, WEATHER_API_KEY


def get_weather(city=None):

    if city is None or city.strip() == "":
        city = DEFAULT_CITY

    if not WEATHER_API_KEY:
        return "Weather is not configured yet. Add WEATHER_API_KEY to your .env file."

    url = "https://api.openweathermap.org/data/2.5/weather"

    try:

        response = requests.get(url, params={"q": city, "appid": WEATHER_API_KEY, "units": "metric"}, timeout=10)

        data = response.json()

        if response.status_code != 200:
            return f"Sorry {USER_NAME}, I couldn't find that city."

        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        weather = data["weather"][0]["description"]
        wind = data["wind"]["speed"]

        return (
            f"In {city}, it's {temperature} degrees Celsius with {weather}. "
            f"It feels like {feels_like} degrees. "
            f"Humidity is {humidity} percent and wind speed is {wind} meters per second."
        )

    except (KeyError, IndexError, requests.RequestException, ValueError):
        return f"Sorry {USER_NAME}, I couldn't connect to the weather service."
