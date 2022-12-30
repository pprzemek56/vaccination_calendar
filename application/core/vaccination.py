import sys

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget

Builder.load_file("layouts/vaccination.kv")

sys.path.append('database')

import vaccination_calendar


class Vaccination(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vaccination_names = vaccination_calendar.get_vaccination()
        self.dialog = None

    def on_enter(self, *args):
        if not self.ids.vaccination_list.children:
            for vaccination in self.vaccination_names:
                item = OneLineAvatarIconListItem(text=f"{vaccination}", on_release=self.open_vaccination)
                item.add_widget(IconLeftWidget(icon="needle"))
                self.ids.vaccination_list.add_widget(item)

    def open_vaccination(self, instance):
        vaccination = vaccination_calendar.get_vaccination_by_name(instance.text)

        self.dialog = MDDialog(
                title=f"Szczepionka przeciw {vaccination['name']}",
                text=f"{vaccination['information']}\nIlość dawek: {vaccination['dose']}\nSzczepienie {'obowiązkowe' if vaccination['mandatory'] else 'nieobowiązkowe'}",
                buttons=[
                    MDFlatButton(
                        text="OKEY",
                        on_release=self.close_dialog)])
        self.dialog.open()


    def close_dialog(self, obj):
        self.dialog.dismiss()
