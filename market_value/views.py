import requests
from bs4 import BeautifulSoup
from django.shortcuts import render


def market_value(request):
    URL = 'https://www.transfermarkt.es/fc-barcelona/kader/verein/131'

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'

    headers = {
        'User-Agent': user_agent,
    }

    response = requests.get(URL, headers=headers)
    webpage = response.text

    soup = BeautifulSoup(webpage, 'html.parser')

    table = soup.find(name="table", class_="items")

    odd_records = table.find_all(name="tr", class_="odd")
    even_records = table.find_all(name="tr", class_="even")

    player_data = []

    def data_scrapper(record):
        player_number = record.find("div", class_="rn_nummer").text
        player_name = record.find(name="td", class_="hauptlink").find(name="a").text.strip()
        position = record.find_all('td')[4].get_text(strip=True)
        market_value = record.find(name="td", class_="rechts hauptlink").find('a').get_text()
        age = record.find_all('td')[5].get_text(strip=True)
        contract_end_date = record.find_all('td')[7].get_text(strip=True)
        img_src_player = record.find(name="td", rowspan="2").find("img").get("data-src")
        img_src_flag = record.find_all(name="td", class_="zentriert")[2].find("img").get("src")
        country = record.find_all(name="td", class_="zentriert")[2].find("img").get("title")
        return {
            "player_number": player_number,
            "player_name": player_name,
            "position": position,
            "market_value": market_value,
            "age": age,
            "contract_end_date": contract_end_date,
            "img_src_player": img_src_player,
            "img_src_flag": img_src_flag,
            "country": country
        }

    for records in [odd_records, even_records]:
        for record in records:
            player_data.append(data_scrapper(record))

    total_players = len(player_data)

    return render(request, 'market_value.html', {'player_data': player_data, 'total_players': total_players})
