from bs4 import BeautifulSoup
from selenium import webdriver
from mongodb import add_entries
import time

# define the driver to use and the page to scrape.
# Selenium supports various browsers/drivers, I'm using the one for Firefox
path = r'C:\\Users\\Annik\\Geckodriver\\geckodriver.exe'
driver = webdriver.Firefox(executable_path = path)
main_url = "https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/13375-Extension-of-EU-Digital-COVID-Certificate-Regulation/feedback_de?p_id=27926341"

# run the driver, access the page, and get its HTML
try:
    driver.get(main_url)
    time.sleep(3)

    html = driver.page_source
    pageSoup = BeautifulSoup(html, "html.parser")
    driver.close()
except Exception as e:
    print(e)

# let's derive the last comment page from the pagination items
def getLastPage(soup):
    pages = soup.find_all('ecl-pagination-item', {'class': 'ecl-pagination__item'})
    print(f"last page: {pages[-2].text}")
    return int(pages[-2].text)

# now we know the last comment page:
last_page = getLastPage(pageSoup)

# we'll start at index 0 of course
load_index = 0

# when the comment section was still open, new comments got added to the first page,
# which made it difficult to retrieve them without accidentally skipping content.
# Meanwhile, the comment section has been closed 
# so we can simply start scraping on page one and continue up until the last page: 
while load_index < last_page:
    page_no = load_index + 1
    page_comments = []

    # opening the driver and having it access the page...
    print(f"loading page {page_no}")
    url = f"{main_url}&page={load_index}"
    driver = webdriver.Firefox(executable_path = path)
    try:
        driver.get(url)
        # generating comments is slow so we give the driver some time
        time.sleep(10)
        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")
        driver.close()
    except Exception as e:
        print(e)
        with open('error_logs.txt', 'w') as log:
            log.write(f"an exception occurred on page {page_no} (index {load_index})")
            log.write(str(e))
            log.close()

    # now we get all names, comment texts, and submit dates
    names = soup.find_all('div', {'class' : 'ecl-u-type-prolonged-m'})
    comment_texts = soup.find_all('p', {'class' : 'ecl-u-type-paragraph'})
    dates = soup.find_all('time')

    # if comments couldn't be retreived in time, try again
    if names == []:
        continue

    # else, use data to create a dict for each comment and append it to the comments list:
    i = 0
    while i < len(names):
        datetime = dates[i].attrs['datetime']
        date_and_time = datetime.rsplit(" ")
        comment = {
            "page_index": load_index,
            "page_no": page_no,
            "comment_no": (load_index * 10) + i + 1,
            "name": names[i].text,
            "date": date_and_time[0],
            "time": date_and_time[1],
            "comment": comment_texts[i].text
        }
        # add comment to the page_comments list
        page_comments.append(comment)
        i += 1

    # add page comments to db
    add_entries(page_comments, page_no)

    # okay, that's it for this page. Let's increase our index so we can get the next page's content!
    load_index += 1