import json, csv
from functools import reduce
from collections import Counter

def read_json(file):
    with open(file, "r") as f:
        data = json.load(f)
    return data

def add_flight_number_to_passenger(passenger, flight_number):
    passenger["flight_number"] = flight_number
    return passenger

def add_flight_number_to_passengers(flight):
    flight_number = flight["flight_number"]
    passengers = flight["passengers"]
    transformed_passengers = list(map(lambda p: add_flight_number_to_passenger(p, flight_number), passengers))
    flight["passengers"] = transformed_passengers
    return flight

def read_csv(file_path):
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)

def get_city(flight, airports, origin=None):
    code = flight["origin"] if origin else flight["destination"]
    for airport in airports:
        if airport["code"] == code:
            return airport["city"]
    return "Unknown"

def add_city_names_to_flights(flights, airports):
    return list(map(lambda flight: {
        **flight,
        "origin_city":  get_city(flight, airports, origin=True),
        "destination_city": get_city(flight, airports, origin=False)
    }, flights))

def get_top_departure_cities(flights, top_n=5):
    departure_counts = Counter(flight["origin_city"] for flight in flights)
    return departure_counts.most_common(top_n)

if __name__ == '__main__':
    data = read_json("resources/flights.json")

    # print the number of flights in the input file
    print(len(data["flights"]))

    # Get the flights
    flights = data["flights"]

    # add the flight_number information in the passenger dictionary and build the passenger table
    data_with_flight_number_in_passenger = list(map(add_flight_number_to_passengers, flights))

    print("Raw dataset with enriched passengers", data_with_flight_number_in_passenger[0])

    # Create the passenger dataset
    passengers = list(map(lambda f: f["passengers"], data_with_flight_number_in_passenger))

    # flatten the map
    passengers_flatten = reduce(lambda acc, curr: acc + curr, passengers)
    print("Element in passenger dataset", passengers_flatten[1])

    # Create the flight dataset
    flights = data_with_flight_number_in_passenger
    print("Element in flight Dataset", flights[0])

    # read the airport file
    airports = read_csv("resources/airports.csv")
    # Print the 10 first elements of the airports dataset
    print("airports", airports[0:10])

    # In flight dataset, add 2 new columns with origin and destination converted into real city names
    updated_flights = add_city_names_to_flights(flights, airports)
    print("Flight updated with cities", updated_flights[0:5])

    # cities with the most outgoing flights
    top_10_departure_cities = get_top_departure_cities(updated_flights, 10)
    print(top_10_departure_cities)
