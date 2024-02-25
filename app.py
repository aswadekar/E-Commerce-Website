from flask import Flask, render_template, request
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
        """ driver.get(f"https://www.croma.com/search/?text={product_name}") """
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

        return render_template('result.html', product=product_name, amazon_price=amazon_price, flipkart_price=flipkart_price, croma_price=croma_price, reliance_price=reliance_price, product_img=product_img)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)