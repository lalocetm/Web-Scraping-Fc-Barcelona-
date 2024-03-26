import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
import pandas as pd
# Create your views here.

def scrape_transfermarkt_data():
    URL = 'https://www.transfermarkt.es/fc-barcelona/mitarbeiter/verein/131'
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'

    headers = {
        'User-Agent': user_agent,
    }

    response = requests.get(URL, headers=headers)
    webpage = response.text

    soup = BeautifulSoup(webpage, 'html.parser')

    records = soup.find_all(name="table", class_="inline-table")

    staf_imgs = []
    staf_names = []
    staf_positions = []

    def data_scrapper(record):
        img = record.find(name="td", rowspan="2").find("img").get("src")
        name = record.find_all('td')[1].get_text(strip=True)
        position = record.find_all('td')[2].get_text(strip=True)
        return img, name, position

    for record in records:
        img, name, position = data_scrapper(record)

        staf_imgs.append(img) if img else None
        staf_names.append(name) if name else None
        staf_positions.append(position) if position else None

    data = {"Staf_imgs": staf_imgs, "Staf_names": staf_names, "Staf_positions": staf_positions}

    df = pd.DataFrame(data)
    return df



def staff_view(request):
    # Llamar a la función de scraping para obtener los datos
    df = scrape_transfermarkt_data()

    # Convertir el DataFrame a un diccionario de Python
    staff_data = df.to_dict(orient='records')

    # Pasar los datos a la plantilla HTML
    return render(request, 'staff/technical_staff.html', {'staff_data': staff_data})