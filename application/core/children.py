import sys
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget

sys.path.append('database')

import vaccination_calendar

Builder.load_file("layouts/children.kv")

"""
OneLineAvatarIconListItem:
    text: "Karol"

    IconLeftWidget:
        icon: "images/icons/numeric-1.png"
"""


class Children(Screen):
    def on_enter(self, *args):
        children_list = vaccination_calendar.get_children()
        list_elements = []
        for child in children_list:
            item = OneLineAvatarIconListItem(text=f"{child['name']}")
            item.add_widget(IconLeftWidget(icon=f"images/icons/numeric-{child['id']}.png"))
            list_elements.append(item)

        for element in list_elements:
            self.ids.children_list.add_widget(element)
