from src.classes.website_class import AbstractWebsite
from src.classes.logger_class import LoguruLogger

from datetime import datetime, timedelta
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger


class Booking(AbstractWebsite):
    def __init__(self, url):
        super().__init__(url)
        self.logger = LoguruLogger(__name__).get_logger()
        self.file_name = f"{self.__class__.__name__}_{datetime.now().strftime('%H_%M__%m_%d_%Y')}.csv"

    def remove_register_popup_window(self):
        """
        Remove the popup if exist at the start of the run
        :return: doesn't return anything (None)
        """
        try:
            ads_button = WebDriverWait(self.driver_class.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Dismiss sign-in info.']"))
            )
            logger.debug("Register button exists")
            ads_button.click()
        except:
            logger.error("Register button do not exists")

    def choose_people_amount(self, adults: int, children: int, room: int):

        """
        Adapt page to the selected amount of adults, children and rooms
        :param adults: adults amount time int
        :param children: children amount time int
        :param room: room amount time int
        :return: doesn't return anything (None)
        """
        # click on how many people
        try:
            people_button = WebDriverWait(self.driver_class.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='occupancy-config']"))
            )
            logger.debug("Click - People Button")
            people_button.click()

        except:
            logger.error("People button do not exists")
        time.sleep(0.5)
        adults_current_amount, children_current_amount, rooms_current_amount = self.driver_class.driver.find_elements(
            By.CLASS_NAME,
            'd723d73d5f')
        logger.debug(f"Current Adults amount:{adults_current_amount.text}")
        logger.debug(f"Current Children amount:{adults_current_amount.text}")
        logger.debug(f"Current Rooms amount:{adults_current_amount.text}")

        # adults
        adults_plus_button = self.driver_class.driver.find_element(By.XPATH,
                                                                   '/html/body/div[4]/div/div[2]/div/div[1]/div/form/div[1]/div[3]/div/div/div/div/div[1]/div[2]/button[2]')
        adults_minus_button = self.driver_class.driver.find_element(By.XPATH,
                                                                    '/html/body/div[4]/div/div[2]/div/div[1]/div/form/div[1]/div[3]/div/div/div/div/div[1]/div[2]/button[1]')

        # children
        children_plus_button = self.driver_class.driver.find_element(By.XPATH,
                                                                     '/html/body/div[4]/div/div[2]/div/div[1]/div/form/div[1]/div[3]/div/div/div/div/div[2]/div[2]/button[2]')
        children_minus_button = self.driver_class.driver.find_element(By.XPATH,
                                                                      '/html/body/div[4]/div/div[2]/div/div[1]/div/form/div[1]/div[3]/div/div/div/div/div[2]/div[2]/button[1]')

        # rooms
        rooms_plus_button = self.driver_class.driver.find_element(By.XPATH,
                                                                  '/html/body/div[4]/div/div[2]/div/div[1]/div/form/div[1]/div[3]/div/div/div/div/div[3]/div[2]/button[2]')
        rooms_minus_button = self.driver_class.driver.find_element(By.XPATH,
                                                                   '/html/body/div[4]/div/div[2]/div/div[1]/div/form/div[1]/div[3]/div/div/div/div/div[3]/div[2]/button[1]')

        # fixing adults
        while True:
            adults_current_amount = int(self.driver_class.driver.find_elements(By.CLASS_NAME, 'd723d73d5f')[0].text)
            if adults_current_amount < adults:
                adults_plus_button.click()
                logger.debug("Click - Increase adults Button")
            if adults_current_amount > adults:
                adults_minus_button.click()
                logger.debug("Click - Decrease adults Button")
            if adults_current_amount == adults:
                break
        time.sleep(0.5)

        # fixing children
        while True:
            children_current_amount = int(self.driver_class.driver.find_elements(By.CLASS_NAME, 'd723d73d5f')[1].text)
            if children_current_amount < children:
                children_plus_button.click()
                logger.debug("Click - Increase children Button")

            if children_current_amount > children:
                children_minus_button.click()
                logger.debug("Click - Decrease children Button")
            if children_current_amount == children:
                break
        time.sleep(0.5)

        # fixing rooms
        while True:
            room_current_amount = int(self.driver_class.driver.find_elements(By.CLASS_NAME, 'd723d73d5f')[2].text)
            if room_current_amount < room:
                rooms_plus_button.click()
                logger.debug("Click - Increase room Button")
            if room_current_amount > room:
                rooms_minus_button.click()
                logger.debug("Click - Decrease room Button")
            if room_current_amount == room:
                break

        # lets click on save button
        try:
            time.sleep(0.5)
            self.driver_class.driver.find_element(By.XPATH,
                                                  '/html/body/div[4]/div/div[2]/div/div[1]/div/form/div[1]/div[3]/div/div/div/button').click()
        except:
            logger.error("Problem in Save people button")
        else:
            logger.debug("Click - Save People Button")

    def choose_dates(self, ttt: int, los: int):
        start_date = datetime.now() + timedelta(days=ttt)
        end_date = start_date + timedelta(days=los)
        start_date_str = self.format_date(start_date)
        end_date_str = self.format_date(end_date)
        logger.info(f"Start Date: {start_date_str}")
        logger.info(f"End Date: {end_date_str}")
        try:
            time.sleep(0.5)
            date_button = WebDriverWait(self.driver_class.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='date-display-field-start']"))
            )
            logger.debug("Click - Date Button")
            date_button.click()
        except:
            logger.error("Date button do not exists")

        # Click on the dates

        try:
            time.sleep(0.5)
            start_date_button = WebDriverWait(self.driver_class.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, f"//span[@aria-label='{start_date_str}']")))
            logger.debug("Click - Start Date Button")
            start_date_button.click()
            time.sleep(0.2)
            end_date_button = WebDriverWait(self.driver_class.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, f"//span[@aria-label='{end_date_str}']")))
            logger.debug("Click - End Date Button")
            end_date_button.click()
            time.sleep(0.2)

        except:
            logger.error("Start/End Date button does not exists")
        return start_date_str, end_date_str

    def click_on_search_hotels_button(self):
        time.sleep(0.5)
        try:
            self.driver_class.driver.find_element(By.XPATH,
                                                  '/html/body/div[4]/div/div[2]/div/div[1]/div/form/div[1]/div[4]/button').click()
        except:
            logger.error("Problem in Search Hotels button")
        else:
            logger.debug("Click - Search Hotels Button")

    def click_on_load_nore_results(self):
        try:
            time.sleep(1)
            self.driver_class.driver.execute_script("window.scrollTo(0,100000)")
            logger.debug("Script - Scrolling down")
            time.sleep(1)
            self.driver_class.driver.execute_script("window.scrollTo(0,100000)")
            logger.debug("Script - Scrolling down")
            time.sleep(3)
            for _ in range(2):
                self.driver_class.driver.find_element(By.CLASS_NAME,
                                                      'a83ed08757.c21c56c305.bf0537ecb5.f671049264.deab83296e'
                                                      '.af7297d90d').click()
                logger.debug("Click - Load More Results Button")
                time.sleep(2)
        except:
            logger.error("Problem in Load More Results button")
        else:
            logger.debug("Click - Search Hotels Button")

    def collect_hotels_data(self, ttt: int, los: int, start_date_str: str, end_date_str: str, snapshot_number: int):
        hotels_lst = []
        current_url = self.driver_class.driver.current_url
        logger.debug(f"Current URL: {current_url}")
        time.sleep(2)
        hotels_elements = self.driver_class.driver.find_elements(By.CLASS_NAME, "c1edfbabcb")
        logger.info(f"There are {len(hotels_elements)} hotels")
        for hotel_element in hotels_elements:
            # Extract data using the specific class names inside each WebElement
            name = hotel_element.find_element(By.CSS_SELECTOR, "div[data-testid='title']").text
            try:
                rating = hotel_element.find_element(By.CLASS_NAME, "a3b8729ab1.d86cee9b25").text
            except Exception as e:
                logger.error(f"Hotel : {name} doesnt have rating")
                continue
            try:
                price = hotel_element.find_element(By.CLASS_NAME, "f6431b446c.fbfd7c1165.e84eb96b1f").text
            except Exception as e:
                logger.error(f"Hotel : {name} doesnt have price")
                continue
            try:
                reviews_amount = hotel_element.find_element(By.CLASS_NAME, "abf093bdfe.f45d8e4c32.d935416c47").text
            except Exception as e:
                logger.error(f"Hotel : {name} doesnt have reviews amount")
                continue

            # bed_type = hotel_element.find_element(By.CLASS_NAME, "abf093bdfe.e8f7c070a7").text
            # center_distance = hotel_element.find_element(By.CSS_SELECTOR, "span[data-testid='distance']").text
            # Store data in a dictionary and add to the list
            hotels_lst.append({
                "website": self.__class__.__name__,
                "snapshot_number": snapshot_number,
                "snapshot_date": datetime.now().strftime("%d %B %Y"),
                'start_date_str': start_date_str,
                'end_date_str': end_date_str,
                'ttt': ttt,
                'los': los,
                'name': name,
                'rating': rating,
                'price': price,
                'reviews_amount': reviews_amount
                # 'bed_type': bed_type,
                # 'center_distance': center_distance
            })
        return hotels_lst

    @staticmethod
    def format_date(date_object):
        # Format the date as '10 May 2024'
        formatted_date = date_object.strftime('%#d %B %Y')
        return formatted_date
