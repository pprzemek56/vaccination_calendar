from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp


class VaccinationCalendarApp(MDApp):
    def build(self):
        screen_manager = ScreenManager()

        return screen_manager


if __name__ == "__main__":
    VaccinationCalendarApp().run()
