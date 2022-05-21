from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json

# define the driver to use and the page to scrape.
# Selenium supports various browsers/drivers, I'm using the one for Firefox
path = r'C:\\Users\\Annik\\Geckodriver\\geckodriver.exe'
driver = webdriver.Firefox(executable_path = path)
main_url = "https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/13375-Extension-of-EU-Digital-COVID-Certificate-Regulation/feedback_de?p_id=27926341"

# run the driver, access the page, and get its HTML
driver.get(main_url)
time.sleep(3)

html = driver.page_source
pageSoup = BeautifulSoup(html, "html.parser")

# first, let's find the last comment page from the pagination items
def getLastPage(soup):
    pages = soup.find_all('ecl-pagination-item', {'class': 'ecl-pagination__item'})
    # extract 'prev' and 'next' pagination items
    print(f"last page: {pages[-2].text}")
    return int(pages[-2].text)

# now we know the index of the last comment page:
lastPageIndex = getLastPage(pageSoup) - 1
driver.close()

load_index = 0
comments = []

# when the comment section was still open, new comments got added to the first page,
# which made it difficult to retrieve them without accidentally skipping content.
# Now, the comment section is closed so we can simply start scraping on page one: 

while load_index <= 0:
    # opening the driver and having it access the page...
    print(f"loading page {load_index + 1}")
    url = f"{main_url}&page={load_index}"
    driver = webdriver.Firefox(executable_path = path)
    driver.get(url)
    # loading the comment section is quite slow,
    # so I make sure to wait long enough before getting the content
    time.sleep(9) 
    
    html = driver.page_source
    soup = BeautifulSoup(html, features="html.parser")

    # now we get all names, comment texts, and submit dates...
    names = soup.find_all('div', {'class' : 'ecl-u-type-prolonged-m'})
    print(names)
    commentTexts = soup.find_all('p', {'class' : 'ecl-u-type-paragraph'})
    dates = soup.find_all('time')

    # ...and use them to create a dict for each comment that we then append to the comments list:
    i = 0
    while i < len(names):
        datetime = dates[i].attrs['datetime']
        date_and_time = datetime.rsplit(" ")
        comments.append({
            "page_index": load_index,
            "page_no": load_index + 1,
            "comment_no": len(comments) + 1,
            "name": names[i].text,
            "date": date_and_time[0],
            "time": date_and_time[1],
            "comment": commentTexts[i].text
        })
        i += 1
    
    driver.close()

    # okay, that's it for this page. Let's increase our index so we can get the next page's content!
    load_index += 1

# All content retreived. Let's print the comments in pretty JSON!
json_comments = json.dumps(comments, indent=4, sort_keys=True, ensure_ascii=False)
print(json_comments)