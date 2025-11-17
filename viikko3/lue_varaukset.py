from datetime import datetime

def hae_varaaja(varaus):
    nimi = varaus[1]
    print(f"Varaaja: {nimi}")

def hae_varausnumero(varaus):
    numero = varaus[0]
    print(f"Varausnumero: {numero}")

def hae_paiva(varaus):
    paiva = datetime.strptime(varaus[2], "%Y-%m-%d").date()
    print(f"Päivämäärä: {paiva.strftime("%d.%m.%Y")}")

def hae_aloitusaika(varaus):
    aloitus = datetime.strptime(varaus[3], "%H:%M").time()
    print(f"Aloitusaika: {aloitus.strftime("%H:%M")}")

def  hae_tuntimaara(varaus):
    kesto = varaus[4]
    print(f"Tuntimäärä: {kesto}")

def  hae_tuntihinta(varaus):
    tuntitaksa = varaus[5]
    print(f"Tuntihinta: {tuntitaksa} €")

def laske_kokonaishinta(varaus):
    tuntimaara = int(varaus[4])
    tuntihinta = float(varaus[5])
    kokonaishinta = tuntihinta*tuntimaara
    print(f"Kokonaishinta: {kokonaishinta} €")

def hae_maksettu(varaus):
    maksettu = varaus[6]
    print(f"Maksettu: {'Kyllä' if maksettu else 'Ei'}")

def hae_kohde(varaus):
    paikka = varaus[7]
    print(f"Kohde: {paikka}")

def hae_puhelin(varaus):
    numero = varaus[8]
    print(f"Puhelinnumero: {numero}")

def hae_sahkoposti(varaus):
    sapo = varaus[9]
    print(f"Sähköposti: {sapo}")

def main():
    varaukset = "varaukset.txt"

    with open(varaukset, "r", encoding="utf-8") as f:
        varaus = f.read().strip()
        varaus = varaus.split('|')

    hae_varausnumero(varaus)
    hae_varaaja(varaus)
    hae_paiva(varaus)
    hae_aloitusaika(varaus)
    hae_tuntimaara(varaus)
    hae_tuntihinta(varaus)
    laske_kokonaishinta(varaus)
    hae_maksettu(varaus)
    hae_kohde(varaus)
    hae_puhelin(varaus)
    hae_sahkoposti(varaus)

if __name__ == "__main__":
    main()
