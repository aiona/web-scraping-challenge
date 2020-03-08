from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd


def init_browser():
    executable_path = {'executable_path': '/Users/adamiona/Desktop/Python_Stuff/web-scraping-challenge/chromedriver'}
    browser = Browser("chrome", **executable_path, headless=False)

    return browser

def scrapeNews():
    browser = init_browser()
    mars_info = {}
    
   #Get Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    browser.is_element_present_by_css('ul.item_list li.slide', wait_time=0.75)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Get title and paragraph text. 
    article_title = soup.find_all('div', class_='content_title')[0].text.strip()
    #article_text = soup.find_all('div', class_='article_teaser_body')[0].text.strip()
    print(article_title)
    #print(article_text)

    mars_info['article_title'] = article_title

def scrape():
    browser = init_browser()
    mars_info = {}
    
   #Get Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    browser.is_element_present_by_css('ul.item_list li.slide', wait_time=0.75)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Get title and paragraph text. 
    article_title = soup.find_all('div', class_='content_title')[0].get_text()
    article_text = soup.find_all('div', class_='article_teaser_body')
    print(article_title)
    print(article_text)

    mars_info['article_title'] = article_title
    #Visit JPL Images site
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Click button to view full image
    full_img = browser.find_by_id('full_image')
    full_img.click()

    #Click 'More Info' button
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info = browser.find_link_by_partial_text("more info")
    more_info.click()

    #Get image link
    image_url = browser.find_by_tag('img')[6]['src']
    print(image_url)
    
    #featured_image_url = "https://www.jpl.nasa.gov" + str(image_url)
    mars_info["featured_image_url"] = image_url
    #or featured_image_url
   

    #Get Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Space Facts
    url = 'https://space-facts.com/mars/'
    df = pd.read_html(url)[0]
    df.columns =['description', 'value']
    df.set_index('description', inplace=True)
    facts_table = df.to_html()
    mars_info["facts"] = facts_table


    #Visit Astrogeology Website
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    #Use for loop to iterate through 
    #Click each link to get image url
    collapsible = soup.find("div", class_="collapsible results")
    #class = accordian?

    hemispheres = []

    product_links = soup.find('a', class_='itemLink product-item')["href"]
    links = browser.find_by_css('h3')

    #Loop through div containing links
    for i in range(len(links)):
        
        #image_link = url + str(product_links)
        browser.find_by_css('h3')[i].click()
        title = browser.find_by_css('h2.title').text
        title = title.replace("Enhanced", "")
        browser.find_by_text('Sample').click()
        img_url = browser.url
        #find_by_tag('img')['src']


        #Append the dictionary with the image url string and the hemisphere title to a list. 
        #This list will contain one dictionary for each hemisphere.    
        hemis_dict = {"Title": title, "URL": img_url}
        hemispheres.append(hemis_dict)
        browser.windows[0]
        browser.back()

    print(hemispheres)






    return mars_info





