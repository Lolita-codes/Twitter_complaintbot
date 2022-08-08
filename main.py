import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv
load_dotenv('.env')


PROMISED_DOWNLOAD = os.environ['PROMISED_DOWNLOAD']
PROMISED_UPLOAD = os.environ['PROMISED_UPLOAD']
TWITTER_EMAIL = os.environ['TWITTER_EMAIL']
TWITTER_PASSWORD = os.environ['TWITTER_PASSWORD']
CHROME_DRIVER_PATH = os.environ['CHROME_DRIVER_PATH']


class InternetSpeedTwitterBot:
    def __init__(self):
        # Creates Selenium driver
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        self.down = 0
        self.up = 0
        self.provider = None

    # Gets the current live download and upload speeds
    def get_internet_speed(self):
        self.driver.get('https://www.speedtest.net/')
        time.sleep(60)
        go = self.driver.find_element(By.CLASS_NAME, 'start-text').click()
        time.sleep(120)
        self.provider = self.driver.find_element(By.CLASS_NAME, 'result-label').text
        self.down = self.driver.find_element(By.CLASS_NAME, 'download-speed').text
        self.up = self.driver.find_element(By.CLASS_NAME, 'upload-speed').text
        print(self.provider)
        print(f'down: {self.down}')
        print(f'up: {self.up}')

    # Automatically log in to Twitter and tweet
    def tweet_at_provider(self):
        if self.up < int(PROMISED_UPLOAD) or self.down < int(PROMISED_DOWNLOAD):
            self.driver.get('https://twitter.com/i/flow/login?resume=true&lang=en')
            time.sleep(10)
            email = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
            email.send_keys(TWITTER_EMAIL)
            next = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div/span/span').click()
            time.sleep(10)
            password = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
            password.send_keys(TWITTER_PASSWORD)
            log_in = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div/div/span/span').click()
            time.sleep(10)
            msg = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div/div/div/div')
            msg.send_keys(f'Hey @{self.provider}, why is my internet speed {self.down}down/{self.up}up when I pay '
                          f'for {PROMISED_DOWNLOAD}down/{PROMISED_UPLOAD}up?')
            tweet = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div/span/span').click()
            time.sleep(5)
        self.driver.quit()


complain = InternetSpeedTwitterBot()
complain.get_internet_speed()
complain.tweet_at_provider()