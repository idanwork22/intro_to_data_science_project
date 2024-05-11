import selenium

from src.classes.website_class import AbstractWebsite
from src.classes.logger_class import LoguruLogger

from datetime import datetime, timedelta
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger


class Expedia(AbstractWebsite):
    def __init__(self, url):
        super().__init__(url)
        self.logger = LoguruLogger(__name__).get_logger()
        self.file_name = f"{self.__class__.__name__}_{datetime.now().strftime('%H_%M__%m_%d_%Y')}.csv"

    def remove_register_popup_window(self):
        """
        Remove the popup if exist at the start of the run
        :return: doesn't return anything (None)
        """
        pass

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
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-stid='open-room-picker']"))
            )
            logger.debug("Click - People Button")
            people_button.click()

        except:
            logger.error("People button do not exists")
        time.sleep(0.5)
        adults_current_amount = self.driver_class.driver.find_element(By.ID, 'traveler_selector_adult_step_input-0').get_attribute('value')
        children_current_amount = self.driver_class.driver.find_element(By.ID,
                                                                        'traveler_selector_children_step_input-0').get_attribute('value')

        logger.debug(f"Current Adults amount:{adults_current_amount}")
        logger.debug(f"Current Children amount:{children_current_amount}")

        # adults
        adults_plus_button = self.driver_class.driver.find_element(By.XPATH,
                                                                   '/html/body/div[2]/div[1]/div/div/main/div/div/div/div/div[2]/section[1]/div/div/form/div/div/div[3]/div/div[2]/div/div/section/div[1]/div[1]/div/div/button[2]')
        adults_minus_button = self.driver_class.driver.find_element(By.XPATH,
                                                                    '/html/body/div[2]/div[1]/div/div/main/div/div/div/div/div[2]/section[1]/div/div/form/div/div/div[3]/div/div[2]/div/div/section/div[1]/div[1]/div/div/button[1]')

        # children
        children_plus_button = self.driver_class.driver.find_element(By.XPATH,
                                                                     '/html/body/div[2]/div[1]/div/div/main/div/div/div/div/div[2]/section[1]/div/div/form/div/div/div[3]/div/div[2]/div/div/section/div[1]/div[2]/div[1]/div/button[2]')
        children_minus_button = self.driver_class.driver.find_element(By.XPATH,
                                                                      '/html/body/div[2]/div[1]/div/div/main/div/div/div/div/div[2]/section[1]/div/div/form/div/div/div[3]/div/div[2]/div/div/section/div[1]/div[2]/div[1]/div/button[1]')

        # fixing adults
        while True:
            adults_current_amount = int(
                self.driver_class.driver.find_element(By.ID, 'traveler_selector_adult_step_input-0').get_attribute('value'))
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
            children_current_amount = int(
                self.driver_class.driver.find_element(By.ID, 'traveler_selector_children_step_input-0').get_attribute('value'))
            if children_current_amount < children:
                children_plus_button.click()
                logger.debug("Click - Increase children Button")

            if children_current_amount > children:
                children_minus_button.click()
                logger.debug("Click - Decrease children Button")
            if children_current_amount == children:
                break
        time.sleep(0.5)

        # lets click on save button
        try:
            time.sleep(0.5)
            self.driver_class.driver.find_element(By.XPATH,
                                                  '/html/body/div[2]/div[1]/div/div/main/div/div/div/div/div[2]/section[1]/div/div/form/div/div/div[3]/div/div[2]/div/div/div/div/button').click()
        except:
            logger.error("Problem in Save people button")
        else:
            logger.debug("Click - Save People Button")

    def choose_dates(self, ttt: int, los: int):
        start_date = datetime.now() + timedelta(days=ttt)
        end_date = start_date + timedelta(days=los)
        start_date_str = self.format_date(start_date)
        end_date_str = self.format_date(end_date)
        logger.debug(f"Start Date: {start_date_str}")
        logger.debug(f"End Date: {end_date_str}")
        try:
            time.sleep(0.5)
            date_button = WebDriverWait(self.driver_class.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='uitk-date-selector-input1-default']"))
            )
            logger.debug("Click - Date Button")
            date_button.click()
        except:
            logger.error("Date button do not exists")

        # Click on the dates
        time.sleep(0.5)
        date_clickable_elements = self.driver_class.driver.find_elements(By.CLASS_NAME, "uitk-day-button.uitk-day-selectable.uitk-day-clickable")

        date_dict = {}
        for date_clickable_element in date_clickable_elements:
            date_dict[date_clickable_element.find_element(By.CLASS_NAME, "uitk-day-aria-label").get_attribute('aria-label')] = date_clickable_element

        for date, button in date_dict.items():
            if start_date_str in date:
                button.click()
            if end_date_str in date:
                button.click()

        # lets click on save button
        try:
            time.sleep(0.5)
            date_button = WebDriverWait(self.driver_class.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-stid='apply-date-selector']"))
            )
            date_button.click()
        except:
            logger.error("Problem in Save Dates button")
        else:
            logger.debug("Click - Save Dates Button")

        return start_date_str, end_date_str

    def click_on_search_hotels_button(self):
        try:
            time.sleep(0.5)
            date_button = WebDriverWait(self.driver_class.driver, 5).until(
                EC.element_to_be_clickable((By.ID, "search_button"))
            )
            date_button.click()
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
            for _ in range(1):
                self.driver_class.driver.find_element(By.CLASS_NAME,
                                                      'uitk-button.uitk-button-medium.uitk-button-has-text.uitk-button-secondary').click()
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
        hotels_elements = self.driver_class.driver.find_elements(By.CLASS_NAME, "uitk-layout-flex.uitk-layout-flex-block-size-full-size.uitk-layout-flex-flex-direction-column.uitk-layout-flex-justify-content-space-between")
        logger.info(f"There are {len(hotels_elements)} hotels")
        for hotel_element in hotels_elements:
            # Extract data using the specific class names inside each WebElement
            name = hotel_element.find_element(By.CLASS_NAME, "uitk-heading.uitk-heading-5.overflow-wrap.uitk-layout-grid-item.uitk-layout-grid-item-has-row-start").text
            try:
                rating = hotel_element.find_element(By.CLASS_NAME, "uitk-badge-base-text").text
            except Exception as e:
                logger.error(f"Hotel : {name} doesnt have rating")
                continue
            try:
                price = hotel_element.find_element(By.CLASS_NAME, "uitk-text.uitk-type-end.uitk-type-200.uitk-text-default-theme").text
            except Exception as e:
                logger.error(f"Hotel : {name} doesnt have price")
                continue
            try:
                reviews_amount = hotel_element.find_element(By.CLASS_NAME, "uitk-text.uitk-type-200.uitk-type-regular.uitk-text-default-theme").text
            except Exception as e:
                logger.error(f"Hotel : {name} doesnt have reviews")
                continue
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
                'reviews_amount': reviews_amount,
            })
        return hotels_lst

    @staticmethod
    def format_date(date_object):
        # Format the date as '10 May 2024'
        formatted_date = date_object.strftime('%A, %B %d, %Y')
        return formatted_date
