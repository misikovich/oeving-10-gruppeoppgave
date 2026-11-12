import csv
import os
from datetime import date, datetime
import matplotlib.pyplot as plt

mappe = "data"
stasjoner = {
    "Oslo Blindern": "oslo_blindern_1954_2025_med_makstemperatur.csv",
    "Røros": "roeros_1954_2025_med_makstemperatur.csv",
    "Tromsø": "tromsoe_1954_2025_med_makstemperatur.csv",
    "Værnes": "vaernes_1954_2025_med_makstemperatur.csv",
    "Venabu": "venabu_1954_2025_med_makstemperatur.csv",
    "Sinnes": "sinnes_2014_2025.csv",
}


def til_tall(tekst):
    tekst = tekst.replace(",", ".").strip()
    if tekst == "-" or tekst == "":
        return None
    return float(tekst)


def skiføre_per_sesong(filnavn):
    målinger = {}
    skiføre = {}

    with open(filnavn, encoding="utf-8-sig") as fil:
        leser = csv.reader(fil, delimiter=";")
        overskrift = next(leser)
        snø_kol = overskrift.index("Snødybde")

        for rad in leser:
            try:
                dato = datetime.strptime(rad[2], "%d.%m.%Y")
                snø = til_tall(rad[snø_kol])
            except (ValueError, IndexError):
                continue
            if snø is None:
                continue

            # Sesongen 1. november til 31. mai, oppkalt etter året den slutter
            if dato.month >= 11:
                sesong = dato.year + 1
            elif dato.month <= 5:
                sesong = dato.year
            else:
                continue

            målinger[sesong] = målinger.get(sesong, 0) + 1
            if snø >= 20:
                skiføre[sesong] = skiføre.get(sesong, 0) + 1

    år = []
    dager = []
    for sesong in sorted(målinger):
        dager_i_sesong = (date(sesong, 5, 31) - date(sesong - 1, 11, 1)).days + 1
        if målinger[sesong] >= dager_i_sesong / 2:
            år.append(sesong)
            dager.append(skiføre.get(sesong, 0))
    return år, dager


plt.figure(figsize=(12, 6))
for navn, fil in stasjoner.items():
    år, dager = skiføre_per_sesong(os.path.join(mappe, fil))
    plt.plot(år, dager, marker="o", label=navn)

plt.xlabel("Skisesong (år sesongen slutter)")
plt.ylabel("Dager med skiføre (snødybde ≥ 20 cm)")
plt.title("Antall dager med skiføre per sesong")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
