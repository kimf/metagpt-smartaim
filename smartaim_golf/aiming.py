## aiming.py
import math
from typing import Tuple

class Aiming:
    def __init__(self, user: User, weather: Weather):
        self.user = user
        self.weather = weather

    def get_aiming_point(self, club: str) -> Tuple[float, float]:
        # Get the dispersion pattern for the given club
        dispersion_pattern = self.user.get_dispersion_pattern().get(club, None)
        if dispersion_pattern is None:
            print(f"No dispersion pattern found for club {club}")
            return (0.0, 0.0)

        # Get the current weather
        current_weather = self.weather.get_weather()
        if 'wind' not in current_weather:
            print(f"No wind data found in current weather")
            return dispersion_pattern

        # Calculate the wind effect
        wind_speed = current_weather['wind'].get('speed', 0)
        wind_direction = current_weather['wind'].get('deg', 0)

        # Calculate the aiming point
        wind_effect_x = wind_speed * math.cos(math.radians(wind_direction))
        wind_effect_y = wind_speed * math.sin(math.radians(wind_direction))

        aiming_point_x = dispersion_pattern[0] + wind_effect_x
        aiming_point_y = dispersion_pattern[1] + wind_effect_y

        return (aiming_point_x, aiming_point_y)
