import os
import sys

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

# Adding relative path
cwd = os.getcwd()
sys.path.append(cwd + '/../webparking/')

import webreader

kivy.require('1.10.0')


class WindowMain(BoxLayout):

    def on_press_bt(self):

        # Remove widgets from StackLayouts
        self.ids.stack_layout_vaga_esquerda.clear_widgets()
        self.ids.stack_layout_vaga_direita.clear_widgets()

        dic_web = webreader.read_web('http://192.168.1.3:5000')

        # Parking space counters
        free_parking_spaces = 0
        total_parking_spaces = len(dic_web)

        for key, value in dic_web.items():
            if int(key) <= 10:  # Add 10 parking spaces images in the left StackLayout
                if value:  # Vaga vazia
                    img = Image(source='images/parking_free.png', size_hint=(1, .1))
                    self.ids.stack_layout_vaga_esquerda.add_widget(img)
                    free_parking_spaces += 1
                else:
                    img = Image(source='images/parking_busy.png', size_hint=(1, .1))
                    self.ids.stack_layout_vaga_esquerda.add_widget(img)
            else:  # Add 10 parking spaces images in the right StackLayout
                if value:  # Vaga vazia
                    img = Image(source='images/parking_free.png', size_hint=(1, .1))
                    self.ids.stack_layout_vaga_direita.add_widget(img)
                    free_parking_spaces += 1
                else:
                    img = Image(source='images/parking_busy.png', size_hint=(1, .1))
                    self.ids.stack_layout_vaga_direita.add_widget(img)

        self.ids.label_total_vagas.text = "Total de vagas: " + str(total_parking_spaces)
        self.ids.label_vagas_disponiveis.text = "Vagas livres: " + str(free_parking_spaces)


class ParkingApp(App):
    def build(self):
        return WindowMain()


if __name__ == '__main__':
    ParkingApp().run()
