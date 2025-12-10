# Copyright (c) 2025 Nea Järvenpää
# This code is licensed under the MIT License.

from datetime import datetime, date
from pathlib import Path
import sys

def muunna_tiedot(viikkotiedosto: list) -> list:
    """ Tämä muuntaa tietorivien tietotyypit oikeiksi """
    muutoslista = []
    muutoslista.append(datetime.fromisoformat(viikkotiedosto[0]))
    muutoslista.append(int(viikkotiedosto[1]))
    muutoslista.append(int(viikkotiedosto[2]))
    muutoslista.append(int(viikkotiedosto[3]))
    muutoslista.append(int(viikkotiedosto[4]))
    muutoslista.append(int(viikkotiedosto[5]))
    muutoslista.append(int(viikkotiedosto[6]))
    return muutoslista

def lue_data(viikkotiedosto: str) -> list:
    """Tämä lukee viikkotiedoston ja palauttaa sopivassa rakenteessa"""
    koko_viikon_tiedot = []
    with open(viikkotiedosto, "r", encoding="utf-8") as f:
        next(f)
        for koko_viikon_tieto in f:
            koko_viikon_tieto = koko_viikon_tieto.strip()
            kvt_sarakkeet = koko_viikon_tieto.split(';')
            koko_viikon_tiedot.append(muunna_tiedot(kvt_sarakkeet))
    return koko_viikon_tiedot

def paivan_tiedot(paiva: str, lukemat: list) -> list[float]:
    """ Tämä lukee lukemat ja yhdistää ne oikeisiin sarakkeisiin. """
    pv = int(paiva.split('.')[0])
    kk = int(paiva.split('.')[1])
    v = int(paiva.split('.')[2])
    tiedot_summattu = []
    kulutusV1 = 0
    kulutusV2 = 0
    kulutusV3 = 0
    tuotantoV1 = 0
    tuotantoV2 = 0
    tuotantoV3 = 0
    for lukema in lukemat:
         if lukema[0].date() == date(v, kk, pv):
             kulutusV1 += lukema[1]
             kulutusV2 += lukema[2]
             kulutusV3 += lukema[3]
             tuotantoV1 += lukema[4]
             tuotantoV2 += lukema[5]
             tuotantoV3 += lukema[6]

    tiedot_summattu.append(kulutusV1/1000)
    tiedot_summattu.append(kulutusV2/1000)
    tiedot_summattu.append(kulutusV3/1000)
    tiedot_summattu.append(tuotantoV1/1000)
    tiedot_summattu.append(tuotantoV2/1000)
    tiedot_summattu.append(tuotantoV3/1000)
    return tiedot_summattu

viikonpaivat = {
    0: "Maanantai",
    1: "Tiistai",
    2: "Keskiviikko",
    3: "Torstai",
    4: "Perjantai",
    5: "Lauantai",
    6: "Sunnuntai",
}

def muodosta_paivalista(lukemat: list) -> list[date]:
    """Tämä palauttaa kaikki päivämäärät datasta järjestyksessä."""
    paivat = {lukema[0].date() for lukema in lukemat}
    return sorted(paivat)

def tulosta_paiva_rivi(pv_nimi: str, pvm_str: str, arvot: list[float], out=sys.stdout) -> None:
    """Tämä tulostaa yhden päivän rivin siististi."""
    muotoilut = [f"{x:.2f}".replace('.', ',') for x in arvot]
    print(
        f"{pv_nimi:<12} {pvm_str:<12}  "
        f"{muotoilut[0]:>7}  {muotoilut[1]:>7}  {muotoilut[2]:>7}   "
        f"{muotoilut[3]:>7} {muotoilut[4]:>7} {muotoilut[5]:>7}",
        file=out
    )

def tulosta_otsikko(otsikko: str, out=sys.stdout) -> None:
    """Tämä tulostaa raportin tietorivin tiedostoon."""
    print(otsikko, file=out)
    print("Päivä        Pvm           Kulutus [kWh]                 Tuotanto [kWh]", file=out)
    print("             (pv.kk.vvvv)    v1       v2        v3          v1     v2     v3", file=out)
    print("---------------------------------------------------------------------------", file=out)

def _tyokansio() -> Path:
   """Tämä palauttaa työskentelykansion"""
   return Path.cwd()


def main():
    """Tämä tulostaa raporttiin tiedot viikottain."""
    csv_tiedostot = [
        ("Viikon 41 sähkönkulutus ja -tuotanto (kWh, vaiheittain)", "viikko41.csv"),
        ("Viikon 42 sähkönkulutus ja -tuotanto (kWh, vaiheittain)", "viikko42.csv"),
        ("Viikon 43 sähkönkulutus ja -tuotanto (kWh, vaiheittain)", "viikko43.csv"),
    ]

    raportti_polku = _tyokansio() / "yhteenveto.txt"

    with raportti_polku.open("w", encoding="utf-8", newline="\n") as tiedosto:
        for otsikko, polku in csv_tiedostot:
            print("", file=tiedosto)
            lukemat = lue_data(polku)
            tulosta_otsikko(otsikko, out=tiedosto)
            kaikki_paivat = muodosta_paivalista(lukemat)
            for pvm in kaikki_paivat:
                pvm_str = f"{pvm.day:02d}.{pvm.month:02d}.{pvm.year}"
                pv_nimi = viikonpaivat[pvm.weekday()]
                arvot = paivan_tiedot(pvm_str, lukemat)
                tulosta_paiva_rivi(pv_nimi, pvm_str, arvot, out=tiedosto)
            print("---------------------------------------------------------------------------", file=tiedosto)

    print(f"raportti luotu!")

if __name__ == "__main__":
    main()
