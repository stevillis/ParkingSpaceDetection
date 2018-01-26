import kivy

kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

from webparking import webreader


class ParkingFreeSpace(BoxLayout):
    def text(self):
        print('sass')


class WindowMain(BoxLayout):

    def __init__(self):
        super(WindowMain, self).__init__()

    def on_press_bt(self):

        # Remove os widgets dos StackLayouts
        self.ids.stack_layout_vaga_esquerda.clear_widgets()
        self.ids.stack_layout_vaga_direita.clear_widgets()

        # self.ids.stack_layout_vaga_esquerda.add_widget(Label(text='oi', size_hint=(1., .1)))

        dic_web = webreader.read_web('http://192.168.1.3:5000')
        print(dic_web)

        """dic = {"1": True, "2": False, "3": True, "4": True, "5": False, "6": True, "7": False, "8": True, "9": False,
               "10": False, "11": True, "12": False, "13": True, "14": False, "15": False, "16": True, "17": False,
               "18": False, "19": True, "20": True}
        """

        # Contadores para as vagas
        vagas_livres = 0
        total_vagas = len(dic_web)

        print('Total de vagas', total_vagas)

        for key, value in dic_web.items():
            if int(key) <= 10:  # Adiciona as 10 primeiras vagas do lado esquerdo
                if value:  # Vaga vazia
                    img = Image(source='images/parking_free.png', size_hint=(1, .1))
                    self.ids.stack_layout_vaga_esquerda.add_widget(img)
                    vagas_livres += 1
                else:
                    img = Image(source='images/parking_busy.png', size_hint=(1, .1))
                    self.ids.stack_layout_vaga_esquerda.add_widget(img)
            else:  # Adiciona as 10 primeiras vagas do lado direito
                if value:  # Vaga vazia
                    img = Image(source='images/parking_free.png', size_hint=(1, .1))
                    self.ids.stack_layout_vaga_direita.add_widget(img)
                    vagas_livres += 1
                else:
                    img = Image(source='images/parking_busy.png', size_hint=(1, .1))
                    self.ids.stack_layout_vaga_direita.add_widget(img)

        self.ids.label_total_vagas.text = "Total de vagas: " + str(total_vagas)
        self.ids.label_vagas_disponiveis.text = "Vagas livres: " + str(vagas_livres)
        print('Vagas livres', vagas_livres)


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
