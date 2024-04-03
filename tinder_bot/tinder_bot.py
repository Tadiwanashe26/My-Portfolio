from selenium import webdriver


class TinderBot:
    def __init__(self):
        self.driver = webdriver.Chrome('/mnt/c/WebDriver')
        
    def open_driver(self):
        self.driver.get('https://tinder.com/')

        

