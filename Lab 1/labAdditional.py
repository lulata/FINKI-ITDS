from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import matplotlib.pyplot as plt
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

browser = webdriver.Chrome(options=options)

url = 'https://finance.yahoo.com/crypto'
browser.get(url)

time.sleep(3)

cryptos = browser.find_elements(By.CSS_SELECTOR, 'tr.yf-paf8n5')
data = []

for crypto in cryptos:
    try:
        name = crypto.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text
        price = crypto.find_element(By.CSS_SELECTOR, 'td:nth-child(4)').text.replace(',', '')
        market_cap = crypto.find_element(By.CSS_SELECTOR, 'td:nth-child(7)').text.replace(',', '')

        if price.endswith('T'):
            price = float(price[:-1]) * 1e12  
        elif price.endswith('B'):
            price = float(price[:-1]) * 1e9   
        elif price.endswith('M'):
            price = float(price[:-1]) * 1e6   
        else:
            price = float(price)

        if market_cap.endswith('T'):
            market_cap = float(market_cap[:-1]) * 1e12 
        elif market_cap.endswith('B'):
            market_cap = float(market_cap[:-1]) * 1e9   
        else:
            market_cap = float(market_cap)  

        print(f"Name: {name}, Price: {price}, Market Cap: {market_cap}")
        data.append({
            'Name': name,
            'Price': price,
            'Market Cap': market_cap
        })
    except Exception as e:
        print(f"Error parsing crypto row: {e}")

browser.quit()

df = pd.DataFrame(data)



plt.figure(figsize=(10, 5))
plt.hist(df['Price'], bins=30, color='blue', edgecolor='black')
plt.title('Distribution of Cryptocurrency Prices')
plt.xlabel('Price (USD)')
plt.ylabel('Frequency')
plt.show()

