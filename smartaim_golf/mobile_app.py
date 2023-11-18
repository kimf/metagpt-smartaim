## mobile_app.py
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.network.urlrequest import UrlRequest
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from database import Database, User
from weather import Weather
from aiming import Aiming
from map import Map
import bcrypt

class SmartAimGolfApp(App):
    def build(self):
        self.db = Database()
        self.weather = Weather(api_key="YOUR_OPENWEATHERMAP_API_KEY")
        self.root = BoxLayout(orientation='vertical')
        self.username_input = TextInput(hint_text='Username')
        self.password_input = TextInput(hint_text='Password', password=True)
        self.club_spinner = Spinner(text='Select Club', values=('Driver', 'Iron', 'Putter'))
        self.location_input = TextInput(hint_text='Location')
        self.login_button = Button(text='Login')
        self.login_button.bind(on_release=self.login)
        self.root.add_widget(self.username_input)
        self.root.add_widget(self.password_input)
        self.root.add_widget(self.club_spinner)
        self.root.add_widget(self.location_input)
        self.root.add_widget(self.login_button)
        return self.root

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        user = self.db.get_user(username)
        if user is None or not bcrypt.checkpw(password.encode(), user.password.encode()):
            popup = Popup(title='Login Failed', content=Label(text='Invalid username or password'), size_hint=(None, None), size=(400, 400))
            popup.open()
            return
        self.user = user
        self.aiming = Aiming(user, self.weather)
        self.map = Map(user)
        self.root.clear_widgets()
        self.root.add_widget(Label(text=f'Welcome, {username}!'))
        self.calculate_aiming_button = Button(text='Calculate Aiming Point')
        self.calculate_aiming_button.bind(on_release=self.calculate_aiming_point)
        self.root.add_widget(self.calculate_aiming_button)
        self.show_map_button = Button(text='Show Dispersion Pattern')
        self.show_map_button.bind(on_release=self.show_dispersion_pattern)
        self.root.add_widget(self.show_map_button)

    def calculate_aiming_point(self, instance):
        club = self.club_spinner.text
        location = self.location_input.text
        self.weather.get_weather(location)
        aiming_point = self.aiming.get_aiming_point(club)
        popup = Popup(title='Aiming Point', content=Label(text=str(aiming_point)), size_hint=(None, None), size=(400, 400))
        popup.open()

    def show_dispersion_pattern(self, instance):
        self.map.show_dispersion_pattern()
        popup = Popup(title='Dispersion Pattern', content=Label(text='Dispersion pattern displayed on map'), size_hint=(None, None), size=(400, 400))
        popup.open()

if __name__ == '__main__':
    SmartAimGolfApp().run()
