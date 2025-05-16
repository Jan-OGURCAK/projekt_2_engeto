"""
projekt_2.py: druhý projekt do Engeto Online Python Akademie

author: Ján OGURČÁK
email: jan.ogurcak@seznam.cz

"""


def hlavicka():
    """
    Fukce je prostým výpisem hlavičky programu
    """
    
    print("Hi there!")
    print("-" * 48)
    print(f"I've generated a random {glob['delka_cisla']} digit number for you.")
    print("Let's play a bulls and cows game.")
    print("-" * 48)
    if glob["test_mode"]:
        print("#" * 48)
        print('This is a test mode (glob["test_mode"] = True)')
        print(f"Searched number is {glob['hadane_cislo']}")
        print("#" * 48)

        print("Enter a number:")

    return


def dej_hadane_cislo():
    """
    Funkce generuje nahodný n -  místný int a zapíše ho jako sled
    cislic do stringu 'glob["hadane_cislo]"'

    Parameters:
    :glob["hadane_cislo"]: -> str
    """
    from random import randint

    sada_cisel = list(range(0, 10))  # Vygeneruje sadu čísel pro generování
    glob["hadane_cislo"] = ""

    cislo = sada_cisel[randint(1, 9)]  # První číslice nesmí být '0' -> jiný .randint
    glob["hadane_cislo"] += str(cislo)
    sada_cisel.remove(cislo)

    for _ in range(0, glob["delka_cisla"] - 1):  # Tady už vybíráme z toho co zbylo
        cislo = sada_cisel[randint(0, len(sada_cisel) - 1)]
        glob["hadane_cislo"] += str(cislo)
        sada_cisel.remove(cislo)

    return


def opakovani_cislic(vstup: str) -> bool:
    """
    Funkce přebírá jako parametr n - místný str: a kontroluje
    jestli se jednotlivé číslice neopakují

    Parameters:
    :vstup: -> str n - místné číslo

    :navrat: -> bool True když jsou minimálně dvě číslice stejné

    """
    navrat = False
    pom_set = set()

    for znak in vstup:  # Nakrmí set
        pom_set.add(znak)

    # Když set: našel duplicitu -> změna délky stringu
    navrat = False if (len(pom_set) == glob["delka_cisla"]) else True

    return navrat


def nacti_cislo() -> bool:
    """
    Funkce načte n - místne číslo jako str:, zkontroluje jeho formát
    dle pravidel hry a výsledek zapíše do str: 'glob["nactene_cislo"]'

    Parameters:
    :cislo_OK: bool navratovy parametr - načtení čísla OK
    """
    
    print("-" * 48)
    print(">>>", end=" ")

    vstup = input()

    cislo_OK = True

    err_text = ""

    if not vstup.isnumeric():
        err_text = f"{vstup} is not a numeric value!"
        cislo_OK = False

    if cislo_OK and (len(vstup) != glob["delka_cisla"]):
        err_text = f"{vstup} does not have a correct length"
        cislo_OK = False

    if cislo_OK and (vstup[0] == "0"):
        err_text = f"The number ({vstup}) must not start with zero!"
        cislo_OK = False

    if cislo_OK and opakovani_cislic(vstup):
        err_text = f"({vstup}) - digits must not be repeated!"
        cislo_OK = False

    if not cislo_OK:  # V zadaném stringu je chyba -> hlášení a pryč
        print(err_text)
        print(f"{glob['delka_cisla']} digit number is expected.")
        print("  - The number must not start with zero!")
        print("  - digits must not be repeated!")
    else:  # Zadané číslo je OK
        glob["nactene_cislo"] = vstup

    return cislo_OK


def vyhodnot():
    """
    Funkce porovná vygenerované číslo s načteným číslem

    Parameters:
    :glob["hadane_cislo"]: str číslo generované programem

    :glob["nactene_cislo"]: str číslo zadané uživatelem

    :glob["bulls"]: int výsledky pro Bulls

    :glob["cows"]: int výsledky pro Cows

    """
    for hadane, nactene in zip(glob["hadane_cislo"], glob["nactene_cislo"]):
        if nactene == hadane:  # Zhodná čísla na zhodné pozici --> Bull
            glob["bulls"] += 1

        elif nactene in glob["hadane_cislo"]:  # Zhodná čísla na rozdílné pozici --> Cow
            glob["cows"] += 1

    suffix_bulls = "bull" if (glob["bulls"] == 1) else "bulls"
    suffix_cows = "cow" if (glob["cows"] == 1) else "cows"

    print(f"{glob['bulls']} {suffix_bulls}, {glob['cows']} {suffix_cows}")

    return


def vypis_zapati():  # Prostý výpis zápatí programu del zadání
    """
    Funkce vypíše zápatí programu
    """
    
    print("-" * 48)
    print("Correct, you've guessed the right number")

    print(f"in {glob['pokusu']} guesses!", "\n")
    print(f"Game time is {glob['total_time_hra']} seconds")
    print("-" * 48)
    print("That's amazing!", "\n")

    return


def dej_vetu_historie() -> dict:
    """
    Funkce vygeneruje vetu pro zapis historie

    Parameters:
    :navrat: dict vlastna veta
    """
    # Výpočet času kola
    cas = (time.time() - glob["start_time_pokus"])
    cas = round(cas, 1)

    navrat = {
        "hled_cislo": glob["nactene_cislo"],
        "bulls": glob["bulls"],
        "cows": glob["cows"],
        "cas_kola": cas,
    }

    return navrat


def zapis_radek_historie(cislo_kola: int):  # Zápis parametrů kola do dict()
    """
    Funkce zapíše vetu se statistikou kola do historie

    Parameters:
    :cislo_kola: int poradove cislo kola
    """

    glob["historie"][cislo_kola] = dej_vetu_historie()

    return


def vypis_historie():  # Výpis historie jednotlivých kol hry
    """
    Prosty vypis historie hry
    """

    print("\n")
    print("GAME HISTORY".center(48, " "))
    print("============".center(48, " "))
    print("\n")

    print("Round No   Number    Bulls   Cows    Time")

    print("-" * 48)

    for key, polozka in glob["historie"].items():  # Prevod položek dict() na str a formátování
        veta = (
            str(key).rjust(4, " ")
            + str(polozka["hled_cislo"]).rjust(12, " ")
            + str(polozka["bulls"]).rjust(8, " ")
            + str(polozka["cows"]).rjust(8, " ")
            + str(polozka["cas_kola"]).rjust(8, " ")
            + " s"
            )

        print(veta)

    print("-" * 48)
    print("Total game time:" + glob["total_time_hra"].rjust(24, " ") + " s")


# =========================================================
# =================== Vlastni program =====================
# =========================================================

import time

# Soubor globálních proměnných
glob = {
    "hadane_cislo": "",
    "nactene_cislo": "",
    "delka_cisla": 4,
    "test_mode": True,
    "bulls": 0,
    "cows": 0,
    "pokusu": 0,
    "start_time_hra": None,
    "start_time_pokus": None,
    "end_time_hra": None,
    "total_time_hra": None,
    "historie": dict(),
}

if (__name__ == "__main__"):

    dej_hadane_cislo()  # Vygeneruje n - místný int: (dle nastavení glob["delka_cisla"])

    hlavicka()  # Vypíše hlavičku programu se stručnými pravidly.

    glob["start_time_hra"] = time.time()  # Uložení času začátku hry

    while (glob["bulls"] != glob["delka_cisla"]):  # Hlavní smyčka programu. Program skončí když jsou všechna čísla "bull"
        glob["start_time_pokus"] = time.time()  # Uložení času začátku kola

        while (not nacti_cislo()):  # Smyčka kola hry. Opakuje se dokud nedostane číslo dle pravidel
            pass

        glob["bulls"] = 0
        glob["cows"] = 0

        vyhodnot()  # Vyhodnoti kolo hry a nastavi promenne glob["bulls"] promenne glob["bulls"]
        glob["pokusu"] += 1 # Inc cisla kola

        zapis_radek_historie(glob["pokusu"])  # Zapise vysledek kola pro pozdejsi vypis

    trvani = (time.time() - glob["start_time_hra"])  # Hra končí, vypočtem jeji delku..
    glob["total_time_hra"] = str(round(trvani, 1))  # zaokrouhlíme na 1 desetinné misto a zapíšem

    vypis_zapati()  # Vypis standartního zápatí dle zadání

    vypis_historie()  # Výpis historie jednotlivých kol
