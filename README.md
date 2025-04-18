# MoneyTrackApp

MoneyTrackApp antaa käyttäjille mahdollisuuden tallentaa päivittäiset kulutuksensa. Jokaisella rekisteröityneellä käyttäjällä on oma kululuettelonsa.

## Dokumentaatio
- [Vaatimusmäärittely](./dokumentaatio/vaatimusmaarittely.md)
- [Työaikakirjanpito](./dokumentaatio/tyoaikakirjanpito.md)
- [Changelog](./dokumentaatio/changelog.md)
- [Arkkitehtuuri](./dokumentaatio/arkkitehtuuri.md)

## Asennus
1. Kloonaa koneellesi ja asenna riippuvuudet komennolla
```bash
poetry install
```
2. Aktivoi virtuaaliympäristö
```bash
poetry shell
```

## Komentorivitoiminnot
Huom! Tietokanta voidaan nyt alustaa vain manuaalisesti. Alusta tietokanta ennen ohjelman käynnistämistä
```bash
poetry run python3 src/initialize_database.py
```

Ohjelman käynnistäminen

```bash
poetry run invoke start
```

Testaus

```bash
poetry run invoke test
```

Testikattavuusraportti

```bash
poetry run invoke coverage-report
```

[.pylintrc](./.pylintrc) määrittelemät tarkistukset:
```bash
poetry run invoke lint
```

[__ylimääräinen koodikatselmointi__](https://github.com/neakovalainen/ohjelmistotekniikka25/issues/1)
