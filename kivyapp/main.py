# File name: main.py

import kivy
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout

# Version of kivy
kivy.require('1.10.0')


class Main(AnchorLayout):
    parking_space_available = ''
    parking_space_busy = ''

    def update(self):
        app = App.get_running_app()


class MainApp(App):
    def build(self):
        return Main()


if __name__ == '__main__':
    MainApp().run()
