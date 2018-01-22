import kivy

kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from webparking import webreader


class WindowMain(BoxLayout):
    def on_press_bt(self):
        dic_web = webreader.read_web('http://192.168.1.3:5000')
        print(dic_web)


class ParkingApp(App):
    def build(self):
        return WindowMain()


def start():
    """
    Start the Kivy Application
    :return: None
    """
    window = ParkingApp()
    window.run()


if __name__ == '__main__':
    start()

# window = ParkingApp()
# window.run()
