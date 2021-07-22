import os
import time
import smtplib
import requests
from bs4 import BeautifulSoup

# Program that checks new fragrances up for sale on parfumo against wish list.

def findPerfumes():
    """Finds perfumes+links on first page of URL and returns them in a list."""
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
wishlist = ['Luna Rossa Black', 'Spicebomb Extreme', "L'Homme - Prada",
'Allure Homme Sport Eau Extrême', 'Layton', 'Musc', 'Velours']

# while True:
# starttime = time.time()
html_text = requests.get('https://www.parfumo.de/Souks/Offers/Perfumes').text
soup = BeautifulSoup(html_text, 'lxml')
perfumes = soup.find_all('div', class_='col')

findPerfumes()
perfumes_and_links = dict(zip(latest_perfumes, corresponding_links))
found = foundPerfumes()
frags_mail = ''


EMAIL_ADDRESS = os.environ.get('SMTP_USER')
PASSWORD = os.environ.get('SMTP_PWD')

# Send an email if matches are found. Look for matches every 60 minutes.
# if found:
for frag in found:
    frags_mail += f"{frag}\n{found[frag]}\n\n"

with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(EMAIL_ADDRESS, PASSWORD)
    
    subject = 'New Fragrance Alert!'
    body = frags_mail
    msg = f'Subject: {subject}\n\n{body}'
    smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)
        
# time.sleep(3600.0 - ((time.time() - starttime) % 3600.0))