# Copyright (c) 2025 Nea Järvenpää
# This code is licensed under the MIT License.

from datetime import datetime

def muunna_varaustiedot(varaus: list) -> dict:
    return {
        "varausId": int(varaus[0]),
        "nimi": varaus[1],
        "sähköposti": varaus[2],
        "puhelin": varaus[3],
        "paivamaara": datetime.strptime(varaus[4], "%Y-%m-%d").date(),
        "kellonaika": datetime.strptime(varaus[5], "%H:%M").time(),
        "kesto": int(varaus[6]),
        "hinta": float(varaus[7]),
        "vahvistettu": varaus[8].lower() == "true",
        "kohde": varaus[9],
        "luotu": datetime.strptime(varaus[10], "%Y-%m-%d %H:%M:%S")
    }

def hae_varaukset(varaustiedosto: str) -> list[dict]:
    varaukset: list[dict] = []
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for rivi in f:
            rivi = rivi.strip()
            if not rivi:
                continue
            osat = rivi.split('|')
            try:
                int(osat[0])
            except ValueError:
                continue
            varaukset.append(muunna_varaustiedot(osat))
    return varaukset

def vahvistetut_varaukset(varaukset: list[dict]):
    for varaus in varaukset:
        if varaus["vahvistettu"]:
            print(f"- {varaus['nimi']}, {varaus['kohde']}, {varaus['paivamaara'].strftime('%d.%m.%Y')} klo {varaus['kellonaika'].strftime('%H.%M')}")
    print()

def pitkat_varaukset(varaukset: list[dict]):
    for varaus in varaukset:
        if varaus["kesto"] >= 3:
            print(f"- {varaus['nimi']}, {varaus['paivamaara'].strftime('%d.%m.%Y')} klo {varaus['kellonaika'].strftime('%H.%M')}, kesto {varaus['kesto']} h, {varaus['kohde']}")
    print()

def varausten_vahvistusstatus(varaukset: list[dict]):
    for varaus in varaukset:
        if varaus["vahvistettu"]:
            print(f"{varaus['nimi']} → Vahvistettu")
        else:
            print(f"{varaus['nimi']} → EI vahvistettu")
    print()

def varausten_lkm(varaukset: list[dict]):
    vahvistetutVaraukset = 0
    eiVahvistetutVaraukset = 0
    for varaus in varaukset:
        if varaus["vahvistettu"]:
            vahvistetutVaraukset += 1
        else:
            eiVahvistetutVaraukset += 1
    print(f"- Vahvistettuja varauksia: {vahvistetutVaraukset} kpl")
    print(f"- Ei-vahvistettuja varauksia: {eiVahvistetutVaraukset} kpl")
    print()

def varausten_kokonaistulot(varaukset: list[dict]):
    varaustenTulot = 0.0
    for varaus in varaukset:
        if varaus["vahvistettu"]:
            varaustenTulot += varaus["kesto"] * varaus["hinta"]
    print("Vahvistettujen varausten kokonaistulot:", f"{varaustenTulot:.2f}".replace('.', ','), "€")
    print()

def main():
    varaukset = hae_varaukset("varaukset.txt")
    print("1) Vahvistetut varaukset")
    vahvistetut_varaukset(varaukset)
    print("2) Pitkät varaukset (≥ 3 h)")
    pitkat_varaukset(varaukset)
    print("3) Varausten vahvistusstatus")
    varausten_vahvistusstatus(varaukset)
    print("4) Yhteenveto vahvistuksista")
    varausten_lkm(varaukset)
    print("5) Vahvistettujen varausten kokonaistulot")
    varausten_kokonaistulot(varaukset)

if __name__ == "__main__":
    main()
