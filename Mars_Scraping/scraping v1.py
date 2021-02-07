# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
    # Initiate headless driver for deployment
    # Windows users
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }
    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    try:
        PREFIX = "https://web.archive.org/web/20181114023740"
        url = f'{PREFIX}/https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)
        article = browser.find_by_tag('article').first['style']
        article_background = article.split("_/")[1].replace('");',"")
        return f'{PREFIX}_if/{article_background}'
    except:
        return 'https://www.nasa.gov/sites/default/files/styles/full_width_feature/public/thumbnails/image/pia22486-main.jpg'
 

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

# def hemisphere_data(browser): 
#     # 1. Use browser to visit the URL 
#     url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
#     # 2. Create a list to hold the images and titles.
#     hemisphere_image_urls = []

#     # 3. Write code to retrieve the image urls and titles for each hemisphere.
#     # parse site
#     #Cerberus
#     browser.visit(url)
#     browser.links.find_by_partial_text('Cerberus').click()
#     html = browser.html
#     cerberus_soup = soup(html, 'html.parser')
#     cerberus_url = cerberus_soup.select_one('div.downloads a').get("href")
#     cerberus_title = cerberus_soup.select_one('div.content h2').text

#     #dictionary:
#     cerberus_dict = {
#         "img_url": cerberus_url,
#         "title": cerberus_title
#         }

#     hemisphere_image_urls.append(cerberus_dict)

#     #Schiaparelli
#     browser.visit(url)
#     browser.links.find_by_partial_text('Schiaparelli').click()
#     html = browser.html
#     schiaparelli_soup = soup(html, 'html.parser')
#     schiaparelli_url = schiaparelli_soup.select_one('div.downloads a').get("href")
#     schiaparelli_title = schiaparelli_soup.select_one('div.content h2').text

#     #dictionary:
#     schiaparelli_dict = {
#         "img_url": schiaparelli_url,
#         "title": schiaparelli_title
#         }

#     hemisphere_image_urls.append(schiaparelli_dict)

#     #Syrtis
#     browser.visit(url)
#     browser.links.find_by_partial_text('Syrtis').click()
#     html = browser.html
#     syrtis_soup = soup(html, 'html.parser')
#     syrtis_url = syrtis_soup.select_one('div.downloads a').get("href")
#     syrtis_title = syrtis_soup.select_one('div.content h2').text

#     #dictionary:
#     syrtis_dict = {
#         "img_url": syrtis_url,
#         "title": syrtis_title
#         }

#     hemisphere_image_urls.append(syrtis_dict)   

#     #Valles
#     browser.visit(url)
#     browser.links.find_by_partial_text('Valles').click()
#     html = browser.html
#     valles_soup = soup(html, 'html.parser')
#     valles_url = valles_soup.select_one('div.downloads a').get("href")
#     valles_title = valles_soup.select_one('div.content h2').text

#     #dictionary:
#     valles_dict = {
#         "img_url": valles_url,
#         "title": valles_title
#         }

#     hemisphere_image_urls.append(valles_dict)

#     return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())