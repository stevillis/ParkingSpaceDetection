import kivy

kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle


class ImageParkingFree(BoxLayout):
    def text(self):
        print('sass')


class WindowMain(BoxLayout):
    def on_press_bt(self):
        # dic_web = webreader.read_web('http://192.168.1.3:5000')
        # self.add_widget(Picture(source='images/parking_free128.png'))
        # print(dic_web)

        dic = {"1": True, "2": False, "3": True, "4": True, "5": False, "6": True, "7": False, "8": True, "9": False,
               "10": False, "11": True, "12": False, "13": True, "14": False, "15": False, "16": True, "17": False,
               "18": True, "19": True, "20": False, }

        """for key, value in dic.items():
            if int(key) <= 10:
                if value:
                    
                    print('Adicionado')
        """
        lb = Label(text='Text', size_hint=(1., .1))

        """with lb.canvas:
            Color(1, 1, 1)
            Rectangle(size=lb.size, pos=lb.pos,
                source='images/parking_free.png')
        """
        # img = Image(source='images/parking_free.png')

        # bt = Button(text='OK', size_hint=(1., .1))
        #lb = Label(text='Hi', size_hint=(1., .1))
        self.ids.stack_layout_vaga_esquerda.add_widget(lb)

        print('button')

    # def add_parking_space(self, id_stack):


class ParkingApp(App):
    def build(self):
        return WindowMain()


def start():
    """

    Start
    the
    Kivy
    Application
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
