import sys
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget

sys.path.append('database')

import vaccination_calendar

Builder.load_file("layouts/children.kv")


class Children(Screen):
    first_enter = True
    children_list = vaccination_calendar.get_children()
    list_elements = []

    def on_enter(self, *args):
        if self.first_enter:
            for child in self.children_list:
                item = Builder.load_string(f'''OneLineAvatarIconListItem:
    text: "{child['name']}"
    on_release:
        app.root.current = "child"
        
    IconLeftWidget:
        icon: "images/icons/numeric-{child['id']}.png"''')
                self.list_elements.append(item)

            for element in self.list_elements:
                self.ids.children_list.add_widget(element)

            self.first_enter = False

