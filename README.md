# chaostreff-nuernberg

Website for https://chaostreff-nuernberg.de


## Skriptaufbau

### appointments.inc.php

Das Skript setzt die Daten (erster Donnerstag bzw. dritter Dienstag) pro Monat, ausser es steht in der Datei `appointments.csv` ein anderes Datum.

### appointments.csv

location | year-month | appointment
lab | 2019-06 | 11.06.2019
k4cg | 2020-01 | 09.01.2020

#### location

Muss entweder `lab` oder `k4cg` sein. Alle anderen Werte werden ignoriert -> die Zeile nicht beachtet

#### year-month

Das Jahr und Monat wo der Treff an einem anderen Tag stattfinden wird.

#### appointment

Das Datum das auf der Webseite statt des Regeltermins angezeigt werden soll.
