from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from datetime import date
from calendar import monthcalendar, weekheader

from kivymd.uix.button import MDIconButton
from kivymd.uix.pickers import MDDatePicker

month_name = ["styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec",
              "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień"]


Builder.load_file("layouts/calendar.kv")


class Calendar(Screen):
    calendar_date = date.today()



    def on_enter(self, *args):
        self.ids.year_label.text = f"{self.calendar_date.year}"
        self.ids.month_label.text = f"{month_name[self.calendar_date.month - 1].upper()}"

        self.generate_calendar()

    def set_date(self):
        date_dialog = MDDatePicker(title="Wybierz datę")
        date_dialog.bind(on_save=self.save_date)
        date_dialog.open()

    def save_date(self, instance, value, date_range):
        self.calendar_date = self.calendar_date.replace(year=value.year, month=value.month, day=value.day)
        self.ids.year_label.text = f"{self.calendar_date.year}"
        self.ids.month_label.text = f"{month_name[self.calendar_date.month - 1].upper()}"
        self.generate_calendar()

    def generate_calendar(self):
        self.ids.calendar_layout.clear_widgets()
        for weekday in weekheader(3).split(" "):
            label = MDIconButton(icon=f"images/icons/{weekday}.png", size_hint=(1, 1), disabled=True)
            self.ids.calendar_layout.add_widget(label)
        for i in range(5):
            for j in range(7):
                calendar = self.get_calendar(self.calendar_date.year, self.calendar_date.month)
                btn = MDIconButton(icon=f"images/icons/numeric-{calendar[i + 1][j]}.png", size_hint=(1, 1))
                self.ids.calendar_layout.add_widget(btn)

    def change_month(self, side):
        active_month = self.calendar_date.month
        if side == "left":
            if active_month == 1:
                self.calendar_date = self.calendar_date.replace(month=self.calendar_date.month + 11)
            else:
                self.calendar_date = self.calendar_date.replace(month=self.calendar_date.month - 1)
        else:
            if active_month == 12:
                self.calendar_date = self.calendar_date.replace(month=self.calendar_date.month - 11)
            else:
                self.calendar_date = self.calendar_date.replace(month=self.calendar_date.month + 1)

        self.ids.month_label.text = f"{month_name[self.calendar_date.month - 1].upper()}"
        self.generate_calendar()

    def change_year(self, side):

        if side == "left":
            self.calendar_date = self.calendar_date.replace(year=self.calendar_date.year - 1)
        else:
            self.calendar_date = self.calendar_date.replace(year=self.calendar_date.year + 1)

        self.ids.year_label.text = f"{self.calendar_date.year}"
        self.generate_calendar()


    def get_calendar(self, year, month):
        previous_month = monthcalendar(year - 1 if month == 1 else year,
                                       12 if month == 1 else month - 1)[len(monthcalendar(year - 1 if month == 1 else year,
                                                                                          12 if month == 1 else month - 1)) - 1]
        next_month = monthcalendar(year + 1 if month == 12 else year, 1 if month == 12 else month + 1)[0]
        calendar = [["pon", "wto", "śrd", "czw", "pią", "sob", "nie"]]

        for i in range(5):
            calendar.append(monthcalendar(year, month)[i])
            if i == 0:
                for j in range(7):
                    if calendar[i + 1][j] == 0:
                        calendar[i + 1][j] = f"{previous_month[j]}w"
                    else:
                        break
            elif i == 4:
                for j in range(7):
                    if calendar[i + 1][j] == 0:
                        calendar[i + 1][j] = f"{next_month[-(7 - j)]}w"

        return calendar
