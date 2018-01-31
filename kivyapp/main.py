# -*- coding: utf-8 -*-

import ast

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.network.urlrequest import UrlRequest

kivy.require('1.10.0')


class WindowMain(BoxLayout):
    def __init__(self, **kwargs):
        super(WindowMain, self).__init__(**kwargs)
        self.request = ''
        self.data = ''

    def on_press_bt(self):
        self.request = UrlRequest('http://192.168.1.6:5000', self.update_screen)

    def update_screen(self, *args):
        self.data = ast.literal_eval(str(self.request.result))

        # Remove widgets from StackLayouts
        self.ids.stack_layout_vaga_esquerda.clear_widgets()
        self.ids.stack_layout_vaga_direita.clear_widgets()

        # Sort dic_web to
        # a list of tuples with dic_web keys ordered
        dic_web_sorted = sorted(self.data.items())

        # Parking space counters
        free_parking_spaces = 0
        total_parking_spaces = len(self.data)

        for item in dic_web_sorted:
            # item[0] -> key, item[1] -> value
            if int(item[0]) <= 10:  # Add 10 parking spaces images in the left StackLayout                
                if item[1]:  # Vaga vazia
                    img = Image(source='images/parking_free.png', size_hint=(1, .1))
                    self.ids.stack_layout_vaga_esquerda.add_widget(img)
                    free_parking_spaces += 1
                else:
                    img = Image(source='images/parking_busy.png', size_hint=(1, .1))
                    self.ids.stack_layout_vaga_esquerda.add_widget(img)
            else:  # Add 10 parking spaces images in the right StackLayout
                if item[1]:  # Vaga vazia
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
