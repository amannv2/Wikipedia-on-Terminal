import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


print('>Initializing')

print('Loading', end='')

# use chrome and load Profile 1 user's settings
chrome_options = Options()
chrome_options.add_argument("--headless")

# path to chromedriver
chromedriver = os.path.dirname(__file__) + "/chromedriver"

print('.', end='')
os.environ["webdriver.chrome.driver"] = chromedriver

# idk, init?
print('.', end='')
driver = webdriver.Chrome(chromedriver, options=chrome_options)
print('.\n')

# open this URL
driver.get("https://en.wikipedia.org/wiki/Main_Page")

# get those input boxes by their XPath
try:
    query = driver.find_element_by_xpath('//*[@id="searchInput"]')

    # take input
    q = input('What do you want to search? ')

    # fill values into the input boxes
    query.send_keys(q)

    # required to load suggestions
    time.sleep(1)

    suggestions = driver.find_element_by_class_name('suggestions')

    # for suggestions_list in suggestions:
    div = suggestions.find_element_by_tag_name("div")

    # keep a list of all suggestions with their links
    link_list = []
    title_list = []

    # display all suggestions
    elements = div.find_elements_by_tag_name('a')

    for link in elements:
        link_list.append(link.get_attribute("href"))
        title_list.append(link.get_attribute("title"))

    i = 0
    for item in title_list:
        print(str(i) + ': ' + item)
        i = i + 1

    choice = int(input('Enter Your Choice: '))
    while choice < 0 or choice > i:
        choice = input('Enter Your Choice: ')

    print('\nOpening ' + title_list[choice] + ' in Wikipedia...')

    # open selected page
    driver.get(link_list[choice])

    # get hold of body and its <p> tags
    body = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[4]/div')
    para = body.find_elements_by_tag_name('p')

    print('\nDownloading all textual content...')

    # copy all body content
    buff = ''
    for p in para:
        buff = buff + '\n' + p.text

    # write all copied data into a file
    with open('wiki.txt', 'w', encoding="utf-8") as fp:
        fp.write(buff)

    # save page as html
    cur_page = driver.page_source
    soup = BeautifulSoup(cur_page, 'html.parser')

    with open('wiki.html', 'w', encoding="utf-8") as fp:
        fp.write(soup.prettify())

except:
    print('No Internet Connection')
    exit(-1)

# close the browser
print('\nDone. Quiting Now.')
driver.quit()
