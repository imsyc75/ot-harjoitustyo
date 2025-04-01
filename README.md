# MoneyTrackApp

MoneyTrackApp antaa käyttäjille mahdollisuuden tallentaa päivittäiset kulutuksensa. Jokaisella rekisteröityneellä käyttäjällä on oma kululuettelonsa.

## Dokumentaatio
- [Vaatimusmäärittely](./dokumentaatio/vaatimusmaarittely.md)
- [Työaikakirjanpito](./dokumentaatio/tyoaikakirjanpito.md)
- [Changelog](./dokumentaatio/changelog.md)

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

Ohjelman suorittaminen

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