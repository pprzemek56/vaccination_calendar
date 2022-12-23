import sqlite3


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
                birth_date text,
                days_age integer)"""

    execute_statement(statement)


"""
Children table methods
"""


def get_children():
    statement = "select * from children"

    with sqlite3.connect("vaccination_calendar.db") as conn:
        cursor = conn.cursor()
        cursor.execute(statement)
        children_list = [{"id": child[0], "name": child[1], "birth_date": child[2], "days_age": child[3]}
                         for child in cursor.fetchall()]
        conn.commit()

    return children_list




def execute_statement(statement, **kwargs):
    with sqlite3.connect("vaccination_calendar.db") as conn:
        cursor = conn.cursor()
        cursor.execute(statement)
        conn.commit()


if __name__ == "__main__":
    main()
