from src.classes.manager_class import ManagerClass


def main():
    manager = ManagerClass(snapshot_number=5)

    # manager.extract_data_from_booking(booking_url='https://www.booking.com/searchresults.html?city=20088325',
    #                                   time_to_travel=30,
    #                                   length_of_stay=5,
    #                                   adults=2,
    #                                   children=0,
    #                                   room=1)

    manager.extract_data_from_expedia(expedia_url='https://www.expedia.com/Hotel-Search?destination=New%20York',
                                      time_to_travel=30,
                                      length_of_stay=5,
                                      adults=2,
                                      children=0,
                                      room=1)

if __name__ == '__main__':
    main()
