# Web Scraper - volby 2017

## Co je to
Tento program získá výsledky parlametních voleb 2017 pro vybraný okres a uloží je do CSV souboru.

## Jak na to 
Nainstalujte si knihovny ze souboru requirements.txt

do příkazového řádku napište příkaz:

python web_scraper.py <"odkaz"> <"název souboru csv">

např. takhle

python web_scraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7101" "výsledek.csv"

výstup z tohoto příkazu je ve výsledek.csv
