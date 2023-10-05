from bs4 import BeautifulSoup
import requests
import concurrent.futures

# Send a GET request to the website
url = "https://www.kindercare.com/our-centers"
r = requests.get(url)

# Create a BeautifulSoup object to parse the HTML
soup = BeautifulSoup(r.text, "lxml")

# Find all the div elements with the 'data-state' attribute
div_elements = soup.find_all('div', {'data-state': True})

# Initialize a list to store the HTML content
html_contents = []

li_href_links = []

for div in div_elements:
    ul = div.find('ul', class_='list-plain')
    if ul:
        li_elements = ul.find_all('li')
        for li in li_elements:
            a = li.find('a')
            if a and 'href' in a.attrs:
                href = a['href']
                li_href_links.append("https://www.kindercare.com/" + href)

webdata = ""

for link in li_href_links:
    response = requests.get(link)
    if response.status_code == 200:
        webdata += response.text

with open("output2.html", "w", encoding="utf-8") as html_file:
    html_file.write(webdata)        
