# Testausdokumentti

Ohjelma on testattu automaattisilla yksikkö- ja integrointitesteillä unittestin avulla sekä manuaalisesti suoritetuilla järjestelmätason testeillä.

## Yksikkö- ja integraatiotestaus

### Sovelluslogiikka

Sovelluslogiikasta vastaava ExpenseService-luokka testataan [TestExpenseService](/src/tests/test_services/test_expense_service.py)-testiluokan avulla, samoin kuin UserService-luokka [TestUserService](/src/tests/test_services/test_user_service.py)-testiluokan avulla. Testeissä ExpenseService- ja UserService-objektit alustetaan ja riippuvaiset Repository-objektit injektoidaan riippuvuuksina. Joissakin testeissä käytetään erityisiä Repository-aliluokkia, kuten FailingCreateExpenseRepository, NonexistentExpenseRepository ja FailingUpdateExpenseRepository, poikkeusten testaamiseen.

### Repository-luokat

Repository-luokkia ExpenseRepository ja UserRepository testataan käyttäen niille testissä osoitettuja tietovarastoja.ExpenseRepository-luokka testataan [TestExpenseRepository](/src/tests/test_repositories/test_expense_repository.py)-testiluokan avulla ja UserRepository-luokka testataan [TestUserRepository](/src/tests/test_repositories/test_user_repository.py)-testiluokan avulla.

### Testauskattavuus

Käyttöliittymäkerrosta lukuunottamatta sovelluksen testauksen haarautumakattavuus on 90%

![](/dokumentaatio/pics/testaus_testikattavuus.png)

Testaamattomat osat koostuvat lähinnä joistakin virheenkäsittelypoluista ja ääritapauksista.
Rakentamiseen ja konfigurointiin liittyvien tiedostojen (kuten _build.py_- ja _config.py_-) kattavuus on suhteellisen alhainen.

## Järjestelmätestaus

Sovelluksen järjestelmätestaus on suoritettu manuaalisesti. Sovellus on haettu ja sitä on testattu [käyttöohjeen](./kayttoohje.md) kuvaamalla tavalla sekä macOS- että Linux-ympäristöön. Kaikki [Vaatimusmäärittelydokumentin](/dokumentaatio/vaatimusmaarittely.md) listaamat toiminnallisuudet on käyty läpi. Kunkin ominaisuuden testauksessa yritettiin myös täyttää syöttökentät virheellisillä arvoilla (esim. tyhjillä arvoilla).
