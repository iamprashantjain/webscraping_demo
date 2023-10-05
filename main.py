from bs4 import BeautifulSoup
import pandas as pd
import requests
import pdb

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}

center_names = []
phone_numbers = []
ages = []
center_hours = []
directors = []
street_addresses = []
cities = []
states = []
zip_codes = []
href_links = []
li_href_links = []


url = "https://www.kindercare.com/our-centers"
r = requests.get(url, headers=headers)

soup = BeautifulSoup(r.text, "lxml")
div_elements = soup.find_all('div', {'data-state': True})

for div in div_elements:
    ul = div.find('ul', class_='list-plain')
    if ul:
        li_elements = ul.find_all('li')
        for li in li_elements:
            a = li.find('a')
            if a and 'href' in a.attrs:
                href = a['href']
                li_href_links.append("https://www.kindercare.com/" + href)


for href_link in li_href_links:
    r1 = requests.get(href_link, headers=headers)
    if r1.status_code == 200:
        soup1 = BeautifulSoup(r1.text, "lxml")

    try:
        # Extract center name
        center_name = soup1.find("h1", class_="cdp-center-name").text.strip()
        center_names.append(center_name)
    except:
        center_names.append("not available")

    try:
        # Extract complete address and split into components
        complete_addr = soup1.find("div", class_="center-details center-details--address").text.replace("Address:", "").strip()
        complete_addr_parts = complete_addr.split(",")

        street_addr = complete_addr_parts[0].strip()
        city = complete_addr_parts[1].strip()

        state_zip = complete_addr_parts[2].strip()
        state = state_zip.split()[0]
        zip_code = state_zip.split()[1]

        street_addresses.append(street_addr)
        cities.append(city)
        states.append(state)
        zip_codes.append(zip_code)
    except:
        street_addresses.append("not available")
        cities.append("not available")
        states.append("not available")
        zip_codes.append("not available")

    # Extract phone number
    try:
        call_button = soup1.find('a', class_="btn-2023 btn-2023__secondary btn-2023__secondary--call")
        if call_button:
            href_value = call_button['href']
            phone_number = href_value.replace('tel:', '')
            phone_numbers.append(phone_number)
    except:
        phone_numbers.append("not available")

    # Extract ages
    try:
        age = soup1.find("div", class_="center-details center-details--ages").text.strip().replace("Ages:", '').strip()
        ages.append(age)
    except:
        ages.append("not available")

    # Extract center hours
    try:
        center_hour = soup1.find("div", class_="center-details center-details--hours").text.strip().replace("Open hours: ","")
        center_hours.append(center_hour)
    except:
        center_hours.append("not available")

    # Extract center director
    try:
        director = soup1.find("div", class_="center-details center-details--director").text.strip().replace("Center Director:",'').strip()
        directors.append(director)
    except:
        directors.append("not available")



data = {
    "Center Name": center_names,
    "Center Street Address": street_addresses,
    "Center City": cities,
    "Center State": states,
    "Center Zip Code": zip_codes,
    "Center Phone Number": phone_numbers,
    "Center Ages": ages,
    "Center Hours": center_hours,
    "Center Director": directors,
    "URL": li_href_links
}


df = pd.DataFrame(data)

df.to_excel("titan_data.xlsx", index=False)
