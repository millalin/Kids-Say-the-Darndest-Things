# User Stories sekä keskeiset SQL-lauseet

### Rekisteröimätön käyttäjä:

Rekisteröimättömänä asiakkaana haluan..

- listata ja lukea kaikki sanonnat listaten myös lapsen nimen ja sanontaiän

        SELECT Quote.id, Quote.quote, Child.name AS n, Quote.agesaid FROM Quote 
        JOIN Child ON Child.id = Quote.child_id GROUP BY Quote.id, Child.name

- hakea sanontoja eri kategorioiden mukaan 

        SELECT Quote.id, Quote.quote, Child.name AS n, Quote.agesaid FROM Quote
        JOIN Child ON Child.id = Quote.child_id
        JOIN quotecategory ON quotecategory.quote_id = Quote.id
        WHERE quotecategory.category_id=?
        ODER BY Quote.id

    Ja nähdä yhteenvedon monta sanontaa kategoriassa on monelta eri lapselta

        SELECT COUNT(Quote.id) AS total, COUNT (DISTINCT Child.id) AS childcount FROM Quote
        JOIN Child ON Child.id = Quote.child_id
        JOIN quotecategory ON quotecategory.quote_id = Quote.id
        WHERE quotecategory.category_id = ?

- hakea sanontoja iän mukaan

        SELECT Quote.id, Quote.quote, Child.name AS n, Quote.agesaid FROM Quote
        JOIN Child ON Child.id = Quote.child_id
        WHERE quote.agesaid=?
        ORDER BY Quote.id

     Ja nähdä yhteenvedon monta sanontaa tällä iällä on ja monelta eri lapselta

        SELECT COUNT(Quote.id) AS total, COUNT (DISTINCT Child.id) AS childcount FROM Quote
        JOIN Child ON Child.id = Quote.child_id
        WHERE quote.agesaid = ?

- hakea top 10 (eniten tykätyt) listan ja lukea sen sanonnat

        SELECT quote.id, quote.quote, COUNT(likes.id) AS num FROM likes, quote
        WHERE quote.id=likes.quote_id AND like_count=1 
        GROUP BY like_count, quote.id, quote.quote
        ORDER BY num DESC
        LIMIT 10

- voida rekisteröityä 

        INSERT INTO account (date_created, date_modified, name, username, password, role) 
        VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?, ?)

- ja rekisteröitymisen jälkeen kirjautua 

        SELECT account.id, account.date_created, account.date_modified, 
        account.name, account.username, account.password, account.role 
        FROM account 
        WHERE account.username = ?
       

### Kirjautunut käyttäjä:

Rekisteröityneenä ja kirjautuneena käyttäjänä haluan...

- voida lisätä lapsia tietokantaan

        INSERT INTO child (date_created, date_modified, name, birthday, account_id) 
        VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?)

- voida listata omien lapseni omat sanonnat

         SELECT Quote.id, Quote.quote, Quote.agesaid FROM Quote
         WHERE Child_id=?
         ORDER BY Quote.id

- voida lisätä lapselle sanontoja

        INSERT INTO quote (date_created, date_modified, quote, agesaid, child_id) 
        VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?)

        INSERT INTO quotecategory (quote_id, category_id) VALUES (?, ?)

- voida muokata lapsensa sanontaa

        DELETE FROM quotecategory WHERE quotecategory.quote_id = ? 
        AND quotecategory.category_id = ?

        UPDATE quote SET date_modified=CURRENT_TIMESTAMP, quote=?, agesaid=? 
        WHERE quote.id = ?

        INSERT INTO quotecategory (quote_id, category_id) VALUES (?, ?)        

- tarkastella sanonnan tietoja tarkemmin

        SELECT quote.id, quote.date_created, quote.date_modified, 
        quote.quote, quote.agesaid, quote.child_id  
        FROM quote 
        WHERE quote.id = ?

        Sanonnan kategoriat:

        SELECT category.id, category.date_created, category.date_modified, category.name
        FROM (SELECT quote.id 
        FROM quote 
        WHERE quote.id = ?)  JOIN quotecategory ON quote_id = quotecategory.quote_id 
        JOIN category ON category.id = quotecategory.category_id ORDER BY .quote_id
	
- voida poistaa lapsensa sanonnan

        DELETE FROM quotecategory WHERE quotecategory.quote_id = ? 
        AND quotecategory.category_id = ?

        DELETE FROM likes WHERE likes.id = ?

        DELETE FROM quote WHERE quote.id = ?

- voida tykätä kustakin sanonnasta yhden kerran tai poistaa tykkäyksen

        DELETE FROM likes WHERE likes.quote_id = ? AND likes.account_id = ?

        INSERT INTO likes (date_created, date_modified, account_id, quote_id, like_count) 
        VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?)

- pystyä listaamaan lapseni

         SELECT Child.id, Child.name, Child.birthday FROM Child
         WHERE Account_id=?
         ORDER BY Child.id


- pystyä näkemään tarkemmat tiedot lapsestani

        SELECT child.id, child.date_created, child.date_modified, child.name , 
        child.birthday, child.account_id  
        FROM child 
        WHERE child.id = ?

- pystyä muokkaamaan lapseni tietoja

        UPDATE child SET date_modified=CURRENT_TIMESTAMP, name=?, birthday=? 
        WHERE child.id = ?

- pystyä poistamaan lisäämäni lapsen

        DELETE FROM child WHERE child.id = ?


        Tässä poistettava myös lapseen liittyvät:

        DELETE FROM likes WHERE likes.id = ?

        DELETE FROM quotecategory WHERE quotecategory.quote_id = ? AND quotecategory.category_id = ?

        DELETE FROM quote WHERE quote.id = ? 

### Ylläpitäjä

Ylläpitäjänä haluan...

- voida lisätä ja poistaa kategorioita

        INSERT INTO category (date_created, date_modified, name) 
        VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?)

- voida poistaa kategorioita

        DELETE FROM category WHERE category.id = ?

- voida muokata kategoriaa

        UPDATE category SET date_modified=CURRENT_TIMESTAMP, name=? WHERE category.id = ?

- voida poistaa (mahdollisesti sopimattomia) sanontoja (SQL lause ylempänä käyttäjän sanonnan poiston yhteydessä)

- voida nähdä kaikkien käyttäjien listauksen ja heidän lapsimääränsä

        SELECT Account.id, Account.username, COUNT(Child.id) AS total FROM Account
        LEFT JOIN Child ON Child.account_id = Account.id
        GROUP BY Account.id

- nähdä käyttäjien tarkemmat tiedot ja listauksen käyttäjän lapsista

        SELECT account.id, account.date_created, account.date_modified, 
        account.name, account.username, account.password, account.role 
        FROM account 
        WHERE account.id = ?

        SELECT child.id, child.date_created, child.date_modified, child.name, 
        child.birthday, child.account_id 
        FROM child 
        WHERE child.account_id = ?

- voida poistaa rekisteröityneen käyttäjän

        Tässä tulee poistaa myös käyttäjään liittyvät lapset, lapsien sanonnat ja sanontojen tykkäykset

        DELETE FROM quotecategory WHERE quotecategory.quote_id = ? AND quotecategory.category_id = ?
        DELETE FROM likes WHERE likes.id = ?
        DELETE FROM quote WHERE quote.id = ?
        DELETE FROM child WHERE child.id = ?

        DELETE FROM account WHERE account.id = ?
