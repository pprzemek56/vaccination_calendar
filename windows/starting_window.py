from kivy.app import App


from kivy.lang import Builder

kv = Builder.load_file("vaccinationcalendar.kv")


class VaccinationCalendarApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    VaccinationCalendarApp().run()
