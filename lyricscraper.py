from bs4 import BeautifulSoup
import requests
import time


MAIN_PAGE = "https://www.azlyrics.com"
COHEN_PAGE = "/c/cash.html"
FOLDER_PATH = "D:/final_project/cash_lyrics/"
LYRICS = []


print("Starting scraping Johnny Cash's lyrics...")

print("Getting links to pages of lyrics...")
main_page = requests.get(MAIN_PAGE + COHEN_PAGE)
soup = BeautifulSoup(main_page.text, 'lxml')
listAlbum = soup.find('div', id='listAlbum')

for link in listAlbum.find_all('a'):
    lyrics_link = link.get('href')[2:]
    LYRICS.append(MAIN_PAGE + lyrics_link)
print("Getting links to pages of lyrics is done.")

number_of_lyrics = len(LYRICS)

print("Start getting lyrics...")
counter = 0
for link in LYRICS:
    file_name = link.split('/')[-1][:-5]

    print(f'Status: {counter+1}/{number_of_lyrics}')
    print(f'Lyrics name: {file_name}')

    lyrics_page = requests.get(link)
    soup = BeautifulSoup(lyrics_page.text, 'lxml')
    content = soup.find('div', class_='col-xs-12 col-lg-8 text-center')
    divs = content.find_all('div')
    lyrics = divs[6].text

    with open(f'{FOLDER_PATH}{file_name}.txt', 'w', encoding='utf-8') as file:
        try:
            file.write(lyrics)
        except Exception as e:
            print(e)

    counter += 1
    if counter % 5 == 0:
        print("Have a 1 minute break...")
        time.sleep(60)
    else:
        print("Have a 24 seconds break...")
        time.sleep(24)
print("Getting lyrics is done.")

print("Finished with scraping. Johnny Cash's lyrics are collected!")
