import sys

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget

Builder.load_file("layouts/vaccination.kv")

sys.path.append('database')

import vaccination_calendar


class Vaccination(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vaccination_names = vaccination_calendar.get_vaccination()

    def on_enter(self, *args):
        if not self.ids.vaccination_list.children:
            for vaccination in self.vaccination_names:
                item = OneLineAvatarIconListItem(text=f"{vaccination}", on_release=self.open_vaccination)
                item.add_widget(IconLeftWidget(icon="needle"))
                self.ids.vaccination_list.add_widget(item)

    def open_vaccination(self, instance):
        pass

