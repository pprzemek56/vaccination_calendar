
from kivymd.app import MDApp
from kivymd.uix.scrollview import MDScrollView

from core.screen_manager import WindowManager


class VaccinationCalendarApp(MDApp):
    def build(self):
        print(dir(MDScrollView()))
        # Window.borderless = True
        self.theme_cls.primary_palette = "Green"
        return WindowManager()


if __name__ == "__main__":
    VaccinationCalendarApp().run()
