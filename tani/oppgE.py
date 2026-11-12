
import csv
import glob
import matplotlib.pyplot as plt
import math
from datetime import date, datetime
import os


# til_tall og til_dato fra oppgave 7 D
def til_tall(tekst):
    tekst = tekst.replace(",", ".").strip()

    if tekst == "-" or tekst == "":
        return None

    return float(tekst)


def til_dato(tekst):
    tekst = tekst.strip()

    try:
        return datetime.strptime(tekst, "%Y-%m-%d")
    except ValueError:
        try:
            return datetime.strptime(tekst, "%d.%m.%Y")
        except ValueError:
            return None


# oppgave E
def finn_skiføre(csv_sti):
    sesonger = {}

    #velger riktig kolonne for snødybde basert på filnavn
    if "sinnes" in csv_sti.lower():
        snøkolonne = 6
    else:
        snøkolonne = 7

    with open(csv_sti, 'r', encoding='utf-8-sig') as fil:
        leser = csv.reader(fil, delimiter=';')
        next(leser, None)

        for rad in leser:
            if len(rad) <= snøkolonne:
                continue

            dato = til_dato(rad[2])

            if dato is None:
                continue

            snødybde = til_tall(rad[snøkolonne])

            if snødybde is None:
                continue

            if dato.month >= 11:
                aar = dato.year + 1
            elif dato.month <= 5:
                aar = dato.year
            else:
                continue

            if aar not in sesonger:
                sesonger[aar] = {
                    "måledager": set(),
                    "skiføredager": set()
                }

            sesonger[aar]["måledager"].add(dato)

            if snødybde >= 20:
                sesonger[aar]["skiføredager"].add(dato)

    return sesonger


#csv-filene

filer = (
    glob.glob(os.path.join("data", "*_med_makstemperatur.csv"))
    + glob.glob(os.path.join("data", "*sinnes*.csv"))
)

plt.figure(figsize=(12, 6))

for csv_sti in filer:

    sesonger = finn_skiføre(csv_sti)

    årstall = []
    antall_dager = []

    for aar in sorted(sesonger):

        start = date(aar - 1, 11, 1)
        slutt = date(aar, 5, 31)

        dager_i_sesongen = (slutt - start).days + 1

        krav = math.ceil(dager_i_sesongen / 2)

        måledager = len(sesonger[aar]["måledager"])

        
        if måledager >= krav:

            skiføredager = len(sesonger[aar]["skiføredager"])

            årstall.append(aar)
            antall_dager.append(skiføredager)

    
    stasjon = os.path.basename(csv_sti)

    if "sinnes" in stasjon.lower():
        stasjon = "Sinnes"
    else:
        stasjon = stasjon.replace(
            "_1954_2025_med_makstemperatur.csv", ""
        )

    #grafene
    plt.plot(
        årstall,
        antall_dager,
        marker="o",
        label=stasjon
    )


plt.xlabel("Skisesong")
plt.ylabel("Antall dager med skiføre")
plt.title("Antall dager med skiføre per sesong")

plt.legend(title="Værstasjon")
plt.grid(True)
plt.tight_layout()

plt.show()
