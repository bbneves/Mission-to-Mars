#WebScraping dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    #Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    hemispheres = mars_hemispheres(browser)

    # Run all scraping funciotn and store resultes in dectionary:
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres
    }
    
    #Stop webdriver and return data
    browser.quit()
    return data

### FEATURED NEWS

def mars_news(browser):
    #Visiting NASA MARS Website
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Delay for loading the page
    browser.is_element_not_present_by_css('div.list_text', wait_time=1)

    #Setting up the parser, converting browser html to a soup objetct
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Finding the data with the first <a> tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Getting the first new paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p

### FEATURED IMAGES

def featured_image(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the FULL IMAGE button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        #Finding the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        

    except AttributeError:
        return None,None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

### MARS FACTS
def mars_facts():
    try:
        mars_df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    #Formatting the DF
    mars_df.columns = ['description','Mars', 'Earth']
    mars_df.set_index('description', inplace=True)
    mars_table = mars_df.to_html(classes=["table-striped table-hover table-dark"] )
    # COnvert the df into HTML format, add bootsctrap
    return mars_table

### MARS HEMISPHERES
def mars_hemispheres(browser):
    url = 'https://marshemispheres.com/'
    hemisphere_image_urls = []

    for i in range(4):
        hemis = {}
        # Visiting the site and clicking in the image link
        browser.visit(url)
        browser.find_by_tag('h3')[i].click()
        
        # Parse from html to work with it
        img_location = soup(browser.html,'html.parser')
        
        # Locating the image and saving its url to "img_hem"
        img = img_location.find('img', class_='wide-image').get('src') 
        img_hem = f'https://marshemispheres.com/{img}'
        # Locating the name and saving its text to "name"
        name = img_location.find('h2', class_='title').text
        # Filling the Dictionary and Adding it to the list
        hemis[f'img_url'] = img_hem
        hemis[f'title'] = name
        hemisphere_image_urls.append(hemis)
        
        #Returning to main page to continue
        browser.back()

    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())