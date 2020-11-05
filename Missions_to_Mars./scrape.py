#import dependencies.
from splinter import Browser
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager
from pprint import pprint
import pandas as pd

# Let's get a splinter automated browser going and navigate

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
#visit the web
url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
browser.visit(url)
time.sleep(5)

# Web to Scraper
def home():

    # Create BeautifulSoup object; parse with html
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    slides = soup.find_all('li', class_='slide')

    #get the first row in the slide list, find the title

    news_title = slides[0].find('div', class_ = 'content_title').text
    news_title

    #get the first row in the slide list, find the paragrap called 'article_teaser_body'

    news_p = slides[0].find('div', class_ = 'article_teaser_body').text
    news_p


    # # JPL Mars Space Images - Featured Image

    # visit the mars images web
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(5)

    # find and click the button
    button = browser.find_by_id("full_image")
    button.click()
    time.sleep(5)

    # find aans click a second button 
    browser.is_element_present_by_text('more info', wait_time=1)
    button_two = browser.links.find_by_partial_text("more info")
    button_two.click()

    # Create BeautifulSoup object; parse with html
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    img_url_rel = soup.select_one('figure.lede a img').get("src")
    img_url_rel
