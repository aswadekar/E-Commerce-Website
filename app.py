""" from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_name = request.form['product']
        # Use Selenium to scrape Amazon
        driver = webdriver.Chrome()
        driver.get(f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        amazon_price = soup.find('span', {'class': 'a-price-whole'})
        amazon_price = amazon_price.text.strip() if amazon_price else None
        driver.quit()

        # Use BeautifulSoup to scrape Flipkart and Croma (you'll need to implement these)
        # flipkart_price = ...
        driver = webdriver.Chrome()
        driver.get(f"https://www.flipkart.com/search?q={product_name.replace(' ', '%20')}")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        flipkart_price = soup.find('div', {'class': '_30jeq3 _1_WHN1'})
        flipkart_price = flipkart_price.text.strip() if flipkart_price else None
        driver.quit()
        
        # croma_price = ...
        driver = webdriver.Chrome()
        driver.get(f"https://www.croma.com/searchB?q={product_name.replace(' ', '%20')}%3Arelevance&text={product_name.replace(' ', '%20')}")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        croma_price = soup.find('span', {'class': 'amount plp-srp-new-amount'})
        croma_price = croma_price.text.strip() if croma_price else None
        driver.quit()
        
        #Reliance
        driver = webdriver.Chrome()
        driver.get(f"https://www.reliancedigital.in/{product_name.replace(' ', '-')}")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        reliance_price = soup.find('span', {'class': 'TextWeb__Text-sc-1cyx778-0 kFBgPo'})
        reliance_price = reliance_price.text.strip() if reliance_price else None
        driver.quit()
        
        product_img = f"https://fdn2.gsmarena.com/vv/bigpic/{product_name.replace(' ', '-')}.jpg"
        alternate_img = f"https://cdn-icons-png.flaticon.com/512/2748/2748558.png"

        return render_template('result.html', product=product_name, amazon_price=amazon_price, flipkart_price=flipkart_price, croma_price=croma_price, reliance_price=reliance_price, product_img=product_img, alternate_img=alternate_img)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True) """
    
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_name = request.form['product']
        # Use Selenium to scrape Amazon
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        response = requests.get(f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}", headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        amazon_price = soup.find('span', {'class': 'a-price-whole'})
        amazon_price = amazon_price.text.strip() if amazon_price else None
        amazon_product_link = soup.find('a', {'class': 'a-link-normal s-no-hover'})
        amazon_link = amazon_product_link['href'] if amazon_product_link else None
        amazon_link = f"https://www.amazon.in{amazon_link}" if amazon_link else None
        

        # Use BeautifulSoup to scrape Flipkart and Croma (you'll need to implement these)
        # flipkart_price = ...
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        response = requests.get(f"https://www.flipkart.com/search?q={product_name.replace(' ', '%20')}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off", headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        flipkart_price = soup.find('div', {'class': '_30jeq3'})
        flipkart_price = flipkart_price.text.strip() if flipkart_price else None
        flipkart_product_link = soup.find('a', {'class': '_1fQZEK'})
        flipkart_link = flipkart_product_link['href'] if flipkart_product_link else None
        flipkart_link = f"https://www.flipkart.com{flipkart_link}" if flipkart_link else None
        flipkart_image = soup.find('img', {'class': '_396cs4'})
        flipkart_image_src = flipkart_image['src'] if flipkart_image else None
        flipkart_highlights = soup.find('ul', {'class': '_1xgFaf'}).text.strip() if soup.find('ul', {'class': '_1xgFaf'}) else None
        
        
        # croma_price = ...
        """ headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        response = requests.get(f"https://www.croma.com/searchB?q={product_name.replace(' ', '%20')}%3Arelevance&text={product_name.replace(' ', '%20')}", headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        price_element = soup.find('div', class_='price')
        croma_price = price_element.text if price_element else None
        croma_link = soup.find('a', class_='product__list--name')
        croma_link = croma_link['href'] if croma_link else None
        croma_link = f"https://www.croma.com{croma_link}" if croma_link else None """
        
        croma_price = None
        croma_link = None
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
            response = requests.get(f"https://www.smartprix.com/search.php?term={product_name.replace(' ', '+')}", headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            croma_price_tag = soup.find('a', {'href': '/croma-products-online-store'})
            if croma_price_tag:
                croma_price_container = croma_price_tag.find_next('div', {'class': 'f-heading'})
                if croma_price_container:
                    croma_price = croma_price_container.text.strip()
                    croma_link = f"https://www.smartprix.com{croma_price_tag['href']}"
        except Exception as e:
            print(f"Error scraping Croma: {str(e)}")
        
        
        #Reliance
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        response = requests.get(f"https://www.reliancedigital.in/{product_name.replace(' ', '-')}", headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        reliance_price = soup.find('span', {'class': 'TextWeb__Text-sc-1cyx778-0 gimCrs'})
        reliance_price = reliance_price.text.strip() if reliance_price else None
        
        product_img = None
        if product_img:
            product_img = f"https://fdn2.gsmarena.com/vv/bigpic/{product_name.replace(' ', '-')}.jpg" 
        else:
            product_img = f"https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg"
        
        alternate_img = f"https://cdn-icons-png.flaticon.com/512/2748/2748558.png"

        return render_template('result.html', product=product_name.capitalize(), amazon_price=amazon_price, amazon_link=amazon_link, flipkart_price=flipkart_price, flipkart_link=flipkart_link, flipkart_img=flipkart_image_src, flipkart_highlights=flipkart_highlights, croma_price=croma_price, croma_link=croma_link, reliance_price=reliance_price, product_img=product_img, alternate_img=alternate_img)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
