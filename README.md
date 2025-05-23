# Bakalárska Práca: Interaktívny Nástroj pre Statickú Analýzu 2D Konštrukcií

Vitajte v repozitári mojej bakalárskej práce! Táto aplikácia bola vyvinutá ako nástroj pre študentov na jednoduché grafické modelovanie 2D konštrukcií, zadávanie zaťažení a podpier, s následným výpočtom a vizualizáciou vnútorných síl.

Cieľom bolo vytvoriť intuitívne prostredie, ktoré zjednodušuje proces statickej analýzy a pomáha lepšie pochopiť správanie sa konštrukcií pod zaťažením.

## Kľúčové Funkcie

* **Grafické Modelovanie:** Jednoduché kreslenie nosníkov (priamych aj oblúkových) a ich spájanie priamo na plátne.
* **Presné Kótovanie:** Automatické zobrazenie rozmerov nakreslených prvkov.
* **Flexibilné Úpravy:** Možnosť dynamicky meniť rozmery už existujúcich častí konštrukcie.
* **Definícia Podpier:** Široká škála typov podpier (pevná, posuvná, kĺbová) s nastaviteľnou orientáciou.
* **Zadávanie Zaťažení:** Aplikácia bodových síl, spojitých (lineárnych) zaťažení a ohybových momentov na zvolené prvky.
* **Statická Analýza:** Automatizovaný výpočet reakcií v podporách a priebehov vnútorných síl (normálová sila N, posúvajúca sila T, ohybový moment M).
* **Vizuálne Výstupy:** Prehľadné zobrazenie diagramov N, T, M pomocou knižnice Matplotlib, integrované priamo v aplikácii.
* **Správa Projektu:** Možnosť ukladania rozpracovaných konštrukcií do JSON súborov a ich následné načítanie.
* **Používateľský Komfort:** Funkcie ako Späť/Znova (Undo/Redo) pre kresliace operácie a jednoduché mazanie prvkov.
* **Moderné GUI:** Používateľské rozhranie postavené na knižnici CustomTkinter pre atraktívny a responzívny dizajn.

## Stiahnutie a Spustenie Aplikácie (`.exe`)

Najjednoduchší spôsob, ako spustiť aplikáciu, je stiahnuť si predkompilovaný `.exe` súbor pre Windows:

1.  Prejdite do sekcie **[Releases](https://github.com/piskiii/Bakalarka/releases)** tohto repozitára.
2.  Stiahnite si najnovší `VVU.exe` súbor (alebo `.zip` archív obsahujúci `.exe`) z posledného vydania.
3.  Spustite `VVU.exe`. Inštalácia nie je potrebná.

## Spustenie zo Zdrojového Kódu (pre Vývojárov)

Ak si chcete aplikáciu spustiť priamo zo zdrojového kódu alebo do nej nahliadnuť:

1.  **Nainštalujte Python:**
2.  **Klonujte repozitár:**
    ```bash
    git clone [https://github.com/piskiii/Bakalarka.git](https://github.com/piskiii/Bakalarka.git)
    cd Bakalarka
    ```
3.  **(Odporúčané) Vytvorte a aktivujte virtuálne prostredie:**
    ```bash
    python -m venv .venv
    # Na Windows:
    .\.venv\Scripts\activate
    # Na macOS/Linux:
    # source .venv/bin/activate
    ```
4.  **Nainštalujte požadované knižnice:** Všetky závislosti sú uvedené v `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```
5.  **Spustite aplikáciu:**
    ```bash
    python main.py
    ```

## Použité Technológie

* **Jazyk:** Python
* **GUI:** Tkinter, CustomTkinter
* **Obrázky:** Pillow (PIL)
* **Numerické výpočty:** NumPy
* **Grafy:** Matplotlib
* **Dátový formát:** JSON

## Možnosť Vlastného Buildu `.exe`

Ak si chcete vytvoriť vlastný `.exe` súbor:
1.  Postupujte podľa krokov 1-4 v sekcii "Spustenie zo Zdrojového Kódu".
2.  Nainštalujte PyInstaller: `pip install pyinstaller`
3.  Použite priložený `main.spec` súbor pre konzistentný build:
    ```bash
    pyinstaller main.spec
    ```
    Alebo zadajte plný príkaz:
    ```bash
    pyinstaller --windowed --onefile --icon="logo.png" --add-data "image:image" main.py
    ```
    Výsledný `.exe` nájdete v priečinku `dist/`.

## Autor

* **Michal Palkovič** - ([piskiii](https://github.com/piskiii))
