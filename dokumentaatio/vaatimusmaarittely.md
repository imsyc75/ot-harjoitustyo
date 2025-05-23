# Vaatimusmäärittely

## Sovelluksen tarkoitus
MoneyTrackApp antaa käyttäjille mahdollisuuden tallentaa päivittäiset kulutuksensa. Jokaisella rekisteröityneellä käyttäjällä on oma kululuettelonsa.

## Käyttäjät
Aluksi sovelluksessa on vain tavallisia käyttäjiä, ja myöhemmin voidaan lisätä toisen käyttäjätyypin, kuten ylläpitäjän.

## Perusversion tarjoama toiminnallisuus

### Ennen kirjautumista
- Käyttäjä voi rekisteröityä.(tehty)
    - Käyttäjätunnuksen täytyy olla unikki.
- Käyttä voi kirjautua sovellukseen.(tehty)
    - Kirjautuminen onnistuu, kun käyttäjätunnus ja salasana on syötetty oikein.
    - Jos käyttäjätunnus ei ole olemassa tai salasana ei täsmää, näytetään virheviesti.
    
### Kirjautumisen jälkeen
- Käyttäjä voi luoda uusi meno.(tehty)
    - päivämäärä/kategoria/summa/kuvaus
    - Kolme ensimmäistä kohdetta ovat tyhjiä tai päivämäärä on väärä, sitä ei voi luoda.
- Käyttäjä voi tarkastella olemassa olevia menoja.(tehty)
- Käyttäjä voi muokkaa ja poista menoja.(tehty)

## Jatkokehitysideoita
- Käyttäjä voi nähdä summa kuluista kuukausittain.(tehty)
- Käyttäjä voi suodattaa kuluja päivämäärän mukaan.(tehty)
- Käyttäjä voi luoda piirakkakaavio kuluista.(tehty)
- Käyttäjä voi luoda CSV tiedosto kuluista. (tehty)

## Käyttöliittymäluonnos
Sovellus avautuu kirjautumissivuun. Kirjautumissivulla voidaan siirtyä uuden käyttäjän luontisivuun. Onnistuneen kirjautumisen jälkeen siirtyy kirjautuneen käyttäjän henkilökohtaiseen sivuun.

## Toimintaympäristön rajoitteet
- Sovelluksen tulee toimia Linux- ja OSX-käyttöjärjestelmillä varustetuissa koneissa.
- Kaikki tiedot talletetaan paikallisen koneen levylle.