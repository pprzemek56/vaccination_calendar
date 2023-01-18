
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable

from core.screen_manager import WindowManager


class VaccinationCalendarApp(MDApp):
    def build(self):
        print(dir(MDDataTable()))
        # Window.borderless = True
        self.theme_cls.primary_palette = "Green"
        return WindowManager()


if __name__ == "__main__":
    VaccinationCalendarApp().run()
