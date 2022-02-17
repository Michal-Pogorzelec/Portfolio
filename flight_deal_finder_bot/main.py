from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
import smtplib
import os

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()

ORIGIN_CITY_IATA = "KRK"

if sheet_data[0]["iataCode"] == "":
    flight_search = FlightSearch()
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    print(sheet_data)

    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=6 * 30)

for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )

try:
    if flight.price < destination["lowestPrice"]:
        my_email = os.environ.get('MY_EMAIL')
        password = os.environ.get('PASSWORD')
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email,
                                to_addrs="some_email@gmail.com",
                                msg=f"Low price alert! Only EUR{flight.price} to fly from Krakow-{flight.origin_airport}"
                                    f" to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} "
                                    f"to {flight.return_date}.")
except AttributeError as mess:
    print(f"{mess}")