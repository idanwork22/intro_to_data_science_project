import time
import pandas as pd

from src.classes.booking_class import Booking
from src.classes.expedia_class import Expedia
from src.classes.logger_class import LoguruLogger
from src.classes.website_class import AbstractWebsite


class ManagerClass:
    def __init__(self, snapshot_number: int):
        self.logger = LoguruLogger(__name__).get_logger()
        self.snapshot_number = snapshot_number

    def extract_data_from_booking(self, booking_url, time_to_travel: int, length_of_stay: int,
                                  adults: int, children: int, room: int):
        self.logger.info(f"Start Extract data from: {booking_url}")
        booking_class = Booking(url=booking_url)

        self.extract_general_data(website_instance=booking_class,
                                  time_to_travel=time_to_travel,
                                  length_of_stay=length_of_stay,
                                  adults=adults,
                                  children=children,
                                  room=room)
        booking_class.driver_class.driver.quit()

    def extract_data_from_expedia(self, expedia_url, time_to_travel: int, length_of_stay: int,
                                  adults: int, children: int, room: int):
        self.logger.info(f"Start Extract data from: {expedia_url}")
        expedia_class = Expedia(url=expedia_url)

        self.extract_general_data(website_instance=expedia_class,
                                  time_to_travel=time_to_travel,
                                  length_of_stay=length_of_stay,
                                  adults=adults,
                                  children=children,
                                  room=room)
        expedia_class.driver_class.driver.quit()

    def extract_general_data(self, website_instance: AbstractWebsite, time_to_travel: int, length_of_stay: int,
                             adults: int, children: int, room: int):

        self.logger.debug(f"Getting website data from: {website_instance.url}")
        website_instance.driver_class.driver.get(website_instance.url)

        self.logger.debug("Removing popup")
        website_instance.remove_register_popup_window()
        time.sleep(0.5)

        self.logger.debug("Choosing people amount")
        # website_instance.choose_people_amount(adults=adults,
        #                                       children=children,
        #                                       room=room)

        self.logger.debug("Calling to main iterator ")
        result = self.main_iterator_runner(website_instance=website_instance,
                                           time_to_travel=time_to_travel,
                                           length_of_stay=length_of_stay)

        # save result
        self.save_results(file_name=website_instance.file_name,
                          lst_of_results=result)

    @staticmethod
    def save_results(file_name, lst_of_results):
        df = pd.DataFrame(lst_of_results)
        df.to_csv(file_name, index=False)

    def main_iterator_runner(self, website_instance: AbstractWebsite, time_to_travel: int, length_of_stay: int):
        interator_counter = 1
        for current_ttt in range(1, time_to_travel + 1):
            for current_los in range(1, length_of_stay + 1):
                self.logger.info(f"Iteration number: {interator_counter}: TTT of {current_ttt}, LOS of {current_los}")
                start_date_str, end_date_str = website_instance.choose_dates(ttt=current_ttt, los=current_los)
                website_instance.click_on_search_hotels_button()
                website_instance.click_on_load_nore_results()
                hotels_current_data = website_instance.collect_hotels_data(ttt=current_ttt, los=current_los,
                                                                           start_date_str=start_date_str,
                                                                           end_date_str=end_date_str,
                                                                           snapshot_number=self.snapshot_number)
                website_instance.data += hotels_current_data
                self.logger.debug(f"Finishing running on: TTT of {current_ttt}, LOS of {current_los}")
                interator_counter += 1
            interator_counter +=1
        return website_instance.data
