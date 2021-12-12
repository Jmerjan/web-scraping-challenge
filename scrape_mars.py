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


    #scraping for feature img
    space_url= 'https://spaceimages-mars.com/'
    browser.visit(space_url)

    html= browser.html
    soup= bs(html, 'html.parser')
    browser.links.find_by_partial_text('FULL IMAGE').click()
    featured_image=soup.find('img', class_='headerimage')['src']
    featured_image_url= space_url + featured_image
    
    #Mars Table 
    table_url = 'https://galaxyfacts-mars.com/'
    table = pd.read_html(table_url)
    df = table[0]
    df.set_index(0)
    mars_html=df.to_html(index=False)

    soup = bs(response, 'html.parser')

    mars_html

    # Mars Hemisphere Data
    hem_url='https://marshemispheres.com/'
    browser.visit(hem_url)
    # Parse with beautiful soup
    html= browser.html

#use beautiful soup for HTML parsing
    hem_soup= bs(html, 'html.parser')

#create the variables to find the URLs and hem lists

#make dictionary with the title: name and img_url for each hemisphere

    hem_list=hem_soup.find_all('div', class_='item')
    hem_img_url=[]
    title_list=[]
    hem_list_dict=[]

#for loop through each hem
    for hem in hem_list:
        title= hem.find('h3').text
        title_list.append(title)
    
    #find image through anchor tag
        img_url=hem.find('a', class_='itemLink product-item')['href']
    
        browser.visit(hem_url + img_url)
    
        img_html= browser.html
    
        mars_soup= bs(img_html, 'html.parser')
    
        hem_img_url= hem_url + mars_soup.find('img', class_='wide-image')['src']
        # print(hem_img_url)
    
        hem_list_dict.append({"title": title, "img_url": hem_img_url})

        print(hem_list_dict, hem_img_url )


    mars_data={
        "mars_news_t": news_title,
        "mars_news_p": news_p,
        "mars_feat_img": featured_image_url,
        "mars_table":mars_html,
        "hem_img_0": hem_list_dict[0]['img_url'],
        "hem_img_1": hem_img_url[1],
        "hem_img_2": hem_img_url[2],
        "hem_img_3": hem_img_url[3],
        "hem_title_0":hem_list_dict[0]['title'],
        "hem_title_1":hem_list_dict[1]['title'],
        "hem_title_2":hem_list_dict[2]['title'],
        "hem_title_3":hem_list_dict[3]['title']
    }

    print(mars_data)
    browser.quit()
    return mars_data
