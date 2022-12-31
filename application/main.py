from kivymd.app import MDApp

from core.screen_manager import WindowManager


class VaccinationCalendarApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"g
        return WindowManager()


if __name__ == "__main__":
    VaccinationCalendarApp().run()
