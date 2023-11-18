## map.py
import folium
from typing import Dict, Tuple

class Map:
    def __init__(self, user: User):
        self.user = user

    def show_dispersion_pattern(self) -> None:
        # Get the dispersion pattern
        dispersion_pattern = self.user.get_dispersion_pattern()

        # Create a new map
        m = folium.Map(location=[45.5236, -122.6750])

        # Add markers for each point in the dispersion pattern
        for club, point in dispersion_pattern.items():
            folium.Marker(
                location=point,
                popup=f"{club}: {point}",
                icon=folium.Icon(icon="cloud"),
            ).add_to(m)

        # Save the map to a file
        m.save("dispersion_pattern.html")
