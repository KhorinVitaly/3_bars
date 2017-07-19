import json
from geopy import Point
from geopy.distance import distance
from sys import argv


def load_data(filepath):
    with open(filepath, "r", encoding='utf-8') as json_file:
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
    # Есть сомнения на сколько строка ниже читаема, но зато нет цикла, есть лишь один вызов функции min
    return min(json_data, key=lambda x: get_distance(latitude, longitude, float(x["Latitude_WGS84"]),
                                                float(x["Longitude_WGS84"])))


def print_bar(bar_item):
    print(bar_item["Name"] + "; Address: " + bar_item["AdmArea"] + ", " + bar_item["District"] + ", "
          + bar_item["Address"] + "; Public phone: " + bar_item["PublicPhone"][0]["PublicPhone"])


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


def print_smallest_biggest_and_closest_bars(json_data):
    print("Smallest bar: ", end='')
    print_bar(get_smallest_bar(json_data))
    print("Biggest bar: ", end='')
    print_bar(get_biggest_bar(json_data))

    print("Input your current coordinates")
    latitude = float(input("latitude: "))
    longitude = float(input("longitude: "))
    check_of_coordinates(latitude, longitude)
    print("Closest bar: ", end='')
    print_bar(get_closest_bar(json_data, latitude, longitude))


if __name__ == '__main__':
    json_data = fetch_data()
    try:
        print_smallest_biggest_and_closest_bars(json_data)
    except TypeError:
        print("File format error!")
    except ValueError:
        print("You entered incorrect values ​​for the coordinates!")

