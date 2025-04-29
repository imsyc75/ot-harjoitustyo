# MoneyTrackApp

MoneyTrackApp antaa käyttäjille mahdollisuuden tallentaa päivittäiset kulutuksensa. Jokaisella rekisteröityneellä käyttäjällä on oma kululuettelonsa.

[__ylimääräinen koodikatselmointi__](https://github.com/neakovalainen/ohjelmistotekniikka25/issues/1)

## Dokumentaatio
- [Vaatimusmäärittely](./dokumentaatio/vaatimusmaarittely.md)
- [Työaikakirjanpito](./dokumentaatio/tyoaikakirjanpito.md)
- [Changelog](./dokumentaatio/changelog.md)
- [Arkkitehtuuri](./dokumentaatio/arkkitehtuuri.md)

## Releaset
[Viikon 5 release](https://github.com/imsyc75/ot-harjoitustyo/releases/tag/viikko5)
[Viikon 6 release](https://github.com/imsyc75/ot-harjoitustyo/releases/tag/viikko6)

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

