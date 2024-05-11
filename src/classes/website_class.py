from abc import ABC, abstractmethod
from src.classes.driver_class import DriverClass


class AbstractWebsite(ABC):
    def __init__(self, url):
        self.driver_class = DriverClass()
        self.url = url
        self.data = []

    @abstractmethod
    def remove_register_popup_window(self):
        """Remove the popup if exist at the start of the run"""
        pass

    @abstractmethod
    def choose_people_amount(self, adults: int, children: int, room: int):
        """
        Adapt page to the selected amount of adults, children and rooms
        :param adults: adults amount time int
        :param children: children amount time int
        :param room: room amount time int
        :return: doesn't return anything (None)
        """
        pass

    @abstractmethod
    def choose_dates(self, ttt: int, los: int):
        """
        Choosing date to travel
        :param ttt: the difference between the search date on the website to the checkin date
        :param los: the number of nights that we want to stay in the hotel
        :return:
        """

    @abstractmethod
    def click_on_search_hotels_button(self):
        """
        Click on search button to get result
        :return:
        """
        pass

    @abstractmethod
    def click_on_load_nore_results(self):
        """
        scroll down couple times and click on load more result
        button - also couple times :)
        :return:
        """
        pass

    @abstractmethod
    def collect_hotels_data(self, ttt: int, los: int, start_date_str: str, end_date_str: str, snapshot_number: int):
        """
        collect hotels data by find the list of the hotels elements
        and extract all the relevant data from that element
        :param snapshot_number: snapshot number
        :param ttt: the difference between the search date on the website to the checkin date
        :param los: the number of nights that we want to stay in the hotel
        :param start_date_str: the date of the first day in the hotel
        :param  end_date_str:  the date of the last day in the hotel
        :return:
        """
