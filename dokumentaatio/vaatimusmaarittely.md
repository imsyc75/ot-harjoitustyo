# Vaatimusmäärittely

## Sovelluksen tarkoitus
MoneyTrackApp antaa käyttäjille mahdollisuuden tallentaa päivittäiset kulutuksensa. Jokaisella rekisteröityneellä käyttäjällä on oma kululuettelonsa.

## Käyttäjät
Aluksi sovelluksessa on vain tavallisia käyttäjiä, ja myöhemmin voidaan lisätä toisen käyttäjätyypin, kuten ylläpitäjän.

## Perusversion tarjoama toiminnallisuus

### Ennen kirjautumista
- Käyttäjä voi rekisteröityä.
    - Käyttäjätunnuksen täytyy olla unikki.
    - Salasanan täytyy sisältää välimerkkejä ja pituuddeltaan vähintään 8 merkkiä. 
- Käyttä voi kirjautua sovellukseen.
    - Kirjautuminen onnistuu, kun käyttäjätunnus ja salasana on syötetty oikein.
    - Jos käyttäjätunnus ei ole olemassa tai salasana ei täsmää, näytetään virheviesti.
    
### Kirjautumisen jälkeen
- Käyttäjä voi luoda uusi meno.
    - päivämäärä/kategoria/summa/kuvaus
    - Kolme ensimmäistä kohdetta ovat tyhjiä tai päivämäärä on väärä, sitä ei voi luoda.
- Käyttäjä voi tarkastella olemassa olevia menoja.
- Käyttäjä voi muokkaa ja poista menoja.

## Jatkokehitysideoita
- Käyttäjä voi luoda uusi tulo.
- Käyttäjä voi luoda yhteenveto kuluista ja tuloista aikajaksoittain (päivä/viikko/kuukausi)
- Käyttäjä voi tarkastella kuluja kategorian ja päivämäärän mukaan
- Käyttäjä voi luoda piirakkakaavio kuluista

## Käyttöliittymäluonnos
Sovellus avautuu kirjautumissivuun. Kirjautumissivulla voidaan siirtyä uuden käyttäjän luontisivuun. Onnistuneen kirjautumisen jälkeen siirtyy kirjautuneen käyttäjän henkilökohtaiseen sivuun.

## Toimintaympäristön rajoitteet
- Sovelluksen tulee toimia Linux- ja OSX-käyttöjärjestelmillä varustetuissa koneissa.
- Kaikki tiedot talletetaan paikallisen koneen levylle.