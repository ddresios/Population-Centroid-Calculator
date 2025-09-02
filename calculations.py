#This will be the file where I implement the calculation methods. 

import math
import numpy as np

#define the list of all the coordinate points I want to check
def create_grid(lat_res: int, lon_res: int) -> list:
    min_lat, max_lat = 24.0, 50.0    
    min_lon, max_lon = -125.0, -66.0 # Create the bounding box roughly the side of Murica

    lat_step = lat_res   
    lon_step = lon_res   # 1 degree longitude

    lats = np.arange(min_lat, max_lat + lat_step, lat_step)
    lons = np.arange(min_lon, max_lon + lon_step, lon_step)

    coordinates = [(lat, lon) for lat in lats for lon in lons]
    return coordinates

def haversine(coord1: tuple, coord2: tuple) -> float: #I just vibe coded the next few methods lol
    """
    Calculate the great-circle distance between two points on the Earth 
    using the haversine formula.
    
    Parameters:
        coord1: Tuple (lat1, lon1) in degrees.
        coord2: Tuple (lat2, lon2) in degrees.
    
    Returns:
        Distance in kilometers as a float.
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Radius of Earth in kilometers
    R = 6371.0  

    # Convert degrees to radians
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    # Haversine formula
    a = math.sin(dphi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance
    distance = R * c
    return distance

def quality_append(coord_grid: list, techer_locations: list) -> list:
    """
    For each coordinate in coord_grid, compute the average haversine distance
    to all teacher locations and return a list of tuples:
    (coordinate, average_distance)
    """
    return [
        (coord, sum(haversine(coord, techer) for techer in techer_locations) / len(techer_locations))
        for coord in coord_grid
    ]

