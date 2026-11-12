
import csv
import matplotlib.pyplot as plt

# Lager 12 tomme lister, en for hver måned
vind = {}

for måned in range(1, 13):
    vind[måned] = []

csv_fil = "Joshua/oslo_blindern_1954_2025_med_makstemperatur.csv"
# Leser CSV-filen
with open(csv_fil, encoding="utf-8") as fil:
    leser = csv.reader(fil, delimiter=";")

    overskrift = next(leser)

    # Finner plasseringen til dato og vind i CSV-filen
    dato_plassering = overskrift.index("Tid(norsk normaltid)")
    vind_plassering = overskrift.index("Høyeste middelvind (døgn)")

    for rad in leser:

        dato = rad[dato_plassering]
        vindstyrke = rad[vind_plassering]

        # Hopper over manglende målinger
        if vindstyrke == "-" or vindstyrke == "":
            continue

        # Henter ut måneden fra datoen
        dato_deler = dato.split(".")
        måned = int(dato_deler[1])

        # Gjør vindstyrken om til et tall
        vindstyrke = float(vindstyrke.replace(",", "."))

        # Legger vindstyrken i riktig måned
        vind[måned].append(vindstyrke)


# Lager lister for resultatene
minimum = []
median = []
maksimum = []

# Regner ut statistikken for hver måned
for måned in range(1, 13):

    målinger = vind[måned]

    # Sorterer målingene
    målinger.sort()

    # Finner minimum og maksimum
    minimum.append(målinger[0])
    maksimum.append(målinger[-1])

    # Finner median
    antall = len(målinger)

    if antall % 2 == 1:
        midten = antall // 2
        median.append(målinger[midten])

    else:
        midten = antall // 2
        verdi1 = målinger[midten - 1]
        verdi2 = målinger[midten]

        median.append((verdi1 + verdi2) / 2)


# Lager grafen
måneder = ["Jan", "Feb", "Mar", "Apr", "Mai", "Jun",
           "Jul", "Aug", "Sep", "Okt", "Nov", "Des"]

plt.plot(måneder, minimum, label="Minimum")
plt.plot(måneder, median, label="Median")
plt.plot(måneder, maksimum, label="Maksimum")

plt.xlabel("Måned")
plt.ylabel("Vindstyrke (m/s)")
plt.title("Vindstatistikk Oslo Blindern")

plt.ylim(0, 20)


plt.legend()
plt.grid()
plt.show()
