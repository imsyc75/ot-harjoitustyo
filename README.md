# MoneyTrackApp

MoneyTrackApp antaa käyttäjille mahdollisuuden tallentaa päivittäiset kulutuksensa. Jokaisella rekisteröityneellä käyttäjällä on oma kululuettelonsa.

[__ylimääräinen koodikatselmointi__](https://github.com/neakovalainen/ohjelmistotekniikka25/issues/1)

## Dokumentaatio
- [Vaatimusmäärittely](./dokumentaatio/vaatimusmaarittely.md)
- [Työaikakirjanpito](./dokumentaatio/tyoaikakirjanpito.md)
- [Changelog](./dokumentaatio/changelog.md)
- [Arkkitehtuuri](./dokumentaatio/arkkitehtuuri.md)
- [Käyttöohje](./dokumentaatio/kayttoohje.md)
- [Testaus](./dokumentaatio/Testaus.md)

## Releaset
[Viikon 5 release](https://github.com/imsyc75/ot-harjoitustyo/releases/tag/viikko5)  
[Viikon 6 release](https://github.com/imsyc75/ot-harjoitustyo/releases/tag/viikko6)  
[Final release](https://github.com/imsyc75/ot-harjoitustyo/releases/tag/viikko7)

## Asennus
Lataa projektin [Final release](https://github.com/imsyc75/ot-harjoitustyo/releases/tag/viikko7) lähdekoodi.

1. Asenna riippuvuudet komennolla
```bash
poetry install
```
2. Alusta tietokanta ennen ohjelman käynnistämistä
```bash
poetry run invoke build
```
3. Käynnistä ohjelman
```bash
poetry run invoke start
```

## Komentorivitoiminnot
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

