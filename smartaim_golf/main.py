## main.py
import argparse
from database import Database, User
from weather import Weather
from aiming import Aiming
from map import Map

def main():
    parser = argparse.ArgumentParser(description='SmartAim Golf Application')
    parser.add_argument('--username', type=str, required=True, help='Username')
    parser.add_argument('--password', type=str, required=True, help='Password')
    parser.add_argument('--location', type=str, required=True, help='Location for weather data')
    parser.add_argument('--club', type=str, required=True, help='Club for aiming point calculation')
    args = parser.parse_args()

    # Create a new user
    user = User(args.username, args.password)

    # Create a new database and add the user
    db = Database()
    db.add_user(user)

    # Get the current weather
    weather = Weather(api_key="YOUR_OPENWEATHERMAP_API_KEY")
    weather.get_weather(args.location)

    # Create a new aiming and calculate the aiming point
    aiming = Aiming(user, weather)
    aiming_point = aiming.get_aiming_point(args.club)
    print(f"Aiming point for {args.club}: {aiming_point}")

    # Create a new map and show the dispersion pattern
    map = Map(user)
    map.show_dispersion_pattern()

if __name__ == '__main__':
    main()
