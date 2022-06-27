#WebScraping dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[ ]:


https://redplanetscience.com/


# In[23]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[4]:


#Visiting NASA MARS Website
url = 'https://redplanetscience.com/'
browser.visit(url)

# Delay for loading the page
browser.is_element_not_present_by_css('div.list_text', wait_time=1)


# In[8]:


#Setting up the parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[10]:


# Finding the data
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[11]:


# Getting the first news only
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[37]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[36]:


# Find and click the FULL IMAGE button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[31]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[17]:


#Finding the relative image url

img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[18]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[20]:


mars_df = pd.read_html('https://galaxyfacts-mars.com')[0]
mars_df.columns = ['description','Mars', 'Earth']
mars_df.set_index('description', inplace=True)


# In[21]:


mars_df


# In[22]:


mars_df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# In[78]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'


# In[91]:


# 2. Create a list and dictionary to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

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
    


# In[92]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[93]:


# 5. QUIT THE BROWSER
browser.quit()

