# Dependencies
from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
import pandas as pd
import time

def scrape():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    # Dictionary to save data to
    mars_dictionary = {}
    
    # NASA Mars News
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(2)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve all article slides
    slides = soup.find_all('li',class_='slide')
    # Find the title and text of article and save to dictionary
    mars_dictionary["news_title"] = slide.find('div',class_='content_title').text.strip()
    mars_dictionary["news_text"] = slide.find('div',class_='article_teaser_body').text.strip()
    
    # JPL Mars Space Images - Featured Image
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    time.sleep(2)
    html = browser.html
    # Use splinter to click on the Full image button
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    html2 = browser.html
    # Retrieve the link the image url
    soup = BeautifulSoup(html2, 'lxml')
    mars_dictionary["mars_images"] = soup.find('div',class_='fancybox-inner').find('img')
    
    # Mars Weather
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    mars_dictionary["mars_weather"] = soup.find('p',class_='tweet-text').text
    
    # Mars Facts
    # Use the read_html function in Pandas to scrape any tabular data from the page
    url4 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url4)
    # Format the first dataframe in the tables list.
    df = tables[0]
    df = df.rename(columns={0:''})
    df = df.rename(columns={1:'values'})
    df.set_index('',inplace=True)
    mars_dictionary["facts"] = df
    
    # Mars Hemispheres
    hemispheres = ['Cerberus Hemisphere','Schiaparelli Hemisphere', 'Syrtis Major Hemisphere','Valles Marineris Hemisphere']

    hemisphere_image_urls = []
    for hemisphere in hemispheres:
        url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url5)
        button = browser.find_link_by_partial_text(hemisphere)
        button.click()
        time.sleep(1)
        html = browser.html
        soup = BeautifulSoup(html, 'lxml')
        hemisphere_title=soup.find('section',class_='block metadata').find('h2').text
        image_div= soup.find('div',class_='downloads')
        hemisphere_image=image_div.ul.find_all('li')[1].a['href']
        hemisphere_image_urls.append({"title":hemisphere_title,"img_url":hemisphere_image})
    mars_dictionary["hemisphers"] = hemisphere_image_urls
    browser.quit()
    
    return mars_dictionary