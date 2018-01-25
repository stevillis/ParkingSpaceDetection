import kivy

kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

from webparking import webreader


class ButtonUpdate():
    pass

class WindowMain(BoxLayout):
    def on_press_bt(self):
        # dic_web = webreader.read_web('http://192.168.1.3:5000')
        # self.add_widget(Picture(source='images/parking_free128.png'))
        # print(dic_web)
        print('button')


class Picture(Image):
    pass


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


"""
canvas:
            Color:
                rgb: 1, 1, 1
            Rectangle:
                source: 'images/parking_busy.png'
                size: self.size
"""