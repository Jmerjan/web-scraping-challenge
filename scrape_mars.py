import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
import time



def scrape():

    #setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #connect to URL and us beautiful soup
    red_url= 'https://redplanetscience.com/'
    browser.visit(red_url)
    response = browser.html
    soup = bs(response, 'html.parser')

    #Find the news title variables for the most recent
    news_title=soup.find_all('div', class_='content_title')[0].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

    


    mars_data={
        "mars_news_t": news_title,
        "mars_news_p": news_p
    }

    browser.quit()
    return mars_data
