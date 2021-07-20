from bs4 import BeautifulSoup
import requests
import time

# Program that checks new fragrances up for sale on parfumo against wish list.

def findPerfumes():
    """Finds perfumes on first page of URL and returns them in a list."""
    html_text = requests.get('https://www.parfumo.de/Souks/Offers/Perfumes').text
    soup = BeautifulSoup(html_text, 'lxml')
    perfumes = soup.find_all('div', class_='col')

    for perfume in perfumes:
        perfume_name = perfume.find('div', class_='name').text
        latest_perfumes.append(perfume_name)
        corresponding_links.append(perfume.a['href'])
    return latest_perfumes, corresponding_links

def matches(latest, wish):
    """Checks if perfume appears in wishlist and returns a boolean value."""
    return wish in latest

def foundPerfumes():
    """Checks if latest perfumes are in wish list and if returns them in dict
    with the respective link as value."""
    overlapping_perfume_and_link = {x: perfumes_and_links[x] 
    for x in perfumes_and_links if any(matches(x, y) for y in wishlist)}
    return overlapping_perfume_and_link

latest_perfumes = []
corresponding_links = []
wishlist = ['Layton', 'Herod', 'XerJoff', 'Vanilla']

# while True:
# starttime = time.time()
html_text = requests.get('https://www.parfumo.de/Souks/Offers/Perfumes').text
soup = BeautifulSoup(html_text, 'lxml')
perfumes = soup.find_all('div', class_='col')

findPerfumes()
# Creates a dictionary with the perfume name as key and the link as value.
perfumes_and_links = dict(zip(latest_perfumes, corresponding_links))
print(foundPerfumes())
# time.sleep(1800.0 - ((time.time() - starttime) % 1800.0))

