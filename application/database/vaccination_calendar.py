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
                "values ('Gru??licy', 'Gru??lica jest chorob?? zaka??n??, zwykle rozprzetrzenia si?? drog?? oddechow??.', 0, 1, '1/1', 1);" \
                "values ('Wirusowemu zapaleniu w??troby typu B', 'Wirusowe zapelenie w??troby typu B to jedna z najgor??niejszych chor??b zaka??nych. Do zaka??enia dochodzi przez kontakt z zaka??on?? krwi??, kontakty seksualne z zaka??onymi, poprzez dzielenie si?? sprz??tem podczas stosowania narkotyk??w.', 0, 1, '1/3', 1);" \
                "values ('Wirusowemu zapaleniu w??troby typu B', 'Wirusowe zapelenie w??troby typu B to jedna z najgor??niejszych chor??b zaka??nych. Do zaka??enia dochodzi przez kontakt z zaka??on?? krwi??, kontakty seksualne z zaka??onymi, poprzez dzielenie si?? sprz??tem podczas stosowania narkotyk??w.', 30, 60, '2/3', 1);" \
                "values ('Wirusowemu zapaleniu w??troby typu B', 'Wirusowe zapelenie w??troby typu B to jedna z najgor??niejszych chor??b zaka??nych. Do zaka??enia dochodzi przez kontakt z zaka??on?? krwi??, kontakty seksualne z zaka??onymi, poprzez dzielenie si?? sprz??tem podczas stosowania narkotyk??w.', 180, 210, '3/3', 1);" \
                "values ('Rotawirusom', 'Zaka??enia rotawirusami stanowi?? najpowszechniejsz?? przyczyn?? ostrych biegunek u dzieci. Niemal??e ka??dy 5-latek uleg?? co najmniej raz zara??eniu tym wirusem. Ponadto infekcja rotawirusowa jest gro??na zw??aszcza dla niemowl??t, poniewa?? to one najci????ej przechodz?? chorob??.', 30, 180, '1/1', 1);" \
                "values ('B??onicy, t????cowi, krztu??cowi', 'Szczepionka DTP chroni przed zachorowaniem na trzy choroby: b??onic?? (dyfteryt), t????ec i krztusiec wywo??ywane przez maczugowce b??onicy, laseczki t????ca oraz przez pa??eczki krztu??ca.', 30, 60, '1/7', 1);" \
                "values ('B??onicy, t????cowi, krztu??cowi', 'Szczepionka DTP chroni przed zachorowaniem na trzy choroby: b??onic?? (dyfteryt), t????ec i krztusiec wywo??ywane przez maczugowce b??onicy, laseczki t????ca oraz przez pa??eczki krztu??ca.', 60, 120, '2/7', 1);" \
                "values ('B??onicy, t????cowi, krztu??cowi', 'Szczepionka DTP chroni przed zachorowaniem na trzy choroby: b??onic?? (dyfteryt), t????ec i krztusiec wywo??ywane przez maczugowce b??onicy, laseczki t????ca oraz przez pa??eczki krztu??ca.', 120, 180, '3/7', 1);" \
                "values ('B??onicy, t????cowi, krztu??cowi', 'Szczepionka DTP chroni przed zachorowaniem na trzy choroby: b??onic?? (dyfteryt), t????ec i krztusiec wywo??ywane przez maczugowce b??onicy, laseczki t????ca oraz przez pa??eczki krztu??ca.', 450, 540, '4/7', 1);" \
                "values ('B??onicy, t????cowi, krztu??cowi', 'Szczepionka DTP chroni przed zachorowaniem na trzy choroby: b??onic?? (dyfteryt), t????ec i krztusiec wywo??ywane przez maczugowce b??onicy, laseczki t????ca oraz przez pa??eczki krztu??ca.', 2190, 2555, '5/7', 1);" \
                "values ('B??onicy, t????cowi, krztu??cowi', 'Szczepionka DTP chroni przed zachorowaniem na trzy choroby: b??onic?? (dyfteryt), t????ec i krztusiec wywo??ywane przez maczugowce b??onicy, laseczki t????ca oraz przez pa??eczki krztu??ca. *Szczepionka nieobowi??zkowa ale zalecana.', 5110, 5475, '6/7', 0);" \
                "values ('B??onicy, t????cowi, krztu??cowi', 'Szczepionka DTP chroni przed zachorowaniem na trzy choroby: b??onic?? (dyfteryt), t????ec i krztusiec wywo??ywane przez maczugowce b??onicy, laseczki t????ca oraz przez pa??eczki krztu??ca.', 6935, 7300, '7/7', 1);" \
                "values ('Poliomyelitis', 'Polio, inaczej choroba Heinego???Medina, jest gro??n?? chorob?? zaka??n?? prowadz??c?? do rozwoju pora??enia mi????ni, co skutkuje trwa??ym kalectwem, a nawet ??mierci??. Najskuteczniejsz?? metod?? zapobiegaj??c?? zaka??eniu jest szczepienie przeciw IPV, kt??re prowadzone jest w ramach ??wiatowego Programu Eradykacji Poliomyelitis.', 60, 120, '1/4', 1);" \
                "values ('Poliomyelitis', 'Polio, inaczej choroba Heinego???Medina, jest gro??n?? chorob?? zaka??n?? prowadz??c?? do rozwoju pora??enia mi????ni, co skutkuje trwa??ym kalectwem, a nawet ??mierci??. Najskuteczniejsz?? metod?? zapobiegaj??c?? zaka??eniu jest szczepienie przeciw IPV, kt??re prowadzone jest w ramach ??wiatowego Programu Eradykacji Poliomyelitis.', 120, 180, '2/4', 1);" \
                "values ('Poliomyelitis', 'Polio, inaczej choroba Heinego???Medina, jest gro??n?? chorob?? zaka??n?? prowadz??c?? do rozwoju pora??enia mi????ni, co skutkuje trwa??ym kalectwem, a nawet ??mierci??. Najskuteczniejsz?? metod?? zapobiegaj??c?? zaka??eniu jest szczepienie przeciw IPV, kt??re prowadzone jest w ramach ??wiatowego Programu Eradykacji Poliomyelitis.', 450, 540, '3/4', 1);" \
                "values ('Poliomyelitis', 'Polio, inaczej choroba Heinego???Medina, jest gro??n?? chorob?? zaka??n?? prowadz??c?? do rozwoju pora??enia mi????ni, co skutkuje trwa??ym kalectwem, a nawet ??mierci??. Najskuteczniejsz?? metod?? zapobiegaj??c?? zaka??eniu jest szczepienie przeciw IPV, kt??re prowadzone jest w ramach ??wiatowego Programu Eradykacji Poliomyelitis.', 2190, 2555, '4/4', 1);" \
                "values ('Hib', 'Hib to skr??t od nazwy bakterii Haemophilus influenzae typu b, odpowiedzialnych za ci????kie zachorowania u dzieci do 5 roku ??ycia. Najcz??stszym ??r??d??em zaka??e?? Hib jest bezpo??redni kontakt z nosicielem lub chor?? osob??.', 30, 60, '1/4', 1);" \
                "values ('Hib', 'Hib to skr??t od nazwy bakterii Haemophilus influenzae typu b, odpowiedzialnych za ci????kie zachorowania u dzieci do 5 roku ??ycia. Najcz??stszym ??r??d??em zaka??e?? Hib jest bezpo??redni kontakt z nosicielem lub chor?? osob??.', 60, 120, '2/4', 1);" \
                "values ('Hib', 'Hib to skr??t od nazwy bakterii Haemophilus influenzae typu b, odpowiedzialnych za ci????kie zachorowania u dzieci do 5 roku ??ycia. Najcz??stszym ??r??d??em zaka??e?? Hib jest bezpo??redni kontakt z nosicielem lub chor?? osob??.', 120, 180, '3/4', 1);" \
                "values ('Hib', 'Hib to skr??t od nazwy bakterii Haemophilus influenzae typu b, odpowiedzialnych za ci????kie zachorowania u dzieci do 5 roku ??ycia. Najcz??stszym ??r??d??em zaka??e?? Hib jest bezpo??redni kontakt z nosicielem lub chor?? osob??.', 450, 540, '4/4', 1);" \
                "values ('Pneumokokom', 'Pneumokoki s?? najcz??stsz?? przyczyn?? zapalenia ucha ??rodkowego, kt??re u niekt??rych dzieci ko??czy si?? trwa???? g??uchot??. Zaka??enia pneumokokowe s?? wywo??ywane przez bakteri?? zwan?? pneumokokiem wytwarzaj??c?? otoczk?? polisacharydow??, kt??ra warunkuje rozw??j okre??lonych objaw??w.', 30, 60, '1/3', 1);" \
                "values ('Pneumokokom', 'Pneumokoki s?? najcz??stsz?? przyczyn?? zapalenia ucha ??rodkowego, kt??re u niekt??rych dzieci ko??czy si?? trwa???? g??uchot??. Zaka??enia pneumokokowe s?? wywo??ywane przez bakteri?? zwan?? pneumokokiem wytwarzaj??c?? otoczk?? polisacharydow??, kt??ra warunkuje rozw??j okre??lonych objaw??w.', 90, 120, '2/3', 1);" \
                "values ('Pneumokokom', 'Pneumokoki s?? najcz??stsz?? przyczyn?? zapalenia ucha ??rodkowego, kt??re u niekt??rych dzieci ko??czy si?? trwa???? g??uchot??. Zaka??enia pneumokokowe s?? wywo??ywane przez bakteri?? zwan?? pneumokokiem wytwarzaj??c?? otoczk?? polisacharydow??, kt??ra warunkuje rozw??j okre??lonych objaw??w.', 360, 450, '3/3', 1);" \
                "values ('Odrze, ??wince, r????yczce', 'Odra, ??winka i r????yczka nale???? do chor??b o wysokiej zara??liwo??ci, kt??rym mog?? towarzyszy?? powa??ne powik??ania powoduj??ce trwa??y uszczerbek na zdrowiu. W celu zapobiegania zachorowalno??ci w Polsce od 2004 roku wprowadzono obowi??zek szczepienia przeciw wy??ej wspomnianym chorobom.', 360, 450, '1/2', 1);" \
                "values ('Odrze, ??wince, r????yczce', 'Odra, ??winka i r????yczka nale???? do chor??b o wysokiej zara??liwo??ci, kt??rym mog?? towarzyszy?? powa??ne powik??ania powoduj??ce trwa??y uszczerbek na zdrowiu. W celu zapobiegania zachorowalno??ci w Polsce od 2004 roku wprowadzono obowi??zek szczepienia przeciw wy??ej wspomnianym chorobom.', 2190, 2555, '2/2', 1);" \
                "values ('Grypie', 'Grypa jest ostr?? chorob?? zaka??n??, wywo??ywan?? przez wirusy grypy. Do zaka??enia dochodzi drog?? kropelkow?? lub przez kontakt ze ska??on?? powierzchni??. W celu zapobieganiu grypie mo??na zaszczepi?? si?? szczepionk?? IIV po uko??czeniu 6 m.??. lub LAIV po uko??czeniu 24 m.??. do uko??czenia 18 r.??.', 150, 6935, '1/1', 0);" \
                "values ('Meningokokom', 'Zaka??enia meningokokowe s?? wywo??ywane przez bakterie ??? dwoinki zapalenia opon m??zgowo-rdzeniowych, zwane r??wnie?? meningokokami. Najbardziej niebezpieczna jest inwazyjna choroba meningokokowa (IChM), kt??ra obejmuje zapalenie opon  m??zgowo-rdzeniowych lub seps?? (posocznic??).', 30, 7300, '1/1', 0);" \
                "values ('Ludzkiemu wirusowi brodawczaka', 'Wirus HPV (Human Papillomavirus) to ludzki wirus brodawczaka. Wyr????nia si?? 150 typ??w HPV chorobotw??rczych dla cz??owieka, w??r??d kt??rych, typy 16 i 18 nale???? do wysoko onkogennych typ??w wirusa, kt??re odpowiadaj?? za zmiany przedrakowe szyjki macicy i raka szyjki macicy.', 4380, 7300, '1/1', 0);" \
                "values ('Ospie wietrznej', 'Ospa wietrzna jest ostr?? chorob?? zaka??n?? wywo??an?? przez wirus ospy wietrznej i p????pa??ca. Jest jedn?? z najbardziej zara??liwych chor??b zaka??nych. Najcz??stszym ??r??d??em zaka??enia jest bezpo??redni kontakt z chorym lub droga kropelkowa. Do g????wnych objaw??w choroby nale????: sw??dz??ca wysypka na tu??owiu, twarzy, ow??osionej sk??rze g??owy, ko??czynach, gor??czka, z??e samopoczucie, b??le g??owy i mi????ni.', 2190, 7300, '1/1', 0);" \
                "values ('Wirusowemu zapaleniu w??troby typu B', 'Wirusowe zapalenie w??troby typu B to jedna z najgro??niejszych chor??b zaka??nych. Wywo??uje j?? wirus HBV, kt??ry mo??e wywo??ywa?? zaka??enia ostre lub przewlek??e. Po up??ywie kilku lat mo??e ono doprowadzi?? do rozwoju marsko??ci w??troby. Przewlekle zaka??ona osoba jest r??wnie?? nara??ona na ryzyko raka w??trobowokom??rkowego.', 2190, 7300, '1/1', 0);" \
                "values ('Kleszczowemu zapaleniu m??zgu', 'Kleszczowe zapalenie m??zgu to ostra choroba wirusowa, kt??ra cz??sto wi????e si?? z powik??aniami neurologicznymi. ??r??d??em infekcji mo??e by?? uk??szenie przez zaka??onego kleszcza, poprzez spo??ycie niepasteryzowanego mleka zaka??onego zwierz??cia lub znacznie rzadziej poprzez transfuzj?? krwi lub przeszczep narz??du od osoby w fazie wiremii.', 2190, 7300, '1/1', 0);"

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


def insert_into_vaccination_children(child_id):
    statement = """insert into vaccination_children (child_id, vaccination_id, notification_date)
                    select children.id, vaccinations.id, date(children.birth_date, '+' || vaccinations.days_from || ' days')
                    from children
                    cross join vaccinations
                    where children.id = ?"""

    execute_statement(statement, child_id)


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
