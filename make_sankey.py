#!/usr/bin/env python
"""
Auswertung Bundeshaushalt

https://stackoverflow.com/questions/70293723/how-do-i-make-a-simple-multi-level-sankey-diagram-with-plotly
https://plotly.com/python/sankey-diagram/
"""
import sys
import sqlite3
import plotly.graph_objects as go


label_list = ['Bundeshaushalt']
source = []
target = []
value = []

def get_data(cur):
    """
    Einnahmen und Ausgaben ermitteln
    """
    nr = 0
    # Einnahmen
    cur.execute("""
    SELECT substr(titel_text,0,60),soll
    FROM hh_2024
    WHERE einahmen_ausgaben='E'
    ORDER BY soll DESC
    LIMIT 20
    """)
    for (titel_text, soll) in cur.fetchall():
        nr += 1
        #print(f'{titel_text}  {soll}')
        titel_text = str(titel_text) + ' ' + str(round(soll/1000000,1)) + ' Mrd.'
        label_list.append(titel_text)
        source.append(nr)
        target.append(0)
        value.append(soll)
    # Ausgaben
    cur.execute("""
    SELECT f.funktion_text,sum(h.soll)
    FROM hh_2024 AS h
    LEFT JOIN funktion AS f ON h.funktion=f.funktion
    WHERE h.einahmen_ausgaben='A'
    GROUP BY h.funktion
    ORDER BY sum(h.soll) DESC
    LIMIT 30
    """)
    for (titel_text, soll) in cur.fetchall():
        nr += 1
        #print(f'{titel_text}  {soll}')
        titel_text = str(titel_text) + ' ' + str(round(soll/1000000,1)) + ' Mrd.'
        label_list.append(titel_text)
        source.append(0)
        target.append(nr)
        value.append(soll)
    # Test
    #print(label_list, source, target, value)


def erstelle_sankey():
    fig = go.Figure(data=[go.Sankey(
        node = {"label": label_list},
        link = {"source": source, "target": target, "value": value}
        )])
    fig.update_layout(title_text="Bundeshaushalt 2024", font_size=10)
    fig.show()


def main():
    """entry point"""
    if len(sys.argv) != 2:
        print('Erstellt Sankey Diagramm für Bundeshaushalt\n'
              'Benutzung:\n'
              f'{sys.argv[0]} DATABASE\n')
        sys.exit(1)
    # connect to the database
    con = sqlite3.connect(sys.argv[1])
    cur = con.cursor()   # new database cursor
    #
    get_data(cur)
    erstelle_sankey()
    #
    con.commit()
    con.close()


if __name__ == '__main__':
    main()
