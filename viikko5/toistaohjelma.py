#Copyright (c) 2025 Nea Järvenpää
#This code is licensed under the MIT License.

from datetime import datetime, date

def muunna_tiedot(viikkotiedosto: list) -> list:
    """ Tämä muuntaa tietorivien tietotyypit oikeiksi"""
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
    """ Tämä lukee lukemat ja yhdistää ne oikeisiin sarakkeisiin"""
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

PAIVAN_NIMET = {
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

def tulosta_paiva_rivi(pv_nimi: str, pvm_str: str, arvot: list[float]) -> None:
    """Tämähän tulostaa yhden päivän rivin siististi."""
    muotoillut = [f"{x:.2f}".replace('.', ',') for x in arvot]
    print(f"{pv_nimi:<12} {pvm_str:<12}  {muotoillut[0]:>7}  {muotoillut[1]:>7}  {muotoillut[2]:>7}"
          f"{muotoillut[3]:>7} {muotoillut[4]:>7} {muotoillut[5]:>7}")

def main():
    """Tämä tulostaa koko viikon tiedot siististi."""
    lukemat = lue_data("viikko42.csv")

    print("Viikon 42 sähkönkulutus ja -tuotanto (kWh, vaiheittain)", end="\n\n")
    print("Päivä        Pvm           Kulutus [kWh]                 Tuotanto [kWh]")
    print("             (pv.kk.vvvv)   v1      v2      v3             v1     v2     v3")
    print("---------------------------------------------------------------------------")

    kaikki_paivat = muodosta_paivalista(lukemat)

    for pvm in kaikki_paivat:
        pvm_str = f"{pvm.day}.{pvm.month}.{pvm.year}"
        pv_nimi = PAIVAN_NIMET[pvm.weekday()]
        arvot = paivan_tiedot(pvm_str, lukemat)
        tulosta_paiva_rivi(pv_nimi, pvm_str, arvot)


if __name__ == "__main__":
    main()