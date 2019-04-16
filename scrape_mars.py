# import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import time
from selenium import webdriver


def init_browser():
    executable_path = {"executable_path": '/Users/ey/Desktop/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_facts_data = {}

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(2)

    html = browser.html
    soup = bs(html, "html.parser")

    # scrapping latest news about mars from nasa
    news_title = soup.find("div", class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text
    mars_facts_data['news_title'] = news_title
    mars_facts_data['news_paragraph'] = news_paragraph

    # Mars Featured Image
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    browser.is_text_present('FULL IMAGE')
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    html_jpl = browser.html
    soup_jpl = bs(html_jpl, "html.parser")
    featured_image_location = soup_jpl.find(
        "div", class_="fancybox-inner").img["src"].strip()
    base_url = "https://www.jpl.nasa.gov/"
    featured_image_url = base_url + featured_image_location
    featured_image_url
    mars_facts_data["featured_image"] = featured_image_url

    # #### Mars Weather

    # get mars weather's latest tweet from the website
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    html_weather = browser.html
    soup = bs(html_weather, "html.parser")
    mars_weather = soup.find(
        "p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_weather_text = mars_weather.replace('\n', ' ').split('pic')[0]
    mars_facts_data["mars_weather"] = mars_weather_text

    # #### Mars Facts

    url_facts = "https://space-facts.com/mars/"
    time.sleep(2)
    tables = pd.read_html(url_facts)
    tables[0]
    df = tables[0]
    df.columns = ['Description', 'Values']
    html_table = df.to_html()
    html_table.replace('\n', '')
    mars_facts_data["mars_facts_table"] = html_table

 # Mars Hemispheres
# Visit the USGS Astrogeology site
    url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemisphere)
    html_hemisphere = browser.html
    soup_hemisphere = bs(html_hemisphere, "html.parser")
    # mars_hemisphere = soup_hemisphere.find("div", class_="item").text
    hemisphere_titles = soup_hemisphere.find_all('div', class_='item')
    hemisphere_images = []
# loop over hemispheres and save the titles and image links
    for item in hemisphere_titles:
        main_url = "https://astrogeology.usgs.gov"
        url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url_hemisphere)
        title = item.find("h3").text
        # navigate to specific hemisphere page
        browser.click_link_by_partial_text(title)
        time.sleep(2)
        html_hemisphere = browser.html
        soup_hemisphere = bs(html_hemisphere, "html.parser")

    # construct link to hemisphere image
        # print(soup_hemisphere)
        partial_img_url = soup_hemisphere.find(
            'img', class_='wide-image')['src']
        # x = soup_hemisphere.find(
        # 'img', class_ = 'wide-image')
        img_url = main_url + partial_img_url
        # print(f"full img url: {img_url}")

    # append hemisphere title and image url to list
        hemisphere_images.append({"title": title, "img_url": img_url})
        mars_facts_data["hemisphere_images"] = hemisphere_images

    browser.quit()
    return mars_facts_data


# if __name__ == "__main__":
#     mydictionary = scrape()
#     print(mydictionary)
