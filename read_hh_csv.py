#!/usr/bin/env python
"""
Auswertung Bundeshaushalt
"""
import os
import sys
import sqlite3


def read_hh_file(cur, filepath):
    """
    Einlesen einer Bundeshaushalt CSV Datei in eine SQLite Datenbank
    """
    filename = os.path.basename(filepath)
    tablename = filename[:7].lower()
    print(f"read '{filepath}' -> table '{tablename}'")
    cur.execute(f'DROP TABLE IF EXISTS {tablename}')
    cur.execute(f'''
    CREATE TABLE {tablename} (
     einzelplan             TEXT,
     einzelplan_text        TEXT,
     einahmen_ausgaben      TEXT,
     einahmen_ausgaben_text TEXT,
     kapitel                TEXT,
     kapitel_text           TEXT,
     titel                  TEXT,
     funktion               TEXT,
     titel_text             TEXT,
     flex                   TEXT,
     seite                  TEXT,
     soll                   INTEGER,
     titelgruppe            TEXT,
     tgr_text               TEXT
    )
    ''')
    file = open(filepath, 'r')
    for line in file:
        #print(line)
        line += ';;'
        col = line.split(';')
        #print(col)
        #print(len(col))
        #print(line.rstrip())  # whitespace rechts entfernen
        # strip() -> alle whitespace entfernen
        cur.execute(f'INSERT INTO {tablename} VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                     (col[0].strip('"'),
                      col[1].strip('"'),
                      col[2].strip('"'),
                      col[3].strip('"'),
                      col[4].strip('"'),
                      col[5].strip('"'),
                      col[6].strip('"'),
                      col[7].strip('"'),
                      col[8].strip('"'),
                      col[9].strip('"'),
                      col[10].strip('"'),
                      col[11].strip('"'),
                      col[12].strip('"'),
                      col[13].strip('"')
                    )
        )
    file.close()


def add_table_funktion(cur):
    """Erstellt rudimentäre Umsetztabelle der Funktionsnummern mit Kurzbeschreibung"""
    print("add table 'funktion'")
    cur.executescript('''
    DROP TABLE IF EXISTS funktion;
    CREATE TABLE funktion (
     funktion TEXT,
     funktion_text TEXT
    );
    INSERT INTO funktion VALUES ('011', 'Ausgaben Deutscher Bundestag');
    INSERT INTO funktion VALUES ('018', 'Versorgung der Beamten');
    INSERT INTO funktion VALUES ('023', 'Entwicklungshilfe');
    INSERT INTO funktion VALUES ('031', 'Bundeswehrverwaltung');
    INSERT INTO funktion VALUES ('032', 'Verteidigung Bundeswehr');
    INSERT INTO funktion VALUES ('039', 'Versorgung der Soldaten');
    INSERT INTO funktion VALUES ('061', 'Steuer- und Zollverwaltung');
    INSERT INTO funktion VALUES ('164', 'Forschungsförderung');
    INSERT INTO funktion VALUES ('165', 'Ausgaben für Forschung');
    INSERT INTO funktion VALUES ('221', 'Steuerzuschuss für die Renter*innen');
    INSERT INTO funktion VALUES ('224', 'Gesundheitsfond');
    INSERT INTO funktion VALUES ('229', 'Sonstige Sozialversicherungen');
    INSERT INTO funktion VALUES ('232', 'Elterngeld und Mutterschutz');
    INSERT INTO funktion VALUES ('251', 'Bürgergeld');
    INSERT INTO funktion VALUES ('252', 'Leistungen für Unterkunft und Heizung');
    INSERT INTO funktion VALUES ('282', 'Grundsicherung im Alter und bei Erwerbsminderung');
    INSERT INTO funktion VALUES ('721', 'Bundesautobahnen');
    INSERT INTO funktion VALUES ('742', 'Zuschüsse Deutsche Bahn AG');
    INSERT INTO funktion VALUES ('813', 'Sondervermögen (???)');
    INSERT INTO funktion VALUES ('830', 'Zinsen für die Staatsschulden');
    ''')


def main():
    """entry point"""
    if len(sys.argv) == 1:
        print('List CSV Dateien des Bundeshaushalt in eine SQLite Datenbank ein.\n'
              'Benutzung:\n'
              f'{sys.argv[0]} CSV_FILE1 CSV_FILE2 ...\n')
        sys.exit(1)
    con = sqlite3.connect('bundeshaushalt.db')
    cur = con.cursor()
    for index in range(1, len(sys.argv)):
        read_hh_file(cur, sys.argv[index])
    add_table_funktion(cur)
    con.commit()
    con.close()


if __name__ == '__main__':
    main()
