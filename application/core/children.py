import sys
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManagerException
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
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
        self.remove_child_dialog = None

    def on_enter(self, *args):
        self.children_list = vaccination_calendar.get_children()

        for child in self.children_list:
            item = OneLineAvatarIconListItem(id=f"{child['id']}", text=f"{child['name']}", on_release=self.open_child,
                                             on_icon_release=self.on_icon_release)
            item.add_widget(
                IconLeftWidget(id=f"{child['id']}", icon=f"delete", theme_text_color="Custom", text_color=(1, 0, 0, 1),
                               on_release=self.on_icon_release))
            self.list_elements.append(item)

        for element in self.list_elements:
            self.ids.children_list.add_widget(element)

    def on_icon_release(self, instance):
        child_name = vaccination_calendar.get_child_name(instance.id)
        self.remove_child_dialog = MDDialog(
            title="Usuń dziecko",
            text=f"Czy aby na pewno chcesz usunąć dziecko: {child_name}",
            buttons=[
                MDFlatButton(
                    text="Nie",
                    on_release=self.close_dialog),
                MDFlatButton(
                    text="Tak",
                    on_release=lambda child: self.remove_child(instance))])
        self.remove_child_dialog.open()

    def remove_child(self, obj):
        vaccination_calendar.remove_child(obj.id)
        self.remove_child_dialog.dismiss()

    def close_dialog(self, obj):
        self.remove_child_dialog.dismiss()

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
