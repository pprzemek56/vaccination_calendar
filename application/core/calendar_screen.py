from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from datetime import date
from calendar import monthcalendar

month_name = ["styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec",
              "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień"]

Builder.load_file("layouts/calendar.kv")


class Calendar(Screen):
    calendar_date = date.today()

    def on_enter(self, *args):
        self.ids.year_label.text = f"{self.calendar_date.year}"
        self.ids.month_label.text = f"{month_name[self.calendar_date.month - 1].upper()}"
        print(f"year = {self.calendar_date.year}\n month = {self.calendar_date.month}")
        for i in range(6):
            for j in range(7):
                calendar = self.get_calendar(self.calendar_date.year, self.calendar_date.month)
                self.ids.calendar_layout.add_widget(Label(text=f"{calendar[i][j]}", size_hint=(.142, .142), color=(0, 0, 0, 1)))

    def month_to_left(self):
        pass

    def month_to_right(self):
        pass

    def get_calendar(self, year, month):
        previous_month = monthcalendar(year - 1 if month == 1 else year, 12 if month == 1 else month - 1)[4]
        next_month = monthcalendar(year + 1 if month == 12 else year, 1 if month == 12 else month + 1)[0]
        calendar = [["pon", "wto", "śrd", "czw", "pią", "sob", "nie"]]

        for i in range(5):
            calendar.append(monthcalendar(year, month)[i])
            if i == 0:
                for j in range(7):
                    if calendar[i + 1][j] == 0:
                        calendar[i + 1][j] = previous_month[j]
                    else:
                        break
            elif i == 4:
                for j in range(7):
                    if calendar[i + 1][j] == 0:
                        calendar[i + 1][j] = next_month[-(7 - j)]

        return calendar
