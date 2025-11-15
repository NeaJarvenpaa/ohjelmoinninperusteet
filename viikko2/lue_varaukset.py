from datetime import datetime

def main():
    varaus = "varaukset.txt"

    with open(varaus, "r", encoding="utf-8") as f:
        rivit = f.readlines()

    for rivi in rivit:
        rivi = rivi.strip()
        if not rivi:
            continue

    varaus = varaus.split('|')
    print("DEBUG:", varaus)

    varausnumero = int(varaus[0])
    varaaja = str(varaus[1])
    päivämäärä = datetime.strptime(varaus[2],"%Y-%m-%D")
    aloitusaika= datetime.strptime(varaus[3],"%H:%M")
    tuntimäärä= int(varaus[4])
    tuntihinta = float(varaus[5])
    kokonaishinta = float(tuntimäärä*tuntihinta)
    maksettu = bool(varaus[6])
    kohde = str(varaus[7])
    puhelin = str(varaus[8])
    sähköposti = str(varaus[9])
   
    print(varaus)

    print(f"Varausnumero: {varausnumero}")
    print(f"Varaaja: {varaaja}")
    print(f"Päivämäärä: {päivämäärä}")
    print(f"Aloitusaika: {aloitusaika}")
    print(f"Tuntimäärä: {tuntimäärä}")
    print(f"Tuntihinta: {tuntihinta} €")
    print(f"Kokonaishinta: {kokonaishinta} €")
    print(f"Maksettu: {'Kyllä' if maksettu else 'Ei'}")
    print(f"Kohde: {kohde}")
    print(f"Puhelin: {puhelin}")
    print(f"Sähköposti: {sähköposti}")
    print("-" * 30)

if __name__ == "__main__":
    main()