from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_file("layouts/children.kv")

"""
OneLineAvatarIconListItem:
    text: "Karol"

    IconLeftWidget:
        icon: "images/icons/numeric-1.png"
"""


class Children(Screen):


    def on_enter(self, *args):
        pass
