from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from src.classes.singleton import SingletonMeta


class DriverClass:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0,100000)")
