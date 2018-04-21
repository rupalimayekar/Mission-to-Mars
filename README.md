# Mission-to-Mars

![mission_to_mars](images/mission_to_mars.jpg)

This Web Scraping project gets information about the planet Mars from various websites and displays it on a single html page. It saves the scraped information into a Mongo database and then retrieves it for diaplay on an html page.

## Websites for data scraping
The following websites are visited by the python script on clicking the "Go to Mars" button on the top of the page:

* ``NASA Mars News`` - https://mars.nasa.gov/news/
* ``JPL Mars Space Inage`` - https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
* ``Mars Weather Twitter page`` - https://twitter.com/marswxreport?lang=en
* ``Mars Facts page`` - https://space-facts.com/mars/
* ``Mars Hemispheres images`` - https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars

## Technologies used
The following technologies are used for this project:
* Python for the application
    * Flask for the web app
    * splinter for data scraping
    * BeautifulSoup for data scraping
* Mongo database to store all the scraped information
* HTML & Bootstrap for the web page design

You can checkout the [scrape-mars.md](scrape-mars.md) file for details on how the data scraping is done.

## Resulting webpage
The following is the sample of the resulting webpage that is created by this application.

[mission_to_mars](Mission-to-Mars.html)



        
