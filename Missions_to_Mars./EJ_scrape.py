#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import dependencies.
from splinter import Browser
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager
from pprint import pprint
import pandas as pd
import pymongo





# In[2]:
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars 

# news_title = "news_title"
# news_p = "news_p"
# big_img_url = "big_img_url"
# mars_df = "mars_df"
# img_url = "img_url"


def init_browser(): 
        # Let's get a splinter automated browser going and navigate
        executable_path = {'executable_path': ChromeDriverManager().install()}
        return Browser('chrome', **executable_path, headless=False)
        #visit the web

def scrape_info():
        browser = init_browser()
        collection.drop()

        url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
        browser.visit(url)
        time.sleep(5)


        # # NASA Mars News

# In[3]:



        # Create BeautifulSoup object; parse with html

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')


        # In[4]:

        #print(soup.prettify())

        # In[5]:


        slides = soup.find_all('li', class_='slide')

        # In[6]:

        #get the first row in the slide list, find the title

        news_title = slides[0].find('div', class_ = 'content_title').text
        news_title


        # In[7]:


        #get the first row in the slide list, find the paragrap called 'article_teaser_body'

        news_p = slides[0].find('div', class_ = 'article_teaser_body').text
        news_p


        # # JPL Mars Space Images - Featured Image

        # In[8]:


        # visit the mars images web
        url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(url)
        time.sleep(5)


        # In[9]:


        # find and click the button
        button = browser.find_by_id("full_image")
        button.click()
        time.sleep(5)


        # In[10]:


        # find aans click a second button 
        browser.is_element_present_by_text('more info', wait_time=1)
        button_two = browser.links.find_by_partial_text("more info")
        button_two.click()


        # In[11]:


        # Create BeautifulSoup object; parse with html
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')


        # In[12]:


        #get the img
        img_url_rel = soup.select_one('figure.lede a img').get("src")
        img_url_rel


        # In[13]:


        #make the img url
        big_img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
        big_img_url


        # In[ ]:





        # In[14]:


        #featured_image_url = url + soup.find('a',class_='button fancybox')['data-fancybox-href']
        #featured_image_url


        # # Mars Facts

        # In[15]:


        #visit the web
        url = "https://space-facts.com/mars/"
        browser.visit(url)
        time.sleep(5)


        # In[16]:


        #chech the tables in the web
        pd.read_html(url)


        # In[17]:


        #select the first table
        mars_df = pd.read_html(url)[0]
        mars_df


        # In[18]:


        # rename columns 
        mars_df.columns = ['Description', 'Mars']
        mars_df


        # In[19]:


        # setting Desxcription as index column
        mars_df.set_index("Description", inplace = True)
        mars_df


        # In[20]:


        # Use Pandas to convert the data to a HTML table string.
        html_tabla = mars_df.to_html() 
        print(html_tabla)


        # # Mars Hemispheres

        # In[21]:


        #visit the web
        url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url)
        time.sleep(5)


        # In[22]:


        # Create BeautifulSoup object; parse with html

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')


        # In[23]:


        print(soup.prettify())


        # In[24]:


        #find all the "div",class_='item
        results = soup.find_all("div",class_='item')
        #make and empty list
        img_url = []
        #make a loop 
        for result in results:
                #make and empty dicctionary 
                hemisphere_image_urls = {}
                # declare titles
                titles = result.find('h3').text
                # declare links 
                link = result.find("a")["href"]
                base_link = "https://astrogeology.usgs.gov/" + link 
                #visit the web
                browser.visit(base_link)
                html = browser.html
                soup= BeautifulSoup(html, "html.parser")
                        #finde the image
                downloads = soup.find("div", class_="downloads")
                image_url = downloads.find("a")["href"]
                print(titles)
                print(image_url)
                #append the dictionary
                hemisphere_image_urls['title']= titles
                hemisphere_image_urls['image_url']= image_url
                #append the list with the diccionary 
                img_url.append(hemisphere_image_urls)


# In[ ]:




# In[ ]:

        # Store data in a dictionary
        mars_data = {

                'news_title' : news_title,
                'news_p': news_p,
                'big_img_url': big_img_url,
                'html_tabla': html_tabla,
                'hemispheres': img_url,
        }
         # Return results
        return mars_data
         # Close the browser after scraping
        browser.quit()






