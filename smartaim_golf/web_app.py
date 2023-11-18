## web_app.py
from flask import Flask, request, jsonify
from database import Database, User
from weather import Weather
from aiming import Aiming
from map import Map

app = Flask(__name__)
db = Database()
weather = Weather(api_key="YOUR_OPENWEATHERMAP_API_KEY")

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User(username, password)
    db.add_user(user)
    return jsonify({"message": "User created successfully"}), 200

@app.route('/weather', methods=['GET'])
def get_weather():
    location = request.args.get('location')
    current_weather = weather.get_weather(location)
    if not current_weather:
        return jsonify({"message": "Failed to get weather data"}), 500
    return jsonify(current_weather), 200

@app.route('/aiming', methods=['GET'])
def get_aiming_point():
    club = request.args.get('club')
    username = request.args.get('username')
    user = db.get_user(username)
    if user is None:
        return jsonify({"message": "User not found"}), 404
    aiming = Aiming(user, weather)
    aiming_point = aiming.get_aiming_point(club)
    if aiming_point == (0.0, 0.0):
        return jsonify({"message": "Failed to calculate aiming point"}), 500
    return jsonify({"aiming_point": aiming_point}), 200

@app.route('/map', methods=['GET'])
def show_dispersion_pattern():
    username = request.args.get('username')
    user = db.get_user(username)
    if user is None:
        return jsonify({"message": "User not found"}), 404
    map = Map(user)
    map.show_dispersion_pattern()
    return jsonify({"message": "Dispersion pattern displayed successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
