--
--
--
.mode table
.width 2 55 2 10

---------- Einnahmen ----------

.print
.print Bundeshaushalt 2024 Einnahmen, Einzelplan
.print
SELECT '∑' AS '∑', sum(soll) AS betrag
FROM hh_2024
WHERE einahmen_ausgaben='E'
;
SELECT einzelplan AS ep,einzelplan_text,einahmen_ausgaben AS ea,sum(soll) AS betrag
FROM hh_2024
WHERE einahmen_ausgaben='E'
GROUP BY einzelplan_text
ORDER BY betrag DESC
;

.print
.print Bundeshaushalt 2024 Einnahmen, Allgemeine Finanzverwaltung, Einzelplan
.print
SELECT einzelplan AS ep,kapitel_text,einahmen_ausgaben AS ea,sum(soll) AS betrag
FROM hh_2024
WHERE einahmen_ausgaben='E' AND einzelplan='60'
GROUP BY kapitel_text
ORDER BY betrag DESC
;

.print
.print Bundeshaushalt 2024 Einnahmen, Steuern, Einzelplan
.print
SELECT einzelplan AS ep,titel_text,einahmen_ausgaben AS ea,sum(soll) AS betrag
FROM hh_2024
WHERE einahmen_ausgaben='E' AND einzelplan='60' AND kapitel='6001'
GROUP BY titel_text
ORDER BY betrag DESC
;

---------- Ausgaben ----------

.print
.print Bundeshaushalt 2024 Ausgaben, Einzelplan
.print
SELECT '∑' AS '∑', sum(soll) AS betrag
FROM hh_2024
WHERE einahmen_ausgaben='A'
;
SELECT einzelplan AS ep,einzelplan_text,einahmen_ausgaben AS ea,sum(soll) AS betrag
FROM hh_2024
WHERE einahmen_ausgaben='A'
GROUP BY einzelplan_text
ORDER BY betrag DESC
;

.print
.print Bundeshaushalt 2024 Ausgaben, Bundesministerium für Arbeit und Soziales
.print
SELECT einzelplan AS ep,kapitel_text,einahmen_ausgaben AS ea,sum(soll) AS betrag
FROM hh_2024
WHERE einahmen_ausgaben='A' AND einzelplan='11'
GROUP BY kapitel_text
ORDER BY betrag DESC
;

---------- Größte Einnahmen und Ausgaben ----------

.print
.print 'Größte Einahmenposten'
.print
.width 2 1 7 3 90
SELECT einzelplan,einahmen_ausgaben,titel,funktion,titel_text,soll
FROM hh_2024
WHERE einahmen_ausgaben='E'
ORDER BY soll DESC
LIMIT 15
;

.print
.print 'Größte Ausgabenposten'
.print
.width 2 1 7 3 90
SELECT einzelplan,einahmen_ausgaben,titel,funktion,titel_text,soll
FROM hh_2024
WHERE einahmen_ausgaben='A'
ORDER BY soll DESC
LIMIT 15
;

.print
.print 'Die 20 größten Ausgabenposten (gruppiert nach Funktion)'
.print
.width 8 70 20
SELECT h.funktion,f.funktion_text,sum(h.soll) AS summe
FROM hh_2024 AS h
LEFT JOIN funktion AS f ON h.funktion=f.funktion
WHERE h.einahmen_ausgaben='A'
GROUP BY h.funktion
ORDER BY sum(h.soll) DESC
LIMIT 20
;
