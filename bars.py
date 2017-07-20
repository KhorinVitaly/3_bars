import json
from geopy import Point
from geopy.distance import distance
from sys import argv
from functools import partial


def load_data(filepath):
    with open(filepath, "r", encoding='cp1251') as json_file:
        json_data = json_file.read()
        return json.loads(json_data)


def get_biggest_bar(json_data):
    return max(json_data, key=lambda x: x["SeatsCount"])


def get_smallest_bar(json_data):
    return min(json_data, key=lambda x: x["SeatsCount"])


def get_distance(latitude1, longitude1, latitude2, longitude2):
    point1 = Point(latitude1, longitude1)
    point2 = Point(latitude2, longitude2)
    return distance(point1, point2).km


def check_of_coordinates(latitude, longitude):
    if (latitude > 90 or latitude < -90) or (longitude > 180 or longitude < -180):
        raise ValueError()


def get_closest_bar(json_data, latitude, longitude):
    call_distance = partial(get_distance, latitude, longitude)
    return min(json_data, key=lambda x: call_distance(float(x["Latitude_WGS84"]), float(x["Longitude_WGS84"])))


def print_bar(bar_item):
   bars_name = bar_item["Name"]
   adm_area = bar_item["AdmArea"]
   district = bar_item["District"]
   address = bar_item["Address"]
   phone = bar_item["PublicPhone"][0]["PublicPhone"]

   print('Name: {0}; Address: {1}, {2}, {3}; Phone {4}'.format(bars_name, adm_area, district, address, phone))


def fetch_data():
    try:
        filepath = argv[1]
        json_data = load_data(filepath)
        return json_data
    except FileNotFoundError:
        print("File not found!")
    except IndexError:
        print("File not specified!")
    except json.JSONDecodeError:
        print("File is not JSON!")
    exit()


def intput_coordinates():
    print("Input your current coordinates")
    latitude = float(input("latitude: "))
    longitude = float(input("longitude: "))
    check_of_coordinates(latitude, longitude)
    return latitude, longitude


def print_smallest_biggest_and_closest_bars(json_data, latitude, longitude):
    print("Smallest bar: ", end='')
    print_bar(get_smallest_bar(json_data))
    print("Biggest bar: ", end='')
    print_bar(get_biggest_bar(json_data))
    print("Closest bar: ", end='')
    print_bar(get_closest_bar(json_data, latitude, longitude))


if __name__ == '__main__':
    json_data = fetch_data()
    try:
        latitude, longitude = intput_coordinates()
        print_smallest_biggest_and_closest_bars(json_data, latitude, longitude)
    except TypeError:
        print("File format error!")
    except ValueError:
        print("You entered incorrect values ​​for the coordinates!")

