import os
import time
import smtplib
import requests
from bs4 import BeautifulSoup

# Program that checks new fragrances up for sale on parfumo against wish list.

def findPerfumes():
    """Finds perfumes+linkid+links on first page of URL and returns them in a list."""
    html_text = requests.get('https://www.parfumo.de/Souks/Offers/Perfumes').text
    soup = BeautifulSoup(html_text, 'lxml')
    perfumes = soup.find_all('div', class_='col')
    for perfume in perfumes:
        temp_list = []
        perfume_name = perfume.find('div', class_='name').text
        temp_list.append(perfume_name)
        temp_list.append(perfume.a['href'][-7:])
        temp_list.append(perfume.a['href'])
        perfume_id_link.append(temp_list)
    return perfume_id_link

def item_occurs(item, wish):
    """Used as a boolean check in another function to see if the item
    is inside the wish list."""
    for s in wish:
        if s in item:
            return True
    return False

def foundPerfumes(itemlist, wish, alreadyseen):
    """Checks if the items on the front page are in wish list and if so
    adds them to an archive with an unique ID. Then it returns all the matches
    with their respective link."""
    new = []
    for item, i, link in itemlist:
        if item_occurs(item, wish) and (item, i) not in alreadyseen:
            alreadyseen.append((item, i))
            new.append((item, link))
    return new

archive = []

while True:
    perfume_id_link = []
    wishlist = ['Luna Rossa Black', 'Spicebomb Extreme', "L'Homme - Prada",
    'Kyoto', 'Avignon', 'Hinoki', 'Layton', 'Herod', 'Naxos', 'Reflection Man']
    starttime = time.time()

    findPerfumes()
    found = foundPerfumes(perfume_id_link, wishlist, archive)
    frags_mail = ''

    EMAIL_ADDRESS = os.environ.get('SMTP_USER')
    PASSWORD = os.environ.get('SMTP_PWD')

    # Send an email if matches are found. Look for matches every 10 minutes.
    if found:
        for frag in found:
            frags_mail += str(frag) + '\n'

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(EMAIL_ADDRESS, PASSWORD)
            
            subject = 'New Fragrance Alert!'
            body = frags_mail
            msg = f'Subject: {subject}\n\n{body}'
            smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.encode("utf8"))
            
    time.sleep(300.0 - ((time.time() - starttime) % 300.0))