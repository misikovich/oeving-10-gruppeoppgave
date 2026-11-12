import matplotlib.pyplot as plt
from data.dataleser import les_fil, STASJONER


def årlig_snittemperatur(stasjon):
    # summer og tell middeltemperaturen for hvert år
    summer = {}
    antall = {}

    for rad in les_fil(stasjon):
        dato = rad["Tid(norsk normaltid)"]
        temp = rad["Middeltemperatur (døgn)"]
        if temp is None:
            continue

        summer[dato.year] = summer.get(dato.year, 0) + temp
        antall[dato.year] = antall.get(dato.year, 0) + 1

    år = []
    snitt = []
    for årstall in sorted(summer):
        # Nok data om det er målinger for minst 300 dager
        if antall[årstall] >= 300:
            år.append(årstall)
            snitt.append(summer[årstall] / antall[årstall])
    return år, snitt


plt.figure(figsize=(12, 6))
for navn in STASJONER:
    år, snitt = årlig_snittemperatur(navn)
    plt.plot(år, snitt, marker="o", markersize=3, label=navn)

plt.xlabel("År")
plt.ylabel("Gjennomsnittstemperatur (°C)")
plt.title("Årlig gjennomsnittstemperatur per værstasjon")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
