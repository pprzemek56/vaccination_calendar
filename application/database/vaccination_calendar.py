import sqlite3
from datetime import date


def main():
    pass


def create_calendar_sheets_table():
    statement = """create table if not exists calendar_sheets(
                    id integer primary key,
                    child_id integer,
                    title text,
                    note text,
                    created_at text,
                    end_at text,
                    foreign key (child_id) references children(id))"""

    execute_statement(statement)


def create_vaccinations_table():
    statement = """create table if not exists vaccinations(
                    id integer primary key,
                    name text,
                    information text,
                    days_from integer,
                    days_to integer,
                    does text,
                    mandatory boolean)"""

    execute_statement(statement)


def crate_children_table():
    statement = """create table if not exists children (
                id integer primary key,
                name text,
                birth_date text)"""

    execute_statement(statement)


def create_vaccination_children_table():
    statement = """create table if not exists vaccination_children (
                id integer primary key,
                child_id integer,
                vaccination_id integer,
                done boolean,
                foreign key (child_id) references children(id),
                foreign key (vaccination_id) references vaccinations(id))"""

    execute_statement(statement)


"""
    Children table methods
"""


def get_children():
    statement = "select * from children"

    with sqlite3.connect("database/vaccination_calendar.db") as conn:
        cursor = conn.cursor()
        cursor.execute(statement)
        children_list = [{"id": child[0], "name": child[1], "birth_date": child[2]}
                         for child in cursor.fetchall()]
        conn.commit()

    return children_list


def add_child(name, birth_date):
    statement = "insert into children(name, birth_date) values (?, ?)"

    execute_statement(statement, name, date.fromisoformat(birth_date))


def get_child(child_id):
    statement = "select * from children where id = ?"

    with sqlite3.connect("database/vaccination_calendar.db") as conn:
        cursor = conn.cursor()
        cursor.execute(statement, child_id)
        fetched = cursor.fetchone()
        child = {"id": fetched[0], "name": fetched[1], "birth_date": fetched[2]}
        conn.commit()

    return child


def update_name(child_id, name):
    statement = "update children set name = ? where id = ?"

    execute_statement(statement, name, child_id)


def update_date(child_id, birth_date):
    statement = "update children set birth_date = ? where id = ?"

    execute_statement(statement, birth_date, child_id)


def insert_into_vaccination():
    statement = "insert into vaccinations(name, information, days_from, days_to, dose, mandatory)" \
                "values ('Gruźlicy', '', 0, 1, '1/1', 1);" \
                "values ('Wirusowemu zapaleniu wątroby typu B', '', 0, 1, '1/3', 1);" \
                "values ('Wirusowemu zapaleniu wątroby typu B', '', 30, 60, '2/3', 1);" \
                "values ('Wirusowemu zapaleniu wątroby typu B', '', 180, 210, '3/3', 1);" \
                "values ('Rotawirusom', '', 30, 180, '1/1', 1);" \
                "values ('Błonicy, tężcowi, krztuścowi', '', 30, 60, '1/7', 1);" \
                "values ('Błonicy, tężcowi, krztuścowi', '', 60, 120, '2/7', 1);" \
                "values ('Błonicy, tężcowi, krztuścowi', '', 120, 180, '3/7', 1);" \
                "values ('Błonicy, tężcowi, krztuścowi', '', 450, 540, '4/7', 1);" \
                "values ('Błonicy, tężcowi, krztuścowi', '', 2190, 2555, '5/7', 1);" \
                "values ('Błonicy, tężcowi, krztuścowi', '', 5110, 5475, '6/7', 0);" \
                "values ('Błonicy, tężcowi, krztuścowi', '', 6935, 7300, '7/7', 1);" \
                "values ('Poliomyelitis', '', 60, 120, '1/4', 1);" \
                "values ('Poliomyelitis', '', 120, 180, '2/4', 1);" \
                "values ('Poliomyelitis', '', 450, 540, '3/4', 1);" \
                "values ('Poliomyelitis', '', 2190, 2555, '4/4', 1);" \
                "values ('Hib', '', 30, 60, '1/4', 1);" \
                "values ('Hib', '', 60, 120, '2/4', 1);" \
                "values ('Hib', '', 120, 180, '3/4', 1);" \
                "values ('Hib', '', 450, 540, '4/4', 1);" \
                "values ('Pneumokokom', '', 30, 60, '1/3', 1);" \
                "values ('Pneumokokom', '', 90, 120, '2/3', 1);" \
                "values ('Pneumokokom', '', 360, 450, '3/3', 1);" \
                "values ('Odrze, śwince, różyczce', '', 360, 450, '1/2', 1);" \
                "values ('Odrze, śwince, różyczce', '', 2190, 2555, '2/2', 1);" \
                "values ('Grypie', '', 150, 6935, '1/1', 0);" \
                "values ('Meningokokom', '', 30, 7300, '1/1', 0);" \
                "values ('Ludzkiemu wirusowi brodawczaka', '', 4380, 7300, '1/1', 0);" \
                "values ('Ospie wietrznej', '', 2190, 7300, '1/1', 0);" \
                "values ('Wirusowemu zapaleniu wątroby typu B', '', 2190, 7300, '1/1', 0);" \
                "values ('kleszczowemu zapaleniu mózgu', '', 2190, 7300, '1/1', 0);"


def execute_statement(statement, *args):
    if len(args) == 0:
        with sqlite3.connect("database/vaccination_calendar.db") as conn:
            cursor = conn.cursor()
            cursor.execute(statement)
    else:
        with sqlite3.connect("database/vaccination_calendar.db") as conn:
            cursor = conn.cursor()
            cursor.execute(statement, args)
            conn.commit()


if __name__ == "__main__":
    main()
