
import matplotlib.pyplot as plt
import math
from datetime import date
from data.dataleser import les_fil, STASJONER


# oppgave E
def finn_skiføre(stasjon):
    sesonger = {}

    for rad in les_fil(stasjon):

        dato = rad["Tid(norsk normaltid)"]
        snødybde = rad["Snødybde"]

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


plt.figure(figsize=(12, 6))

for stasjon in STASJONER:

    sesonger = finn_skiføre(stasjon)

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
