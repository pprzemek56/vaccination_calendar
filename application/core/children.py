import sys
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

sys.path.append('database')

import vaccination_calendar

Builder.load_file("layouts/children.kv")


class Children(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.children_list = None
        self.list_elements = []

    def on_enter(self, *args):
        self.children_list = vaccination_calendar.get_children()

        for child in self.children_list:
            item = Builder.load_string(f'''OneLineAvatarIconListItem:
    text: "{child['name']}"
    on_release:
        app.root.current = "child"
        app.root.transition.direction = "left"
        
    IconLeftWidget:
        icon: "images/icons/numeric-{child['id']}.png"''')
            self.list_elements.append(item)

        for element in self.list_elements:
            self.ids.children_list.add_widget(element)

    def on_leave(self, *args):

        for i in range(len(self.list_elements)):
            self.ids.children_list.remove_widget(self.list_elements[i])

        self.list_elements.clear()

