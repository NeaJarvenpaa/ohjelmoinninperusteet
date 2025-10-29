#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path


def lue_argumentit() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Lue tiedostosta yksi sana ja tulosta se."
    )
    parser.add_argument(
        "-t",
        "--tiedosto",
        type=Path,
        default=Path("sana.txt"),
        help="Tiedoston polku (oletus: sana.txt)",
    )
    return parser.parse_args()


def lue_yksi_sana(polku: Path) -> str:
    if not polku.exists():
        raise FileNotFoundError(f"Tiedostoa ei löydy: {polku}")

    teksti = polku.read_text(encoding="utf-8").strip()
    kaava = re.compile(r"^[\w-]+$", flags=re.UNICODE)

    if not teksti or not kaava.match(teksti):
        raise ValueError(
            "Tiedoston tulee sisältää vain yksi sana ilman välilyöntejä tai erikoismerkkejä."
        )

    return teksti


def main() -> int:

    args = lue_argumentit()
    try:
        sana = lue_yksi_sana(args.tiedosto)
    except FileNotFoundError as e:
        print(f"Virhe: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Virhe: {e}", file=sys.stderr)
        return 2

    print(sana)
    return 0


if __name__ == "__main__":
    sys.exit(main())