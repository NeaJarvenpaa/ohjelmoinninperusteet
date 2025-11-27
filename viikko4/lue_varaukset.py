from datetime import datetime

def muunna_varaustiedot(varaus: list) -> list:
    muutettu_varaus = []
    muutettu_varaus.append(int(varaus[0]))
    muutettu_varaus.append(str(varaus[1]))
    muutettu_varaus.append(str(varaus[2]))
    muutettu_varaus.append(str(varaus[3]))
    muutettu_varaus.append(datetime.strptime(varaus[4], "%Y-%m-%d").date())
    muutettu_varaus.append(datetime.strptime(varaus[5], "%H:%M").time())
    muutettu_varaus.append(int(varaus[6]))
    muutettu_varaus.append(float(varaus[7]))
    muutettu_varaus.append(bool(varaus[8].lower() == "true"))
    muutettu_varaus.append(str(varaus[9]))
    muutettu_varaus.append(datetime.strptime(varaus[10], "%Y-%m-%d %H:%M:%S"))
    return muutettu_varaus

def hae_varaukset(varaustiedosto: str) -> list:
    varaukset = []
    varaukset.append(["varausId", "nimi", "sähköposti", "puhelin", "varauksenPvm", "varauksenKlo", "varauksenKesto", "hinta", "varausVahvistettu", "varattuTila", "varausLuotu"])
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for varaus in f:
            varaus = varaus.strip()
            varaustiedot = varaus.split('|')
            varaukset.append(muunna_varaustiedot(varaustiedot))
    return varaukset

def vahvistetut_varaukset(varaukset: list):
    for varaus in varaukset[1:]:
        if(varaus[8]):
            print (f"- {varaus[1]}, {varaus[9]}, {varaus[4].strftime('%d.%m.%Y')} klo {varaus[5].strftime('%H.%M')}")

    print()

def pitkat_varaukset(varaukset: list):
    for varaus in varaukset[1:]:
        if(varaus[6] >= 3):
            print(f"- {varaus[1]}, {varaus[4].strftime('%d.%m.%Y')} klo {varaus[5].strftime('%H.%M')}, kesto {varaus[6]} h, {varaus[9]}")

    print()

def varausten_vahvistusstatus(varaukset: list):
    for varaus in varaukset[1:]:
        if(varaus[8]):
            print(f"{varaus[1]} → Vahvistettu")
        else:
            print(f"{varaus[1]} → Ei ole vahvistettu")

    print()

def varausten_lkm(varaukset: list):
    onvahvistettu = 0
    eivahvistettu = 0
    for varaus in varaukset[1:]:
        if(varaus[8]):
            onvahvistettu += 1
        else:
            eivahvistettu += 1

    print(f"- Vahvistettuja varauksia: {onvahvistettu} kpl")
    print(f"- Ei-vahvistettuja varauksia: {eivahvistettu} kpl")
    print()

def varausten_kokonaistulot(varaukset: list):
    tulot = 0
    for varaus in varaukset[1:]:
        if(varaus[8]):
            tulot += varaus[6]*varaus[7]

    print("Vahvistettujen varausten kokonaistulot:", f"{tulot:.2f}".replace('.', ','), "€")
    print()

def main():
    varaukset = hae_varaukset("varaukset.txt")
    print("1) VAHVISTETUT VARAUKSET")
    vahvistetut_varaukset(varaukset)
    print("2) PITKÄT VARAUKSET (≥ 3 h)")
    pitkat_varaukset(varaukset)
    print("3) VARAUSTEN VAHVISTUS-STATUS")
    varausten_vahvistusstatus(varaukset)
    print("4) YHTEENVETO VAHVISTUKSISTA")
    varausten_lkm(varaukset)
    print("5) VAHVISTETTUJEN VARAUSTEN KOKONAISTULOT")
    varausten_kokonaistulot(varaukset)
    
if __name__ == "__main__":
    main()

