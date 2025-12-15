# Copyright (c) 2025 Nea Järvenpää
# This code is licensed under the MIT License.

from datetime import datetime, date

def muunna_tiedot(tietokentta: list) -> list:
    """ Tämä muuntaa rivien tietotyypit oikeiksi ja erottimeksi pisteen."""
    return [
        datetime.fromisoformat(tietokentta[0]),
        float(tietokentta[1].replace(",", ".")),
        float(tietokentta[2].replace(",", ".")),
        float(tietokentta[3].replace(",", ".")),
    ]


def lue_data(vuoden_tiedot: str) -> list:
    """Tämä lukee vuoden CSV-tiedoston ja palauttaa tiedot sopivassa rakenteessa ja tietotyypeissä."""
    tiedot = []
    with open(vuoden_tiedot, "r", encoding="utf-8") as f:
        next(f)
        for tietokentta in f:
            tietokentta = tietokentta.split(";")
            tiedot.append(muunna_tiedot(tietokentta))

    return tiedot


def raportin_luonti(raportti: str):
    """ Tämä kirjoittaa sisällön tiedostoon."""
    with open("raportti.txt", "w", encoding="utf-8") as f:
        f.write(raportti)


def raportti_aikavalilta(
    alkaa: datetime.date, loppuu: datetime.date, tiedot: list
) -> str:
    """ Tämä luo raportin käyttäjän valitsemalta aikaväliltä."""
    raportti = "-----------------------------------------------------\n"
    raportti += f"Raportti väliltä {alkaa.day}.{alkaa.month}.{alkaa.year}-"
    raportti += f"{loppuu.day}.{loppuu.month}.{loppuu.year}\n"
    kulutus = 0
    tuotanto = 0
    lampotila = 0

    for paivamaara in tiedot:
        if alkaa <= paivamaara[0].date() <= loppuu:
            kulutus += paivamaara[1]
            tuotanto += paivamaara[2]
            lampotila += paivamaara[3]

    raportti += "- Kokonaiskulutus: " + f"{kulutus:.2f}".replace(".", ",") + " kWh\n"
    raportti += "- Kokonaistuotanto: " + f"{tuotanto:.2f}".replace(".", ",") + " kWh\n"
    raportti += (
        "- Keskilämpötila: "
        + f"{(lampotila/((loppuu - alkaa).days*24)):.2f}".replace(".", ",")
        + " °C\n"
    )
    raportti += "-----------------------------------------------------\n"
    return raportti

def raportti_kuukaudelta(kuukausi: int, tiedot: list) -> str:
    """ Tämä raportoi yhden kuukauden tiedot."""
    kuukaudet = ["Tammikuu", "Helmikuu", "Maaliskuu", "Huhtikuu", "Toukokuu", "Kesäkuu", "Heinäkuu", "Elokuu", "Syyskuu", "Lokakuu", "Marraskuu", "Joulukuu"]
    raportti = "-----------------------------------------------------\n"
    raportti += f"Raportti kuulta: {kuukaudet[kuukausi-1]} \n"
    kulutus = 0
    tuotanto = 0
    lampotila = 0
    paivien_lkm = 0

    for paivamaara in tiedot:
        if paivamaara[0].date().month == kuukausi:
            kulutus += paivamaara[1]
            tuotanto += paivamaara[2]
            lampotila += paivamaara[3]
            paivien_lkm += 1

    raportti += "- Kokonaiskulutus: " + f"{kulutus:.2f}".replace(".", ",") + " kWh\n"
    raportti += "- Kokonaistuotanto: " + f"{tuotanto:.2f}".replace(".", ",") + " kWh\n"


    raportti += (
        "- Keskilämpötila: "
        + f"{(lampotila/(paivien_lkm*24)):.2f}".replace(".", ",")
        + " °C\n"
    )
    raportti += "-----------------------------------------------------\n"
    return raportti

def raportti_vuodelta(tiedot: list) -> str:
    """ Tämä raportoi koko vuoden tiedot."""
    raportti = "-----------------------------------------------------\n"
    raportti += f"Raportti vuodelta: {tiedot[0][0].date().year} \n"
    kulutus = 0
    tuotanto = 0
    lampotila = 0
    paivien_lkm = 0

    for paiva in tiedot:
        kulutus += paiva[1]
        tuotanto += paiva[2]
        lampotila += paiva[3]
        paivien_lkm += 1

    raportti += "- Kokonaiskulutus: " + f"{kulutus:.2f}".replace(".", ",") + " kWh\n"
    raportti += "- Kokonaistuotanto: " + f"{tuotanto:.2f}".replace(".", ",") + " kWh\n"


    raportti += (
        "- Keskilämpötila: "
        + f"{(lampotila/(paivien_lkm*24)):.2f}".replace(".", ",")
        + " °C\n"
    )
    raportti += "-----------------------------------------------------\n"
    return raportti

def valikot(ylavalikko: bool, alavalikko: bool) -> list:
    """ Tämä luo valikot ja palauttaa valinnat."""

    while True and ylavalikko:
        print("-----------------------------------------------------")
        print("Valitse minkälaisen raportin haluat:")
        print("1) Päiväkohtainen yhteenveto valitulta aikaväliltä.")
        print("2) Kuukausikohtainen yhteenveto tietylle kuukaudelle.")
        print("3) Vuoden 2025 kokonaisyhteenveto.")
        print("4) Lopeta ohjelma.")
        print("-----------------------------------------------------")
        try:
            valinta = int(input("Valitse numero väliltä 1-4."))
            if not (1 <= valinta <= 4):
                raise ValueError
        except:
            print("Valintaasi ei hyväksytä. Anna numero väliltä 1-4.")
            continue

        if valinta == 1:
            try:
                alkaa = input("Anna alkamispäivä (pv.kk.vvvv): ").split(".")
                loppuu = input("Anna loppumispäivä (pv.kk.vvvv): ").split(".")
                valinnat = [
                    0,
                    1,
                    date(int(alkaa[2]), int(alkaa[1]), int(alkaa[0])),
                    date(int(loppuu[2]), int(loppuu[1]), int(loppuu[0])),
                ]
                break
            except:
                print(
                    "Valintaasi ei hyväksytä. Anna päivämäärät muodossa pv.kk.vvvv. Palataan alkuun."
                )
                continue

        elif valinta == 2:
            try:
                kuukausi = int(input("Anna kuukauden numero väliltä 1–12. "))
                valinnat = [0, 2, kuukausi]
                break
            except:
                print(
                    "Valintaasi ei hyväksytä. Anna numero väliltä 1-12. Palataan alkuun."
                )
                continue

        elif valinta == 3:
            valinnat = [0, 3]
            break
        elif valinta == 4:
            valinnat = [0, 4]
            break
        else:
            continue

    while True and alavalikko:
        print("-----------------------------------------------------")
        print("Mitä haluat tehdä seuraavaksi?")
        print("1) Kirjoita nykyinen raportti tiedostoon raportti.txt")
        print("2) Luo toisenlainen raportti")
        print("3) Lopeta ohjelma.")
        print("-----------------------------------------------------")
        try:
            valinta = int(input("Valitse numero väliltä 1-3."))
            if not (1 <= valinta <= 3):
                raise ValueError
        except:
            print("Valintaasi ei hyväksytä. Anna numero väliltä 1-3.")
            continue

        valinnat = [1, valinta]
        break

    return valinnat


def main():
    """Tämä kysyy käyttäjältä kysymyksiä ja etenee käyttäjän vastausten mukaisesti sekä luo raportteja tiedostoon."""

    koko_vuoden_tiedot = lue_data("2025.csv")

    while True:
        ylavalikko = valikot(True, False)
        if ylavalikko[1] == 1:
            raportti = raportti_aikavalilta(ylavalikko[2], ylavalikko[3], koko_vuoden_tiedot)
            print(raportti)
        elif ylavalikko[1] == 2:
            raportti = raportti_kuukaudelta(ylavalikko[2], koko_vuoden_tiedot)
            print(raportti)
        elif ylavalikko[1] == 3:
            raportti = raportti_vuodelta(koko_vuoden_tiedot)
            print(raportti)
        elif ylavalikko[1] == 4:
            break

        alavalikko = valikot(False, True)
        if alavalikko[1] == 1:
            raportin_luonti(raportti)
            continue
        elif alavalikko[1] == 2:
            continue
        elif alavalikko[1] == 3:
            break


if __name__ == "__main__":
    main()