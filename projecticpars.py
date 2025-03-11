from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import requests

# Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = 'your_telegram_bot_token'
TELEGRAM_CHAT_ID = 'your_telegram_chat_id'

# URL of the crypto exchange site
URL = 'https://www.example.com/crypto-exchange'

# Path to the ChromeDriver executable
CHROMEDRIVER_PATH = '/path/to/chromedriver'

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    requests.post(url, data=payload)

def get_crypto_data():
    # Set up Selenium WebDriver
    service = Service(CHROMEDRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)
    
    # Load the page
    driver.get(URL)
    
    # Wait for the page to load
    driver.implicitly_wait(10)
    
    # Get the page source and parse it with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Close the WebDriver
    driver.quit()
    
    # Extract the desired data (example: extracting the price of Bitcoin)
    bitcoin_price = soup.find('div', {'class': 'bitcoin-price'}).text.strip()
    
    return bitcoin_price

if __name__ == '__main__':
    crypto_data = get_crypto_data()
    message = f'Current Bitcoin price: {crypto_data}'
    send_telegram_message(message)