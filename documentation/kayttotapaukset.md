# User Stories

### Rekisteröimätön käyttäjä:

Rekisteröimättömänä asiakkaana haluan..

- listata ja lukea kaikki sanonnat listaten myös lapsen nimen ja sanontaiän

    SELECT Quote.id, Quote.quote, Child.name AS n, Quote.agesaid FROM Quote JOIN Child ON Child.id = Quote.child_id GROUP BY Quote.id, Child.name

- hakea sanontoja eri kategorioiden mukaan

    SELECT Quote.id, Quote.quote, Child.name AS n, Quote.agesaid FROM Quote
    JOIN Child ON Child.id = Quote.child_id
    JOIN quotecategory ON quotecategory.quote_id = Quote.id
    WHERE quotecategory.category_id=?
    GROUP BY Quote.id, Child.name

- hakea top 10 (eniten tykätyt) listan ja lukea sen sanonnat

    SELECT quote.id, quote.quote, COUNT(likes.id) AS num FROM likes, quote
    WHERE quote.id=likes.quote_id AND like_count=1 
    GROUP BY like_count, quote.id, quote.quote
    ORDER BY num DESC
    LIMIT 10

- voida rekisteröityä ja kirjautua sen jälkeen


### Kirjautunut käyttäjä:

Rekisteröityneenä ja kirjautuneena käyttäjänä haluan...

- voida lisätä lapsia tietokantaan
- voida listata omien lapseni omat sanonnat

    SELECT Quote.id, Quote.quote, Quote.agesaid FROM Quote
    WHERE Child_id=?
    ORDER BY Quote.id

- voida lisätä lapsen kohdalle sanontoja
- voida muokata lapsensa sanontaa
- voida poistaa lapsensa sanonnan
- voida tykätä kustakin sanonnasta yhden kerran
- pystyä listaamaan lapseni

    SELECT Child.id, Child.name, Child.birthday FROM Child
    WHERE Account_id=?
    ORDER BY Child.id


- pystyä näkemään tarkemmat tiedot lapsestani
- pystyä muokkaamaan lapseni tietoja
- pystyä poistamaan lisäämäni lapsen
 

### Ylläpitäjä

Ylläpitäjänä haluan...

- voida lisätä ja poistaa kategorioita
- voida poistaa (sopimattomia) sanontoja
- voida poistaa rekisteröityneen käyttäjän
- voida nähdä kaikkien käyttäjien listauksen ja heidän tarkemmat tietonsa sekä lapsimääränsä

    SELECT Account.id, Account.username, COUNT(Child.id) AS total FROM Account
    LEFT JOIN Child ON Child.account_id = Account.id
    GROUP BY Account.id

