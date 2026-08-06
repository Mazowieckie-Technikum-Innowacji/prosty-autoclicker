# Simple Autoclicker - README.md

Bardzo prosty autoclicker, napisany w Pythonie, który wykorzystuje bibliotekę pynput (Windows) i evdev (Linux).

## Uwaga!

Autoclicker **nie posiada** GUI i jest **bardzo prosty w wykryciu** przez auto-cheaty czy inne.

**Nie ponoszę żadnej** odpowiedzialności za nieudane wykorzystanie tego programu w celach cheatowania, oszukiwania innych programów, gier, ... oraz skutków tego, jakimi są bany, timeouty ani żadne inne kary!

Pełna licencja w pliku `LICENSE.md`. (Licencja MIT)

**Projekt w Celach Edukacyjnych!**

## Funkcje

- Automatyczne klikanie lewym przyciskiem myszy
- Tryb stały (steady) - równe odstępy między kliknięciami
- Tryb zlosowaniem (fluctuating) - losowe odstępy z konfigurowalnym minimum
- Obsługa Linuxa (evdev) i Windowsa (pynput)
- Konfiguracja CPS, czasu trwania, losowości
- Obsługa trybu bez limitu czasu

## Wymagania

- Python >= 3.10
- Linux: `evdev`
- Windows: `pynput`
- `numpy` (dla trybu losowego)

## Instalacja

Używając `pip`:

```bash
pip install -r requirements.txt
```

Używając `uv`:

```bash
uv pip install -r requirements.txt
```

### W niektórych systemach, np. `Arch Linux`, trzeba utworzyć `Virtualny folder`.

Używając `python`:

```bash
python -m venv venv
```

Używając `uv`:

```bash
uv venv venv
```

## Uruchamianie

```bash
python .
```

```bash
python __main__.py
```

```bash
uv run .
```

### Używając `Virtualnego Folderu`, np. w systemie `Arch Linux`:

Używając `pip i python`:
```bash
source venv/bin/activate
python .
```

Bezpośrednio:

```bash
./venv/bin/python .
```

Używając `uv`:

```bash
source venv/bin/activate
uv run .
```

## Użycie

Po uruchomieniu program poprosi o:

1. **System** - automatycznie wykrywa Linux/Windows. Jeśli nieobsługiwany, pyta o ręczny wybór.
2. **Czas trwania** - w sekundach. Domyślnie: 2. Wartość 0 = bez limitu (Ctrl+C aby zatrzymać).
3. **CPS** - kliknięcia na sekundę. Domyślnie: 1.
4. **Losowy odstęp** - czy odstęp między kliknięciami ma być losowy. Domyślnie: Tak.
5. **Minimalny odstęp** - minimalny czas między kliknięciami (dla trybu losowego). Domyślnie: 0.1s.

Przed startem program wyświetli podsumowanie ustawień i zapyta o potwierdzenie.

## Testowanie

### Testy automatyczne

```bash
pip install -e ".[test]"
pytest tests/ -v
```

### Testy manualne

Otwórz `manual_test/index.html` w przeglądarce. Dostępne testy:

- **Kliknij!** - podstawowy test kliknięcia
- **Licznik kliknięć** - przyciski +/− z pomiarem CPS
- **Tester CPS** - pomiary w przedziałach 2-60s
- **Wykres kliknięć** - wizualizacja CPS w czasie rzeczywistym

Testy manualne są dostępne online via [GitHub Pages](https://mazowieckie-technikum-innowacji.github.io/prosty-autoclicker/).

## Deweloperzy

```bash
pip install -e ".[dev]"
```

Lintowanie:
```bash
ruff check .
```

Formatowanie:
```bash
ruff format .
```

## Kod

Kod startowy znajduje się w pliku `__main__.py`.
Natomiast kod dla specyficznej platformy znajduje się w plikach w folderze `click_platform`:
- `Linux.py` dla platform typu `Linux`.
- `Windows.py` dla platform typu `Windows`.

## Licencja

MIT - patrz [LICENSE.md](LICENSE.md)

## Autor

Bartosz Zakrzewski - [Github](https://github.com/BartekDeveloper)
