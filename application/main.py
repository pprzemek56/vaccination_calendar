from kivy.core.window import Window
from kivymd.app import MDApp

from core.screen_manager import WindowManager


class VaccinationCalendarApp(MDApp):
    def build(self):
        Window.borderless = True
        self.theme_cls.primary_palette = "Green"
        return WindowManager()


if __name__ == "__main__":
    VaccinationCalendarApp().run()
