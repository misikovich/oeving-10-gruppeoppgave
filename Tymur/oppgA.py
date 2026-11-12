from datetime import datetime
import matplotlib.pyplot as plt
from data.dataleser import les_fil

csv_fil = "data/sinnes_2014_2025.csv"
stasjon = "Sinnes"

kolonner = {
    "temp": "Middeltemperatur (døgn)",
    "nedbør": "Nedbør (døgn)",
    "vind": "Høyeste middelvind (døgn)",
    "snø": "Snødybde",
}

# dikt (år, måned) for å liste gyldige måneder 
måneder = {}

for rad in les_fil(csv_fil):
    dato = rad["Tid(norsk normaltid)"]

    nøkkel = (dato.year, dato.month)
    if nøkkel not in måneder:
        måneder[nøkkel] = {"temp": [], "nedbør": [], "vind": [], "snø": []}

    for navn in kolonner:
        verdi = rad[kolonner[navn]]
        if verdi is not None:
            måneder[nøkkel][navn].append(verdi)


def maks(liste):
    if len(liste) == 0:
        return None
    return max(liste)


def minst(liste):
    if len(liste) == 0:
        return None
    return min(liste)


datoer = []
maks_snø = []
total_nedbør = []
maks_temp = []
min_temp = []
maks_vind = []

for år, måned in sorted(måneder):
    data = måneder[(år, måned)]

    datoer.append(datetime(år, måned, 1))
    maks_snø.append(maks(data["snø"]))
    maks_temp.append(maks(data["temp"]))
    min_temp.append(minst(data["temp"]))
    maks_vind.append(maks(data["vind"]))

    if len(data["nedbør"]) > 20:
        total_nedbør.append(sum(data["nedbør"]))
    else:
        total_nedbør.append(None)
        print(f"{måned:02d}.{år}: ikke registrert total nedbør")


def plott(akse, verdier, tittel, farge):
    # None blir til hull i grafen
    y = [float("nan") if v is None else v for v in verdier]
    akse.plot(datoer, y, color=farge, label=tittel)


fig, (akse1, akse2, akse3, akse4) = plt.subplots(4, 1, figsize=(12, 10), sharex=True)

plott(akse1, maks_snø, "Maks snødybde", "tab:blue")
akse1.set_ylabel("Snødybde (cm)")

akse2.bar(datoer, [0 if v is None else v for v in total_nedbør], width=25, label="Total nedbør")
akse2.set_ylabel("Nedbør (mm)")

plott(akse3, maks_temp, "Maks middeltemperatur", "tab:red")
plott(akse3, min_temp, "Min middeltemperatur", "tab:cyan")
akse3.set_ylabel("Temperatur (°C)")

plott(akse4, maks_vind, "Maks middelvind", "tab:green")
akse4.set_ylabel("Vind (m/s)")
akse4.set_xlabel("Måned")

for akse in (akse1, akse2, akse3, akse4):
    akse.legend(loc="upper left")
    akse.grid()

fig.suptitle(f"Månedlige værdata {stasjon}")
plt.tight_layout()
plt.show()
