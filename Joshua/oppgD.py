
import matplotlib.pyplot as plt
from data.dataleser import les_fil

# Lager 12 tomme lister, en for hver måned
vind = {}

for måned in range(1, 13):
    vind[måned] = []

# Leser CSV-filen (dataleser hopper over manglende målinger og gjør om til tall)
for rad in les_fil("data/oslo_blindern_1954_2025_med_makstemperatur.csv"):

    dato = rad["Tid(norsk normaltid)"]
    vindstyrke = rad["Høyeste middelvind (døgn)"]

    # Hopper over manglende målinger
    if vindstyrke is None:
        continue

    # Legger vindstyrken i riktig måned
    vind[dato.month].append(vindstyrke)


# Lager lister for resultatene
minimum = []
median = []
maksimum = []

# Regner ut statistikken for hver måned
for måned in range(1, 13):

    målinger = vind[måned]

    # Hopper over måneder uten data
    if len(målinger) == 0:
        minimum.append(None)
        median.append(None)
        maksimum.append(None)
        continue

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
