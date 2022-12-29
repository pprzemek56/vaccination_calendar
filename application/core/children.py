import sys
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManagerException
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget

sys.path.append('database')
sys.path.append('core')

import vaccination_calendar
from child import Child

Builder.load_file("layouts/children.kv")


class Children(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.children_list = None
        self.list_elements = []
        self.child_screen = Child()

    def on_enter(self, *args):
        self.children_list = vaccination_calendar.get_children()

        for child in self.children_list:
            item = OneLineAvatarIconListItem(id=f"{child['id']}", text=f"{child['name']}", on_release=self.open_child)
            item.add_widget(IconLeftWidget(icon=f"images/icons/numeric-{child['id']}.png"))
            self.list_elements.append(item)

        for element in self.list_elements:
            self.ids.children_list.add_widget(element)

    def open_child(self, instance):
        self.child_screen.current_id = instance.id
        try:
            self.manager.add_widget(self.child_screen)
        except ScreenManagerException:
            pass
        finally:
            self.manager.current = "child"
            self.manager.transition.direction = "left"

    def on_leave(self, *args):
        for i in range(len(self.list_elements)):
            self.ids.children_list.remove_widget(self.list_elements[i])

        self.list_elements.clear()
