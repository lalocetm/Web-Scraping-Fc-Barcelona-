from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import pandas as pd
from fake_useragent import UserAgent
# Create your views here.


def trophy_data(request):
    URL = 'https://www.fcbarcelona.es/es/club/identidad'
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'

    headers = {
        'User-Agent': user_agent,
    }

    response = requests.get(URL, headers=headers)
    webpage = response.text

    soup = BeautifulSoup(webpage, 'html.parser')
    records = soup.find_all(name="div", class_="footer__trophies")
    trophy_data = []

    def data_scrapper(record):
        competition = [span.text for span in record.find_all('span', class_='footer-trophies__competition-name')]
        trophy_count = [span.text for span in record.find_all('span', class_='footer-trophies__trophy-count')]
        competition_type = [span.text for span in record.find_all('span', class_='footer-trophies__competition-type')]

        return competition, trophy_count, competition_type

    for record in records:
        competition, trophy_count, competition_type = data_scrapper(record)

        for comp, count, ctype in zip(competition, trophy_count, competition_type):
            trophy_data.append({'competition': comp, 'trophy_count': count, 'competition_type': ctype})

    return render(request, 'core/home.html', {'trophy_data': trophy_data})
