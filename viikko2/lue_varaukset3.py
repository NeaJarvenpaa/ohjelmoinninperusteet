from datetime import datetime

def main():
    varaukset = "varaukset.txt"

    with open(varaukset, "r", encoding="utf-8") as f:
        rivit = f.readlines()

    for rivi in rivit:
        osat = rivi.strip()
        if not rivi:
            continue
        
        osat = rivi.split('|')
        if len(osat) < 10:
            print("Virheellinen rivi:", rivi)
            continue

        varausnumero = int(osat[0])
        varaajannimi = osat[1]
        paivamaara = datetime.strptime(osat[2], "%Y-%m-%d").date()
        aloitusaika = datetime.strptime(osat[3], "%H:%M").time()
        tuntimaara = int(osat[4])
        tuntihinta = float(osat[5])
        kokonaishinta = tuntihinta * tuntimaara
        maksettu = osat[6] == "True"
        varauskohde = osat[7]
        puhelinnumero = osat[8]
        sahkoposti = osat[9]

        print(f"""
Varausnumero: {varausnumero}
Varaaja: {varaajannimi}
Päivämäärä: {paivamaara.strftime("%d.%m.%Y")}
Aloitusaika: {aloitusaika.strftime("%H.%M")}
Tuntimäärä: {tuntimaara}
Tuntihinta: {tuntihinta} €
Kokonaishinta: {kokonaishinta} €
Maksettu: {'Kyllä' if maksettu else 'Ei'}
Kohde: {varauskohde}
Puhelin: {puhelinnumero}
Sähköposti: {sahkoposti}
""")

if __name__ == "__main__":
    main()