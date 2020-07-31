from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

import time
import re
​
def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    
    # Run all scraping code (copied from jupyter notebook) and store in dictionary
​
    # 1.......Get Mars news
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    # Scrape page into soup
    html = browser.html
    soup = bs(html, 'lxml')
    results = soup.find_all('div', class_='list_text') 
        # scrape the article header 
    header = results[0].find('div', class_='content_title').text
    
    # scrape the article subheader
    subheader = results[0].find('div', class_='article_teaser_body').text
    
    # Dictionary to be inserted into MongoDB
    post = {
        'header': header,
        'subheader': subheader,
            }

    # Insert dictionary into MongoDB as a document
    collection.insert_one(post)
    
​
    # update below variables
    news_title = header
    news_p = subheader
​
​
    # 2.......Get featured image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
​
    # Find the more info button and click that
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3) 
    browser.click_link_by_partial_text('more info') 
    # Parse the resulting html with soup
​   html2 = browser.html
    img_soup = bs(html2, 'lxml')
    # Find the relative image url
​   img_url = img_soup.select_one("figure.lede a img").get("src")

​
​
​
    # 3.......Get hemispheres
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    # Starting my jupyternotebook code here
    #this holds all the urls. 
    hemisphere_image_urls = []

# Get a List of All the Hemispheres
links = browser.find_by_css("a.product-item h3")
for item in range(len(links)):
    hemisphere = {}
    
    # Find Element on Each Loop to Avoid a Stale Element Exception
    browser.find_by_css("a.product-item h3")[item].click()
    
    # Find Sample Image Anchor Tag & Extract <href>
    sample_element = browser.find_link_by_text("Sample").first
    hemisphere["img_url"] = sample_element["href"]
    
    # Get Hemisphere Title
    hemisphere["title"] = browser.find_by_css("h2.title").text
    
    # Append Hemisphere Object to List
    hemisphere_image_urls.append(hemisphere)
    
    # Navigate Backwards
    browser.back()
​
    # Click the link, find the sample anchor, extract the href
    

​
​
    # 5........Get mars facts
    URl = "http://space-facts.com/mars/"
    #use pd.read_html and df.to_html
    browser.visit(url)
    html5=browser.html
    facts_soup = bs(html5, 'html.parser')
    tables_df = ((pd.read_html(url))[0]).rename(columns={0: "Attribute", 1: "Value"}).set_index(['Attribute'])
    html_table = (tables_df.to_html()).replace('\n', '')
    #saves the table to an HTML File, if needed.
    tables_df.to_html('table.html')
    
​
​
    # Store all scraped data in a dictionary
    data = {"MarsTitle": Header,
            "MarsPara":  subheader,
            "Big Image":img_url,
            "Mars Hemispheres":hemisphere_image_urls,
            "Mars Facts":html_table
            }
​
    # Stop webdriver and return data
    browser.quit()
​
    return data
    # End Function
​
 
if __name__ == "__main__":
​
    # If running as script, print scraped data
    print(scrape_all())