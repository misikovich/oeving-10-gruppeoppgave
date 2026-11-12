from data.dataleser import les_fil

aar = input("Skriv inn årstall: ").strip()

sommerdager = 0
hoysommerdager = 0
tropedager = 0

# CSV-filen ligger i data/-mappen
filnavn = "data/oslo_blindern_1954_2025_med_makstemperatur.csv"

for rad in les_fil(filnavn):
    dato = rad["Tid(norsk normaltid)"]
    maks_temp = rad["Maksimumstemperatur (døgn)"]

    # Hopper over andre år og manglende målinger
    if str(dato.year) != aar or maks_temp is None:
        continue

    if maks_temp > 20:
        sommerdager += 1

    if maks_temp > 25:
        hoysommerdager += 1

    if maks_temp > 30:
        tropedager += 1

print(f"Antall dager i {aar}:")
print(f"Sommerdager: {sommerdager}")
print(f"Høysommerdager: {hoysommerdager}")
print(f"Tropedager: {tropedager}")
