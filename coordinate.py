#I had chatgpt make me a quick script that can convert a JSON file to a csv

import csv
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

# Input and output files
input_file = "locations_only.json"   # your file containing cities like "El Paso, Texas",
output_file = "cities_with_coords.csv"

# Initialize geolocator
geolocator = Nominatim(user_agent="city_coord_app")

def get_coordinates(city_name):
    try:
        location = geolocator.geocode(city_name, timeout=10)
        if location:
            return location.latitude, location.longitude
    except GeocoderTimedOut:
        return None, None
    return None, None

# Read city names
with open(input_file, "r") as f:
    cities = [line.strip().strip('"').strip(',') for line in f if line.strip()]

# Prepare CSV
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["city", "latitude", "longitude"])
    
    for city in cities:
        lat, lon = get_coordinates(city)
        if lat is not None and lon is not None:
            writer.writerow([city, lat, lon])
        else:
            writer.writerow(f"Could not find coordinates for: {city}")
        time.sleep(1)  # avoid hitting rate limits

print(f"Done! Output saved to {output_file}")
