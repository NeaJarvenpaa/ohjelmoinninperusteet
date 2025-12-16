# Copyright (c) 2025 Nea Järvenpää
# This code is licensed under the MIT License.

from datetime import datetime, date, time
from typing import List

class Varaus:
    def __init__(
        self,
        varaus_id: int,
        nimi: str,
        sahkoposti: str,
        puhelin: str,
        varauksen_pvm: date,
        varauksen_klo: time,
        varauksen_kesto: int,
        hinta: float,
        varaus_vahvistettu: bool,
        varattu_tila: str,
        varaus_luotu: datetime
    ):
        self.varaus_id = varaus_id
        self.nimi = nimi
        self.sahkoposti = sahkoposti
        self.puhelin = puhelin
        self.varauksen_pvm = varauksen_pvm
        self.varauksen_klo = varauksen_klo
        self.varauksen_kesto = varauksen_kesto
        self.hinta = hinta
        self.varaus_vahvistettu = varaus_vahvistettu
        self.varattu_tila = varattu_tila
        self.varaus_luotu = varaus_luotu

    def is_confirmed(self) -> bool:
        return self.varaus_vahvistettu

    def is_long(self, raja_tunteina: int = 3) -> bool:
        return self.varauksen_kesto >= raja_tunteina

    def total_price(self) -> float:
        return self.varauksen_kesto * self.hinta

def muunna_varaustiedot(varaus: list[str]) -> Varaus:
    return Varaus(
        varaus_id=int(varaus[0]),
        nimi=varaus[1],
        sahkoposti=varaus[2],
        puhelin=varaus[3],
        varauksen_pvm=datetime.strptime(varaus[4], "%Y-%m-%d").date(),
        varauksen_klo=datetime.strptime(varaus[5], "%H:%M").time(),
        varauksen_kesto=int(varaus[6]),
        hinta=float(varaus[7]),
        varaus_vahvistettu=(varaus[8].lower() == "true"),
        varattu_tila=varaus[9],
        varaus_luotu=datetime.strptime(varaus[10], "%Y-%m-%d %H:%M:%S"),
    )

def hae_varaukset(varaustiedosto: str) -> List[Varaus]:
    varaukset: List[Varaus] = []
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

def vahvistetut_varaukset(varaukset: List[Varaus]):
    for v in varaukset:
        if v.is_confirmed():
            print(f"- {v.nimi}, {v.varattu_tila}, {v.varauksen_pvm.strftime('%d.%m.%Y')} klo {v.varauksen_klo.strftime('%H.%M')}")
    print()

def pitkat_varaukset(varaukset: List[Varaus]):
    for v in varaukset:
        if v.is_long(3):
            print(f"- {v.nimi}, {v.varauksen_pvm.strftime('%d.%m.%Y')} klo {v.varauksen_klo.strftime('%H.%M')}, kesto {v.varauksen_kesto} h, {v.varattu_tila}")
    print()

def varausten_vahvistusstatus(varaukset: List[Varaus]):
    for v in varaukset:
        print(f"{v.nimi} → {'Vahvistettu' if v.is_confirmed() else 'EI vahvistettu'}")
    print()

def varausten_lkm(varaukset: List[Varaus]):
    vahvistetutVaraukset = sum(1 for v in varaukset if v.is_confirmed())
    eiVahvistetutVaraukset = len(varaukset) - vahvistetutVaraukset
    print(f"- Vahvistettuja varauksia: {vahvistetutVaraukset} kpl")
    print(f"- Ei-vahvistettuja varauksia: {eiVahvistetutVaraukset} kpl")
    print()

def varausten_kokonaistulot(varaukset: List[Varaus]):
    varaustenTulot = sum(v.total_price() for v in varaukset if v.is_confirmed())
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