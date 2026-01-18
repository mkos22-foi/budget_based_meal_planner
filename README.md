# Budget-Based Meal Planner
> Aplikacija za planiranje obroka pomoću programiranja s ograničenjima. Korisnik unosi budžet, kalorije i cilj prehrane, a sustav generira optimalan obrok

## Struktura projekta
```
├── UI.py                 # Korisničko sučelje aplikacije
├── hrana.py              # Rječnik sa svim namirnicama
├── main.py               # Logika generiranja obroka
├── requirements.txt      # Python ovisnosti
└── README.md             # Upute za pokretanje projekta
```

## Pokretanje projekta

### 1. Preuzimanje repozitorija i kreiranje virtualnog okružanja
Preuzmite repozitorij te kreirajte virtualno okruženje:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalacija potrebnih paketa
```bash
pip install -r requirements.txt
```

### 3. Pokretanje aplikacije
Aplikacija se pokreće naredbom `python3 UI.py`
