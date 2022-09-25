# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
import pymongo

def init_browser():
    # Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

mars_info = {}

def scrape_mars_news():

    browser = init_browser()

    # Visit Nasa news url through splinter module
    url = 'https://redplanetscience.com'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_info["news_title"] = soup.find('div', class_='content_title').text
    mars_info["news_paragraph"] = soup.find('div', class_='article_teaser_body').text
        
    return mars_info

def scrape_mars_image():

    browser = init_browser()

    # Visit Mars Space Images url through splinter module
    image_url = 'https://spaceimages-mars.com/'
    browser.visit(image_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_image_url = soup.find('img', class_='headerimage fade-in')['src']
    
    featured_image_url = image_url + featured_image_url
    mars_info["featured_image_url"] = featured_image_url 
        
    return mars_info

def scrape_mars_facts():
    # Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about Mars
    url='https://galaxyfacts-mars.com/'
    tables=pd.read_html(url)
    
    mars_fact=tables[0]
    mars_fact=mars_fact.rename(columns={0:"Profile",1:"Value"},errors="raise")
    mars_fact.set_index("Profile",inplace=True)
    mars_fact
    
    fact_table=mars_fact.to_html()
    fact_table.replace('\n','')
    mars_info["mars_facts"] = fact_table

    return mars_info

def scrape_mars_hemispheres():
    browser = init_browser()
    hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(hemispheres_url)
    html = browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item')
    hemisphere_img_urls = []
    for item in items:
        title = item.find('h3').text
        hemisphere_url = 'https://marshemispheres.com/' + item.find('a', class_='itemLink product-item')['href']
        
        browser.visit(hemisphere_url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        hemisphere_img_url = 'https://marshemispheres.com/' + soup.find('img', class_='wide-image')['src']
        hemisphere_img_urls.append({'title': title, 'img_url': hemisphere_img_url})
    mars_info["hemisphere_img_urls"] = hemisphere_img_urls
    
    return mars_info