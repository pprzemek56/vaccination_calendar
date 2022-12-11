from kivymd.app import MDApp

from core.screen_manager import WindowManager


class VaccinationCalendarApp(MDApp):
    def build(self):
        return WindowManager()


if __name__ == "__main__":
    VaccinationCalendarApp().run()
