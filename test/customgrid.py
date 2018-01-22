from kivy.uix.floatlayout import FloatLayout


class CustomGrid(FloatLayout):
    def add_child_to_specific(self, row, col, widget):
        self.ids[row].ids[col].add_widget(widget)
