###########################################################
################ Mission to Mars ################
# 
# This module is designed to scrape various websites to gather information about the planet Mars. 
# This information is related to the latest news on Mars, weather, pictures, etc. The gathered 
# information is saved into data objects for use later when they will all be displayed on a webpage.
# There is one scrape fulction that does all the data gathering and returns a dictionary with all the data.
###########################################################

# Import dependencies
import pandas as pd
import requests as req
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time


# The scrape function
def scrape() :
        # Use splinter with the chrome browser to scrape all the data
        executable_path = {'executable_path': '/usr/local.bin.chromedriver'}
        browser = Browser('chrome', headless=False)

        # Define the data dictionary that will hold all the scraped information which will be returned
        # by this function
        data = {}

        # ## Scraping the NASA Mars website for the latest news on Mars
        # We will scrape the following NASA website for the latest news about the planet Mars. https://mars.nasa.gov/news/
        # We will just get the latest news title and description and save it for later.

        # Tell the browser to visit the NASA news website
        nasa_news_url = "https://mars.nasa.gov/news/"
        browser.visit(nasa_news_url)

        # Extract the html from the webpage using BeautifulSoup
        soup = bs(browser.html, 'html.parser')

        # Look for the first div tag with the class "image_and_description_container" to get the 
        # latest news
        news_result = soup.find('div', class_='image_and_description_container')


        # Get the description from the latest news
        description = news_result.find('div', class_='rollover_description_inner').text.strip()
        print("News Description : " + description)

        # Get the title from the latest news
        news_result = soup.find('div', class_='content_title')
        title = news_result.find('a').text.strip()
        print("\nNews Title : " + title)

        # Add the news to the data object
        data["News"] = {"title": title, "description": description}

        # ## JPL Mars Space Image
        # 
        # Now we visit the following website: https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
        # 
        # We will get the url to the current featured Image on Mars from this website. We need to get the largesize image so we will navigate as specified below:
        # 
        # * Click on the button named "FULL IMAGE" on the main page featured image. We get to the images page
        # * Click on the button named "more info" for the featured image on the images page. We get to the Image Details page. This still displays the medium sized image.
        # * Click on the actual image link on this image on the Image Details page to get to the actual large size image. Now we will get the full url to the large image.

        jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

        # Use splinter to visit the JPL website
        browser.visit(jpl_url)

        # Click on the button on top of the featured image. It saya "FULL IMAGE". Then wait for 5 seconds
        browser.click_link_by_partial_text('FULL IMAGE')
        time.sleep(5)

        # This is the link to the mediumsize image. We need the largesize image
        # Now click on the button that says "more info"
        browser.click_link_by_partial_text('more info')
        time.sleep(5)

        # This is the medium size image too. We need to click on this image link that has the largesize image
        links = browser.find_link_by_partial_href('/spaceimages/images/largesize/')
        links.first.click()
        time.sleep(5)

        # print the contents of this page. This is the large image
        soup = bs(browser.html, 'html.parser')
        print(soup.prettify())

        # We now have the complete url for the largesize image. Extract the url
        featured_image_url = soup.find('img').get('src')
        print("Featured Image URL : " + featured_image_url)

        # Add the image url to the data object
        data["Featured_Image"] = featured_image_url
        
        # ## Getting the Mars Weather
        # We will now visit the Mars weather twitter page at : https://twitter.com/marswxreport?lang=en
        # 
        # Here we will get the latest weather on Mars. We will extract the latest tweet here.

        # Visit the mars weather twitter page
        mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(mars_weather_url)
        time.sleep(5)

        # Extract the latest tweet
        soup = bs(browser.html, 'html.parser')
        mars_weather = soup.find('p', class_='TweetTextSize').text.strip()
        print("Mars Weather : " + mars_weather)

        # Add the weather to the data object
        data["Weather"] = mars_weather

        # ## Getting Mars Facts
        # Next we will visit the following website: https://space-facts.com/mars/
        # 
        # Here we will get the facts on Mars from the main page. This is in the form of a table, so we will use Pandas to extract the table from the page.

        # Read the html for the Mars facts webpage and extract the first table from the list
        mars_facts_url = "https://space-facts.com/mars/"
        df = pd.read_html(mars_facts_url)[0]

        # Change the column names to something meaningful
        df.rename(columns={0:"Fact", 1:"Value"},  inplace=True)

        # Convert the dataframe into an html table
        html = df.to_html(header=True, index=False, border="1")

        # Add the facts to the data object
        data["Facts"] = html

        # ## Mars Hemispheres
        # 
        # Next we will visit this website: https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
        # 
        # Here we will get the urls for the pictures of the 4 hemispheres of Mars. We need to click on the link to each hemisphere, extract the image url, click the Back button, and repeat the same for the remaining 3 hemispheres.

        # Webpage and webpage root
        mars_hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        mars_hem_url_root = "https://astrogeology.usgs.gov"

        # Visit the page and extract the div tag which has a list of hemisphere images
        browser.visit(mars_hem_url)
        time.sleep(2)
        soup = bs(browser.html, 'html.parser')
        items = soup.find_all('div', class_='item')

        # List to store all hemisphere names and image urls
        hemispheres = []

        # Loop through the list items and extract each image url and title
        for item in items:
                # The title is in an h3 tag
                title = item.find('h3').text.strip()
                print(title)
                
                # Click on the title to get to the page where we will get the full image url
                links = browser.find_link_by_partial_text(title)
                links.first.click()
                time.sleep(2)
                
                # Get the relative image url and append it to the website root
                soup = bs(browser.html, 'html.parser')
                image_url = soup.find("img", class_="wide-image").get('src')
                full_image_url = mars_hem_url_root + image_url
                print(full_image_url)
                print("===============================")
                
                # Click on the back button to go back so we can navigate to the next image
                links = browser.find_link_by_partial_text("Back")
                links.first.click()
                
                # Save the title and url as a dict into the hemispheres list
                hemispheres.append({"title":title, "img_url":full_image_url})

        # Add the hemispheres to the data object
        data["Hemispheres"] = hemispheres

        return data
