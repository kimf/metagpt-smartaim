## weather.py
import requests
from typing import Dict

class Weather:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.current_weather = {}

    def get_weather(self, location: str) -> Dict[str, str]:
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": location,
            "appid": self.api_key,
            "units": "metric"
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            self.current_weather = response.json()
        else:
            print(f"Failed to get weather data for {location}. Status code: {response.status_code}")
        return self.current_weather
