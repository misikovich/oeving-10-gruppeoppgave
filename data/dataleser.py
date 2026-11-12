# Felles innlesing av CSV-filene i data/-mappen.

# Modulen tar seg av all feilhåndtering ved innlesing, slik at skriptene
# slipper try/except rundt open(), datoer og tall

import csv
import sys
from datetime import datetime

MAPPE = "data"

DATO_KOLONNE = "Tid(norsk normaltid)"
TEKST_KOLONNER = ("Navn", "Stasjon")

STASJONER = {
    "Oslo Blindern": "oslo_blindern_1954_2025_med_makstemperatur.csv",
    "Røros": "roeros_1954_2025_med_makstemperatur.csv",
    "Tromsø": "tromsoe_1954_2025_med_makstemperatur.csv",
    "Værnes": "vaernes_1954_2025_med_makstemperatur.csv",
    "Venabu": "venabu_1954_2025_med_makstemperatur.csv",
    "Sinnes": "sinnes_2014_2025.csv",
}


def til_tall(tekst):
    """konverterer tekst med comma til float"""
    if tekst is None:
        return None
    tekst = tekst.replace(",", ".").strip()
    if tekst in ("", "-"):
        return None
    try:
        return float(tekst)
    except ValueError:
        return None


def til_dato(tekst):
    """konverterer text dato til datetime python"""
    if tekst is None:
        return None
    try:
        return datetime.strptime(tekst.strip(), "%d.%m.%Y")
    except ValueError:
        return None


def finn_sti(navn):
    """finner path til en sti, tar navn som en argument"""
    if navn in STASJONER:
        return MAPPE + "/" + STASJONER[navn]
    if navn.startswith(MAPPE + "/"):
        return navn
    return MAPPE + "/" + navn


def les_fil(navn):
    """finner og leser CSV og returnerer liste med rader/dict
    Returnerer en tom liste og skriver ut feil ved feil
    """
    sti = finn_sti(navn)
    rader = []

    try:
        with open(sti, encoding="utf-8-sig", newline="") as fil:
            leser = csv.DictReader(fil, delimiter=";")

            if leser.fieldnames is None or DATO_KOLONNE not in leser.fieldnames:
                print(f"Feil: {sti} mangler kolonnen '{DATO_KOLONNE}'", file=sys.stderr)
                return []

            for rad in leser:
                dato = til_dato(rad.get(DATO_KOLONNE))
                if dato is None:
                    continue  # kildelinje nederst eller ødelagt rad

                ny_rad = {}
                for kolonne, verdi in rad.items():
                    if kolonne is None:
                        continue  # ekstra felt uten overskrift
                    if kolonne == DATO_KOLONNE:
                        ny_rad[kolonne] = dato
                    elif kolonne in TEKST_KOLONNER:
                        ny_rad[kolonne] = verdi
                    else:
                        ny_rad[kolonne] = til_tall(verdi)
                rader.append(ny_rad)

    except FileNotFoundError:
        print(f"Feil: fant ikke filen {sti}", file=sys.stderr)
        return []
    except PermissionError:
        print(f"Feil: har ikke tilgang til å lese {sti}", file=sys.stderr)
        return []
    except UnicodeDecodeError:
        print(f"Feil: {sti} er ikke en gyldig UTF-8-fil", file=sys.stderr)
        return []
    except csv.Error as feil:
        print(f"Feil: klarte ikke å lese CSV i {sti}: {feil}", file=sys.stderr)
        return []

    return rader
