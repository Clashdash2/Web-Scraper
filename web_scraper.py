import requests
import bs4
import csv
import sys

cislo_obce = list()
nazev_obce = list()
pocet_volicu = list()
pocet_hlasu = list()
pocet_platnych_hlasu = list()

vsechny_hlasy = []

nazvy_stran = set()

def web_scrape(odkaz, nazev_csv_souboru):

    nazvy_stran = []
    hlasy_stran = []

    page = requests.get(odkaz)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')

    html_cislo_obce = soup.find_all("td",class_="cislo")

    for td_cislo_obce in html_cislo_obce:
        cislo_obce.append(td_cislo_obce.text)


    html_jmeno_obce = soup.find_all("td", class_="overflow_name")

    for td_jmeno_obce in html_jmeno_obce:
        nazev_obce.append(td_jmeno_obce.text)

    x = 0
    for aktualni_obec in cislo_obce:
        adresa_obec = f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xobec={aktualni_obec}&xvyber=7101"
        response = requests.get(adresa_obec)

        s = bs4.BeautifulSoup(response.text, 'html.parser')
        x += 1

        td_volicu = s.find("td", class_="cislo", headers="sa2")
        pocet_volicu.append(td_volicu.text)

        td_hlasy = s.find("td", class_="cislo", headers="sa5")
        pocet_hlasu.append(td_hlasy.text)

        td_platnych_hlasu = s.find("td", class_="cislo", headers="sa6")
        pocet_platnych_hlasu.append(td_platnych_hlasu.text)


        html_strana_t1 = s.find_all("td",class_="overflow_name",headers="t1sa1 t1sb2")
        nazvy_stran.extend([s.text for s in html_strana_t1])
        html_pocet_hlasu_t1 = s.find_all("td",class_="cislo",headers="t1sa2 t1sb3")
        hlasy_stran.extend(h.text for h in html_strana_t1)
        html_strana_t2 = s.find_all("td",class_="overflow_name",headers="t2sa1 t2sb2")
        nazvy_stran.extend([s.text for s in html_strana_t2])
        html_pocet_hlasu_t2 = s.find_all("td",class_="cislo",headers="t2sa2 t2sb3")
        hlasy_stran.extend(h.text for h in html_strana_t1)

        pocet_hlasu_strany = {}
        for j, party_name in enumerate(nazvy_stran):
            if j < len(hlasy_stran):
                hlasy = hlasy_stran[j]
                pocet_hlasu_strany[party_name] = hlasy
                nazvy_stran.add(party_name)
            else:
                pocet_hlasu_strany[party_name] = "N/A"

        vsechny_hlasy.append(pocet_hlasu_strany)

    with open(nazev_csv_souboru, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["Číslo obce", "Název obce", "Počet voličů", "Počet hlasů", "Počet platných hlasů"] + sorted(list(nazvy_stran))
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(len(cislo_obce)):
            row = {
                "Číslo obce": cislo_obce[i],
                "Název obce": nazev_obce[i],
                "Počet voličů": pocet_volicu[i],
                "Počet hlasů": pocet_hlasu[i],
                "Počet platných hlasů": pocet_platnych_hlasu[i]
            }
            for nazev_strany in sorted(list(nazvy_stran)):
                row[nazev_strany] = vsechny_hlasy[i].get(nazev_strany, "0")
            writer.writerow(row)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(1)

    url = sys.argv[1]
    csv_nazev = sys.argv[2]

    web_scrape(url, csv_nazev)