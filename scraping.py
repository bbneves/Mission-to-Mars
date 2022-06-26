#WebScraping dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

#Set up splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

#Visiting NASA MARS Website
url = 'https://redplanetscience.com/'
browser.visit(url)

# Delay for loading the page
browser.is_element_not_present_by_css('div.list_text', wait_time=1)

#Setting up the parser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

# Finding the data
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Getting the first news only
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

### Featured Images
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the FULL IMAGE button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

#Finding the relative image url

img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

### Mars Facts
mars_df = pd.read_html('https://galaxyfacts-mars.com')[0]
mars_df.columns = ['description','Mars', 'Earth']
mars_df.set_index('description', inplace=True)

mars_df.to_html()

browser.quit()

