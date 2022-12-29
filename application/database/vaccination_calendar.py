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
                    child_id integer,
                    name text,
                    information text,
                    days_from integer,
                    days_to integer,
                    is_done boolean default 0,
                    FOREIGN KEY (child_id) REFERENCES children(id))"""

    execute_statement(statement)


def crate_children_table():
    statement = """create table if not exists children (
                id integer primary key,
                name text,
                birth_date text)"""

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
