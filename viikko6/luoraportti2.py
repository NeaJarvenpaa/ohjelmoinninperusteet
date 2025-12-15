# Copyright (c) 2025 Nea Järvenpää
# This code is licensed under the MIT License.

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, date
import csv

@dataclass
class Mittaus:
    """Tämä muuntaa yhden rivin tietotyypit."""
    aikaleima: datetime
    kulutus_kwh: float
    tuotanto_kwh: float
    lampotila_c: float


def muotoilut(fi_number: str) -> float:
    """Tämä muotoilee tietoja oikeaan muotoon."""
    return float(fi_number.replace(",", "."))


def muotoilut2(value: float) -> str:
    """Tämäkin muotoilee tietoja oikeaan muotoon."""
    return f"{value:.2f}".replace(".", ",")


def lue_data(polku: str) -> list[Mittaus]:
    """ Tämä lukee tiedoston ja palauttaa rivit sopivassa muodossa."""
    data: list[Mittaus] = []
    with open(polku, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader, None)
        for rivi in reader:
            if not rivi or len(rivi) < 4:
                continue
            pvm = datetime.fromisoformat(rivi[0])
            kulutus = muotoilut(rivi[1])
            tuotanto = muotoilut(rivi[2])
            lampotila = muotoilut(rivi[3])
            data.append(Mittaus(pvm, kulutus, tuotanto, lampotila))
    return data


KUUKAUDET = [
    "Tammikuu", "Helmikuu", "Maaliskuu", "Huhtikuu",
    "Toukokuu", "Kesäkuu", "Heinäkuu", "Elokuu",
    "Syyskuu", "Lokakuu", "Marraskuu", "Joulukuu"
]


def raportti_aikavalilta(alku: date, loppu: date, data: list[Mittaus]) -> str:
    """Tämä luo raportin valitulta aikaväliltä."""
    raportti = "-----------------------------------------------------\n"
    raportti += f"Raportti väliltä {alku.day}.{alku.month}.{alku.year}-"
    raportti += f"{loppu.day}.{loppu.month}.{loppu.year}\n"

    kulutus = 0.0
    tuotanto = 0.0
    lampotila = 0.0

    for m in data:
        pvm = m.aikaleima.date()
        if alku <= pvm <= loppu:
            kulutus += m.kulutus_kwh
            tuotanto += m.tuotanto_kwh
            lampotila += m.lampotila_c


    tunnit = (loppu - alku).days * 24

    raportti += "- Kokonaiskulutus: " + muotoilut2(kulutus) + " kWh\n"
    raportti += "- Kokonaistuotanto: " + muotoilut2(tuotanto) + " kWh\n"
    raportti += (
        "- Keskilämpötila: "
        + muotoilut2(lampotila / tunnit if tunnit != 0 else 0.0)
        + " °C\n"
    )
    raportti += "-----------------------------------------------------\n"
    return raportti


def raportti_kuukaudelta(kuukausi: int, data: list[Mittaus]) -> str:
    """Tämä luo raportin valitulta kuukaudelta."""
    raportti = "-----------------------------------------------------\n"
    raportti += f"Raportti kuulta: {KUUKAUDET[kuukausi - 1]} \n"

    kulutus = 0.0
    tuotanto = 0.0
    lampotila = 0.0
    rivien_lkm = 0

    for m in data:
        if m.aikaleima.date().month == kuukausi:
            kulutus += m.kulutus_kwh
            tuotanto += m.tuotanto_kwh
            lampotila += m.lampotila_c
            rivien_lkm += 1

    raportti += "- Kokonaiskulutus: " + muotoilut2(kulutus) + " kWh\n"
    raportti += "- Kokonaistuotanto: " + muotoilut2(tuotanto) + " kWh\n"
    raportti += (
        "- Keskilämpötila: "
        + muotoilut2(lampotila / (rivien_lkm * 24) if rivien_lkm != 0 else 0.0)
        + " °C\n"
    )
    raportti += "-----------------------------------------------------\n"
    return raportti


def raportti_vuodelta(data: list[Mittaus]) -> str:
    """Tämä raportoi koko vuoden tiedot."""
    raportti = "-----------------------------------------------------\n"
    vuosi = data[0].aikaleima.date().year if data else "tuntematon"
    raportti += f"Raportti vuodelta: {vuosi} \n"

    kulutus = 0.0
    tuotanto = 0.0
    lampotila = 0.0
    rivien_lkm = 0

    for m in data:
        kulutus += m.kulutus_kwh
        tuotanto += m.tuotanto_kwh
        lampotila += m.lampotila_c
        rivien_lkm += 1

    raportti += "- Kokonaiskulutus: " + muotoilut2(kulutus) + " kWh\n"
    raportti += "- Kokonaistuotanto: " + muotoilut2(tuotanto) + " kWh\n"
    raportti += (
        "- Keskilämpötila: "
        + muotoilut2(lampotila / (rivien_lkm * 24) if rivien_lkm != 0 else 0.0)
        + " °C\n"
    )
    raportti += "-----------------------------------------------------\n"
    return raportti


def kirjoita_raportti_tiedostoon(raportti: str, polku: str = "raportti.txt") -> None:
    """Tämä kirjoittaa raportin tiedostoon."""
    with open(polku, "w", encoding="utf-8") as f:
        f.write(raportti)


def kysy_kokonaisluku(kehotus: str, min_arvo: int, max_arvo: int) -> int:
    """Tämä kysyy käyttäjältä kokonaisluvun annetulta väliltä."""
    while True:
        try:
            val = int(input(kehotus))
            if not (min_arvo <= val <= max_arvo):
                raise ValueError
            return val
        except Exception:
            print(f"Valintaasi ei hyväksytä. Anna numero välillä {min_arvo}-{max_arvo}.")


def kysy_paiva(kehotus: str) -> date:
    """Kysyy päivämäärän muodossa 'pv.kk.vvvv'."""
    try:
        osat = input(kehotus).split(".")
        pv, kk, vv = int(osat[0]), int(osat[1]), int(osat[2])
        return date(vv, kk, pv)
    except Exception:
        raise ValueError("Valintaasi ei hyväksytä. Anna päivämäärä muodossa pv.kk.vvvv.")


def paavalikko() -> list:
    """Tämä kysyy käyttäjältä kysymyksiä ja etenee vastausten mukaan.."""
    print("-----------------------------------------------------")
    print("Valitse minkälaisen raportin haluat:")
    print("1) Päiväkohtainen yhteenveto valitulta aikaväliltä.")
    print("2) Kuukausikohtainen yhteenveto tietylle kuukaudelle.")
    print("3) Vuoden 2025 kokonaisyhteenveto.")
    print("4) Lopeta ohjelma.")
    print("-----------------------------------------------------")

    valinta = kysy_kokonaisluku("Valitse numero väliltä 1-4.", 1, 4)

    if valinta == 1:
        try:
            alku = kysy_paiva("Anna alkupäivä (pv.kk.vvvv): ")
            loppu = kysy_paiva("Anna loppupäivä (pv.kk.vvvv): ")
            return [0, 1, alku, loppu]
        except ValueError:
            print("Valintaasi ei hyväksytä. Anna päivämäärät muodossa pv.kk.vvvv. Palataan alkuun.")
            return paavalikko()

    elif valinta == 2:
        try:
            kk = kysy_kokonaisluku("Anna kuukauden numero väliltä 1–12. ", 1, 12)
            return [0, 2, kk]
        except Exception:
            print("Valintaasi ei hyväksytä. Anna numero välillä 1-12. Palataan alkuun.")
            return paavalikko()

    elif valinta == 3:
        return [0, 3]
    elif valinta == 4:
        return [0, 4]
    else:
        return paavalikko()


def alavalikko() -> list:
    """Tämä tulostaa kysymykset konsoliin."""
    print("-----------------------------------------------------")
    print("Mitä haluat tehdä seuraavaksi?")
    print("1) Kirjoita nykyinen raportti tiedostoon raportti.txt")
    print("2) Luo toisenlainen raportti")
    print("3) Lopeta ohjelma.")
    print("-----------------------------------------------------")

    valinta = kysy_kokonaisluku("Valitse numero väliltä 1-3.", 1, 3)
    return [1, valinta]


def main() -> None:
    """Tämä tulostaa raportit konsoliin ja etenee käyttäjän valintojen mukaan."""
    koko_vuoden_tiedot = lue_data("2025.csv")

    while True:
        valinnat = paavalikko()

        if valinnat[1] == 1:
            raportti = raportti_aikavalilta(valinnat[2], valinnat[3], koko_vuoden_tiedot)
            print(raportti)

        elif valinnat[1] == 2:
            raportti = raportti_kuukaudelta(valinnat[2], koko_vuoden_tiedot)
            print(raportti)

        elif valinnat[1] == 3:
            raportti = raportti_vuodelta(koko_vuoden_tiedot)
            print(raportti)

        elif valinnat[1] == 4:
            break
        else:
            continue

        jatko = alavalikko()
        if jatko[1] == 1:
            kirjoita_raportti_tiedostoon(raportti)
            continue
        elif jatko[1] == 2:
            continue
        elif jatko[1] == 3:
            break


if __name__ == "__main__":
    main()
