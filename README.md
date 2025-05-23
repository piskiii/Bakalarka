# Bakalárska Práca: Interaktívny Nástroj pre Statickú Analýzu 2D Konštrukcií

Vitajte v repozitári mojej bakalárskej práce! Táto aplikácia bola vyvinutá ako nástroj pre študentov na jednoduché grafické modelovanie 2D konštrukcií, zadávanie zaťažení a podpier, s následným výpočtom a vizualizáciou vnútorných síl.

Cieľom bolo vytvoriť intuitívne prostredie, ktoré zjednodušuje proces statickej analýzy a pomáha lepšie pochopiť správanie sa konštrukcií pod zaťažením.

## Stiahnutie a Spustenie Aplikácie (`.exe`)

Najjednoduchší spôsob, ako spustiť aplikáciu, je stiahnuť si predkompilovaný `.exe` súbor pre Windows:

1.  Prejdite do sekcie **[Releases](https://github.com/piskiii/Bakalarka/releases)** tohto repozitára.
2.  Stiahnite si najnovší `VVU.exe` súbor (alebo `.zip` archív obsahujúci `.exe`) z posledného vydania.
3.  Spustite `VVU.exe`. Inštalácia nie je potrebná.

**Upozornenie:** Keďže aplikácia nie je digitálne podpísaná, váš operačný systém Windows (Windows Defender SmartScreen) alebo antivírusový program môže pri prvom spustení zobraziť varovanie. Toto je štandardné správanie pre aplikácie od neznámych vydavateľov. Súbor je bezpečný. Ak sa zobrazí varovanie, možno budete musieť kliknúť na "Ďalšie informácie" a potom "Spustiť aj tak".

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
