import sqlite3
from datetime import date


def main():
    pass


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
                notification_date date,
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

    return child


def get_child_id(name):
    statement = "select id from children where name = ?"

    with sqlite3.connect("database/vaccination_calendar.db") as conn:
        cursor = conn.cursor()
        cursor.execute(statement, (name,))
        fetched = cursor.fetchone()
        child_id = int(fetched[0])

    return child_id


def update_name(child_id, name):
    statement = "update children set name = ? where id = ?"

    execute_statement(statement, name, child_id)


def update_date(child_id, birth_date):
    statement = "update children set birth_date = ? where id = ?"

    execute_statement(statement, birth_date, child_id)


"""
    Vaccination table methods
"""


def insert_into_vaccination():
    statement = "insert into vaccinations(name, information, days_from, days_to, dose, mandatory)" \
                "values ('Gruźlicy', 'Gruźlica jest chorobą zakaźną, zwykle rozprzetrzenia się drogą oddechową.', 0, 1, '1/1', 1);" \
                "values ('Wirusowemu zapaleniu wątroby typu B', 'Wirusowe zapelenie wątroby typu B to jedna z najgorźniejszych chorób zakaźnych. Do zakażenia dochodzi przez kontakt z zakażoną krwią, kontakty seksualne z zakażonymi, poprzez dzielenie się sprzętem podczas stosowania narkotyków.', 0, 1, '1/3', 1);" \
                "values ('Wirusowemu zapaleniu wątroby typu B', 'Wirusowe zapelenie wątroby typu B to jedna z najgorźniejszych chorób zakaźnych. Do zakażenia dochodzi przez kontakt z zakażoną krwią, kontakty seksualne z zakażonymi, poprzez dzielenie się sprzętem podczas stosowania narkotyków.', 30, 60, '2/3', 1);" \
                "values ('Wirusowemu zapaleniu wątroby typu B', 'Wirusowe zapelenie wątroby typu B to jedna z najgorźniejszych chorób zakaźnych. Do zakażenia dochodzi przez kontakt z zakażoną krwią, kontakty seksualne z zakażonymi, poprzez dzielenie się sprzętem podczas stosowania narkotyków.', 180, 210, '3/3', 1);" \
                "values ('Rotawirusom', 'Zakażenia rotawirusami stanowią najpowszechniejszą przyczynę ostrych biegunek u dzieci. Niemalże każdy 5-latek uległ co najmniej raz zarażeniu tym wirusem. Ponadto infekcja rotawirusowa jest groźna zwłaszcza dla niemowląt, ponieważ to one najciężej przechodzą chorobę.', 30, 180, '1/1', 1);" \
                "values ('Błonicy, tężcowi, krztuścowi', 'Szczepionka DTP chroni przed zachorowaniem na trzy choroby: błonicę (dyfteryt), tężec i krztusiec wywoływane przez maczugowce błonicy, laseczki tężca oraz przez pałeczki krztuśca.', 30, 60, '1/7', 1);" \
                "values ('Błonicy, tężcowi, krztuścowi', 'Szczepionka DTP chroni przed zachorowaniem na trzy choroby: błonicę (dyfteryt), tężec i krztusiec wywoływane przez maczugowce błonicy, laseczki tężca oraz przez pałeczki krztuśca.', 60, 120, '2/7', 1);" \
                "values ('Błonicy, tężcowi, krztuścowi', 'Szczepionka DTP chroni przed zachorowaniem na trzy choroby: błonicę (dyfteryt), tężec i krztusiec wywoływane przez maczugowce błonicy, laseczki tężca oraz przez pałeczki krztuśca.', 120, 180, '3/7', 1);" \
                "values ('Błonicy, tężcowi, krztuścowi', 'Szczepionka DTP chroni przed zachorowaniem na trzy choroby: błonicę (dyfteryt), tężec i krztusiec wywoływane przez maczugowce błonicy, laseczki tężca oraz przez pałeczki krztuśca.', 450, 540, '4/7', 1);" \
                "values ('Błonicy, tężcowi, krztuścowi', 'Szczepionka DTP chroni przed zachorowaniem na trzy choroby: błonicę (dyfteryt), tężec i krztusiec wywoływane przez maczugowce błonicy, laseczki tężca oraz przez pałeczki krztuśca.', 2190, 2555, '5/7', 1);" \
                "values ('Błonicy, tężcowi, krztuścowi', 'Szczepionka DTP chroni przed zachorowaniem na trzy choroby: błonicę (dyfteryt), tężec i krztusiec wywoływane przez maczugowce błonicy, laseczki tężca oraz przez pałeczki krztuśca. *Szczepionka nieobowiązkowa ale zalecana.', 5110, 5475, '6/7', 0);" \
                "values ('Błonicy, tężcowi, krztuścowi', 'Szczepionka DTP chroni przed zachorowaniem na trzy choroby: błonicę (dyfteryt), tężec i krztusiec wywoływane przez maczugowce błonicy, laseczki tężca oraz przez pałeczki krztuśca.', 6935, 7300, '7/7', 1);" \
                "values ('Poliomyelitis', 'Polio, inaczej choroba Heinego–Medina, jest groźną chorobą zakaźną prowadzącą do rozwoju porażenia mięśni, co skutkuje trwałym kalectwem, a nawet śmiercią. Najskuteczniejszą metodą zapobiegającą zakażeniu jest szczepienie przeciw IPV, które prowadzone jest w ramach Światowego Programu Eradykacji Poliomyelitis.', 60, 120, '1/4', 1);" \
                "values ('Poliomyelitis', 'Polio, inaczej choroba Heinego–Medina, jest groźną chorobą zakaźną prowadzącą do rozwoju porażenia mięśni, co skutkuje trwałym kalectwem, a nawet śmiercią. Najskuteczniejszą metodą zapobiegającą zakażeniu jest szczepienie przeciw IPV, które prowadzone jest w ramach Światowego Programu Eradykacji Poliomyelitis.', 120, 180, '2/4', 1);" \
                "values ('Poliomyelitis', 'Polio, inaczej choroba Heinego–Medina, jest groźną chorobą zakaźną prowadzącą do rozwoju porażenia mięśni, co skutkuje trwałym kalectwem, a nawet śmiercią. Najskuteczniejszą metodą zapobiegającą zakażeniu jest szczepienie przeciw IPV, które prowadzone jest w ramach Światowego Programu Eradykacji Poliomyelitis.', 450, 540, '3/4', 1);" \
                "values ('Poliomyelitis', 'Polio, inaczej choroba Heinego–Medina, jest groźną chorobą zakaźną prowadzącą do rozwoju porażenia mięśni, co skutkuje trwałym kalectwem, a nawet śmiercią. Najskuteczniejszą metodą zapobiegającą zakażeniu jest szczepienie przeciw IPV, które prowadzone jest w ramach Światowego Programu Eradykacji Poliomyelitis.', 2190, 2555, '4/4', 1);" \
                "values ('Hib', 'Hib to skrót od nazwy bakterii Haemophilus influenzae typu b, odpowiedzialnych za ciężkie zachorowania u dzieci do 5 roku życia. Najczęstszym źródłem zakażeń Hib jest bezpośredni kontakt z nosicielem lub chorą osobą.', 30, 60, '1/4', 1);" \
                "values ('Hib', 'Hib to skrót od nazwy bakterii Haemophilus influenzae typu b, odpowiedzialnych za ciężkie zachorowania u dzieci do 5 roku życia. Najczęstszym źródłem zakażeń Hib jest bezpośredni kontakt z nosicielem lub chorą osobą.', 60, 120, '2/4', 1);" \
                "values ('Hib', 'Hib to skrót od nazwy bakterii Haemophilus influenzae typu b, odpowiedzialnych za ciężkie zachorowania u dzieci do 5 roku życia. Najczęstszym źródłem zakażeń Hib jest bezpośredni kontakt z nosicielem lub chorą osobą.', 120, 180, '3/4', 1);" \
                "values ('Hib', 'Hib to skrót od nazwy bakterii Haemophilus influenzae typu b, odpowiedzialnych za ciężkie zachorowania u dzieci do 5 roku życia. Najczęstszym źródłem zakażeń Hib jest bezpośredni kontakt z nosicielem lub chorą osobą.', 450, 540, '4/4', 1);" \
                "values ('Pneumokokom', 'Pneumokoki są najczęstszą przyczyną zapalenia ucha środkowego, które u niektórych dzieci kończy się trwałą głuchotą. Zakażenia pneumokokowe są wywoływane przez bakterię zwaną pneumokokiem wytwarzającą otoczkę polisacharydową, która warunkuje rozwój określonych objawów.', 30, 60, '1/3', 1);" \
                "values ('Pneumokokom', 'Pneumokoki są najczęstszą przyczyną zapalenia ucha środkowego, które u niektórych dzieci kończy się trwałą głuchotą. Zakażenia pneumokokowe są wywoływane przez bakterię zwaną pneumokokiem wytwarzającą otoczkę polisacharydową, która warunkuje rozwój określonych objawów.', 90, 120, '2/3', 1);" \
                "values ('Pneumokokom', 'Pneumokoki są najczęstszą przyczyną zapalenia ucha środkowego, które u niektórych dzieci kończy się trwałą głuchotą. Zakażenia pneumokokowe są wywoływane przez bakterię zwaną pneumokokiem wytwarzającą otoczkę polisacharydową, która warunkuje rozwój określonych objawów.', 360, 450, '3/3', 1);" \
                "values ('Odrze, śwince, różyczce', 'Odra, świnka i różyczka należą do chorób o wysokiej zaraźliwości, którym mogą towarzyszyć poważne powikłania powodujące trwały uszczerbek na zdrowiu. W celu zapobiegania zachorowalności w Polsce od 2004 roku wprowadzono obowiązek szczepienia przeciw wyżej wspomnianym chorobom.', 360, 450, '1/2', 1);" \
                "values ('Odrze, śwince, różyczce', 'Odra, świnka i różyczka należą do chorób o wysokiej zaraźliwości, którym mogą towarzyszyć poważne powikłania powodujące trwały uszczerbek na zdrowiu. W celu zapobiegania zachorowalności w Polsce od 2004 roku wprowadzono obowiązek szczepienia przeciw wyżej wspomnianym chorobom.', 2190, 2555, '2/2', 1);" \
                "values ('Grypie', 'Grypa jest ostrą chorobą zakaźną, wywoływaną przez wirusy grypy. Do zakażenia dochodzi drogą kropelkową lub przez kontakt ze skażoną powierzchnią. W celu zapobieganiu grypie można zaszczepić się szczepionką IIV po ukończeniu 6 m.ż. lub LAIV po ukończeniu 24 m.ż. do ukończenia 18 r.ż.', 150, 6935, '1/1', 0);" \
                "values ('Meningokokom', 'Zakażenia meningokokowe są wywoływane przez bakterie – dwoinki zapalenia opon mózgowo-rdzeniowych, zwane również meningokokami. Najbardziej niebezpieczna jest inwazyjna choroba meningokokowa (IChM), która obejmuje zapalenie opon  mózgowo-rdzeniowych lub sepsę (posocznicę).', 30, 7300, '1/1', 0);" \
                "values ('Ludzkiemu wirusowi brodawczaka', 'Wirus HPV (Human Papillomavirus) to ludzki wirus brodawczaka. Wyróżnia się 150 typów HPV chorobotwórczych dla człowieka, wśród których, typy 16 i 18 należą do wysoko onkogennych typów wirusa, które odpowiadają za zmiany przedrakowe szyjki macicy i raka szyjki macicy.', 4380, 7300, '1/1', 0);" \
                "values ('Ospie wietrznej', 'Ospa wietrzna jest ostrą chorobą zakaźną wywołaną przez wirus ospy wietrznej i półpaśca. Jest jedną z najbardziej zaraźliwych chorób zakaźnych. Najczęstszym źródłem zakażenia jest bezpośredni kontakt z chorym lub droga kropelkowa. Do głównych objawów choroby należą: swędząca wysypka na tułowiu, twarzy, owłosionej skórze głowy, kończynach, gorączka, złe samopoczucie, bóle głowy i mięśni.', 2190, 7300, '1/1', 0);" \
                "values ('Wirusowemu zapaleniu wątroby typu B', 'Wirusowe zapalenie wątroby typu B to jedna z najgroźniejszych chorób zakaźnych. Wywołuje ją wirus HBV, który może wywoływać zakażenia ostre lub przewlekłe. Po upływie kilku lat może ono doprowadzić do rozwoju marskości wątroby. Przewlekle zakażona osoba jest również narażona na ryzyko raka wątrobowokomórkowego.', 2190, 7300, '1/1', 0);" \
                "values ('Kleszczowemu zapaleniu mózgu', 'Kleszczowe zapalenie mózgu to ostra choroba wirusowa, która często wiąże się z powikłaniami neurologicznymi. Źródłem infekcji może być ukąszenie przez zakażonego kleszcza, poprzez spożycie niepasteryzowanego mleka zakażonego zwierzęcia lub znacznie rzadziej poprzez transfuzję krwi lub przeszczep narządu od osoby w fazie wiremii.', 2190, 7300, '1/1', 0);"

    execute_statement(statement)


def get_vaccination():
    statement = "select distinct name from vaccinations"

    with sqlite3.connect("database/vaccination_calendar.db") as conn:
        cursor = conn.cursor()
        cursor.execute(statement)
        fetched = cursor.fetchall()
        vaccination = [v[0] for v in fetched]

    return vaccination


def get_vaccination_by_name(name):
    statement = "select * from vaccinations where name = ?"

    with sqlite3.connect("database/vaccination_calendar.db") as conn:
        cursor = conn.cursor()
        cursor.execute(statement, (name,))
        fetched = cursor.fetchone()
        vaccination = {"name": fetched[1], "information": fetched[2], "days_from": fetched[3], "days_to": fetched[4],
                       "dose": fetched[5].split("/")[1], "mandatory": True if fetched[6] == 1 else False}

    return vaccination


"""
    Vaccination_Children table methods
"""


def insert_into_vaccination_children(child_id):
    statement = "insert into vaccination_children(child_id, vaccination_id) select ?, id from vaccinations"

    execute_statement(statement, child_id)


def get_child_vaccination(child_id):
    statement = "select vaccinations.name, vaccinations.days_from, vaccinations.days_to, vaccinations.dose, done" \
                " from vaccination_children" \
                " inner join vaccinations" \
                " on vaccination_children.vaccination_id = vaccinations.id" \
                " where child_id = ?"

    with sqlite3.connect("database/vaccination_calendar.db") as conn:
        cursor = conn.cursor()
        cursor.execute(statement, child_id)
        fetched = cursor.fetchall()
        vaccination_list = [{"name": v[0], "from": v[1], "to": v[2], "dose": v[3], "done": True if v[4] else False}
                            for v in fetched]

    return vaccination_list


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
