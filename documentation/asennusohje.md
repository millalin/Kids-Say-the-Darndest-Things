# Ohjelman asennusohje

### Oletusasetukset

Tietokoneella tulisi olla asennettuna Python 3 sekä sqlite3. Ubuntussa nämä voidaan asentaa komennolla

    sudo apt -get install python3
    sudo apt-get install sqlite3


### Ohjelman asennus ja käyttäminen paikallisesti

- Lataa ohjelma zip-versiona ja pura tiedosto. 
- Komentorivillä ohjelman kansiossa asenna virtuaaliympäristö komennolla 
    python3 -m venv venv
- Aktivoi virtuaaliympäristö komennolla 
    source venv/bin/activate
- Lataa tarvittavat riippuvuudet komennolla 
    pip install - r requirements.txt
- Käynnistä sovellus kirjoittamalla 
    python3 run.py 

Tietokantataulut luodaan automaattisesti sovelluksen käynnityessä. Sovellus toimii lokaalisti osoitteessa http://localhost:5000/


### Herokussa toimivan sovelluksen asentaminen

- asenna sovellus ylläolevien ohjeiden mukaisesti (poislukien viimeinen käynnistä kohta)
- Requirements.txt tiedoston tulisi olla ajantasaisesti päivitetty, kun projekti on ladattu Githubista. Varmista kuitenkin, ettei tiedostossa ole pkg-resources==0.0.0 riviä.
- Heroku käynnistää sovelluksen Procfile tiedoston avulla. Tiedosto voidaan luoda komennolla

    echo "web: gunicorn --preload --workers 1 hello:app" > Procfile

- navigoi paikallisen projektin kansioon ja luo paikka sovellukselle Herokuun komennolla

    heroku create projektin_nimi

- luo ohjelmalle versionhallinta
 
    git init 

- lisää tieto Herokusta paikalliseen versionhallintaan ja lähtetä ohjelma Herokuun:

    git remote add heroku https://git.heroku.com/projektin_nimi.git
    git add .
    git commit -m"Heroku"
    git push heroku master  

- Luodaan vielä Herokuun ympäristömuuttuja HEROKU

    heroku config:set HEROKU=1

- lisätään Herokuun vielä tietokanta

    heroku addons:add heroku-postgresql:hoppy-dev


Sovelluksen tulisi nyt toimia osoitteessa https://<projektin_nimi>.herokuapp.com 
