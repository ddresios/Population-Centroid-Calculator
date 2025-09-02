#This will be the main runner file
from calculations import haversine
import csv
import calculations

import csv

import csv

def read_coordinates_from_csv(file_path: str) -> list[tuple[float, float]]:
    """
    Reads a CSV file where rows are like: "City, State", latitude, longitude
    Returns a list of (latitude, longitude) tuples
    """
    coordinates = []

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) < 3:
                continue  # skip incomplete rows
            try:
                lat = float(row[1].strip())
                lon = float(row[2].strip())
                coordinates.append((lat, lon))
            except ValueError:
                continue  # skip rows with invalid numbers
    return coordinates


def find_best_coordinate(quality_appended_list: list) -> tuple:
     return min(quality_appended_list, key = lambda x: x[-1])


def main():
    #first load the techer locations
    techer_locations = read_coordinates_from_csv("cities_with_coords.csv")
    
    
    #then generate a grid of US coordinates (this will be used for visualization later)
    coordinate_grid = calculations.create_grid(1, 1)

    #Create a new list that assigns a value to each coordinate
    quality_appended_list = calculations.quality_append(coordinate_grid, techer_locations)

    #Print out the best location:
    best_location = find_best_coordinate(quality_appended_list)
    print("Average techer coordinates: " + str(best_location[0]) + " Average techer distance: " + str(best_location[1]) + " km" )
    

if __name__ == "__main__":
        main()