# imports
from splinter import Browser
from bs4 import BeautifulSoup as Soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape():


    # splinter setup
    executablepath = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executablepath, headless=False)


    # NASA MARS NEWS
    #visit the url for the mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Create a beautiful soup object
    html = browser.html
    news_soup = Soup(html, 'html.parser')

    element = news_soup.select_one('div.list_text')
    print(element)

    News_title = element.find('div', class_='content_title').get_text()
    news_paragraph = element.find('div', class_='article_teaser_body').get_text()



    # JPL SPACE IMAGES
    # Visit the url for the spaces images from JPL
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Create a beautiful soup object
    html = browser.html
    news_soup = Soup(html, 'html.parser')

    # Find the image button
    imageElement = browser.find_by_tag('button')[1]

    # Click the button in the browser
    imageElement.click()

    # After clicking create another bs object
    # Create a beautiful soup object
    html = browser.html
    image_soup = Soup(html, 'html.parser')

    image_url = image_soup.find('img', class_='fancybox-image').get('src')
    print(image_url)

    img_url = f"{url}{image_url}"
    print(img_url)


    # MARS FACT PAGE
    df = pd.read_html('https://galaxyfacts-mars.com/')[0]
    df

    # re-configure the dataframe
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    df

    df.to_html()


    # MARS HEMISPHERE PICS
    #visit the url for the hemisphere images from the site
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    html = browser.html

    # Create a list to hold the images and the titles for the hemispheres
    hemisphereImageUrls = []

    links = browser.find_by_css('a.product-item img')

    for link in range(len(links)):
        hemi_dict = {}
        
        #click the picture
        browser.find_by_css('a.product-item img')[link].click()
        
        #find the text marked 'Sample' in the product page
        sample = browser.links.find_by_text('Sample').first
        
        # Find the href to the sample
        hemi_dict['img_url'] = sample['href']
            
        # Grab the headings and store as the title
        hemi_dict['title'] = browser.find_by_css('h2.title').text
        
        #append the dictionary to the list of URLs
        hemisphereImageUrls.append(hemi_dict)
        
        #go back to the main hemisphere page
        browser.back()

    # hemisphereImageUrls
    browser.quit()

    # Create final dictionary to load to mongoDB
    mars_data = {'news_title': News_title,
                'news_paragraph': news_paragraph,
                'img_url': img_url,
                'df': df,
                'hemisphereImageUrls': hemisphereImageUrls}

    return mars_data

