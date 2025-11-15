from datetime import datetime
def main():
    varaukset = "varaukset.txt"

    with open(varaukset, "r", encoding="utf-8") as f:
        varaus = f.read().strip()         

    varausnumero = int(varaus.split('|')[0])
    print("Varausnumero:", varausnumero)
    varaajannimi = varaus.split('|')[1]
    print("Varaaja:", varaajannimi)
    paivamaara = datetime.strptime(varaus.split('|')[2], "%Y-%m-%d").date()
    print("Päivämäärä:", paivamaara.strftime("%d.%m.%Y"))
    aloitusaika = datetime.strptime(varaus.split('|')[3], "%H:%M").time()
    print("Aloitusaika:", aloitusaika.strftime("%H.%M"))
    tuntimaara = int(varaus.split('|')[4])
    print("Tuntimäärä:", tuntimaara)
    tuntihinta = float(varaus.split('|')[5])
    print("Tuntihinta:", tuntihinta, "€")
    kokonaishinta = tuntihinta*tuntimaara
    print("Kokonaishinta:", kokonaishinta, "€")
    maksettu = varaus.split('|')[6]
    print(f"Maksettu: {'Kyllä' if maksettu else 'Ei'}")
    varauskohde = varaus.split('|')[7]
    print("Kohde:", varauskohde)
    puhelinnumero = varaus.split('|')[8]
    print("Puhelin:", puhelinnumero)
    sahkoposti = varaus.split('|')[9]
    print("Sähköposti:", sahkoposti)

if __name__ == "__main__":
    main()