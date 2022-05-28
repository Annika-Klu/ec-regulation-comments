import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from mongodb.actions import log_err, add_entries

# Define the driver to use and the page to scrape.
# Selenium supports various browsers/drivers, I'm using the one for Firefox
driver_path = r'C:\\Users\\Annik\\Geckodriver\\geckodriver.exe'
main_url = "https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/13375-Extension-of-EU-Digital-COVID-Certificate-Regulation/feedback_de?p_id=27926341"

def load_driver():
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument("--headless")
    service = Service(executable_path = driver_path)
    return webdriver.Firefox(service=service, options=firefox_options)

# Start scraping at page index 0
load_index = 0

# Initialize last page at 1, redefine later during first page loading iteration
last_page = 1

# Method to derive the last comment page from the pagination items
def getLastPage(soup):
    pages = soup.find_all('ecl-pagination-item', {'class': 'ecl-pagination__item'})
    print(f"last page: {pages[-2].text}")
    return int(pages[-2].text)

# When the comment section was still open, new comments got added to the first page,
# which made it difficult to retrieve them without accidentally skipping content.
# Meanwhile, the comment section has been closed so I simply scrape from first to last page: 
while load_index < last_page:
    page_no = load_index + 1
    page_comments = []

    # open the driver and have it access the page...
    print(f"loading page {page_no}")
    url = f"{main_url}&page={load_index}"
    driver = load_driver()
    try:
        driver.get(url)
        # give it some time to load comments
        time.sleep(10)
        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")
        driver.close()
    except Exception as e:
        log_err(f"loading page {page_no}", "other", e)
    
    # use results from first page to determine last page and reset var accordingly
    if last_page == 1:
        last_page = getLastPage(soup)
        print(f"last page set to {last_page}")

    # get all names, comment texts, and submit dates
    try:
        names = soup.find_all('div', {'class' : 'ecl-u-type-prolonged-m'})
        comment_texts = soup.find_all('p', {'class' : 'ecl-u-type-paragraph'})
        dates = soup.find_all('time')
    # if page src couldn't be loaded, try again
    except NameError as e:
        continue

    # if page src available but comments couldn't be retreived in time, also try again
    if names == []:
        continue

    # else, use data to create a dict for each comment and append it to page_comments list:
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
        page_comments.append(comment)
        i += 1

    # insert page_comments list into db
    add_entries(page_comments, page_no)

    # That's it for this page. Increase index to get the next page's content!
    load_index += 1

# once all content retrieved, exit script
exit(0)