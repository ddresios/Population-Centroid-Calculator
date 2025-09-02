#This will be the main runner file
from calculations import haversine
import csv
import calculations
import matplotlib.pyplot as plt
import numpy as np

import cartopy.crs as ccrs
import cartopy.feature as cfeature


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



def plot_quality_heatmap_us(quality_list: list, locations_list: list, grid_size: int = 100):
    """
    Plots a heatmap of quality values over the USA.
    
    Parameters:
        quality_list: List of tuples ((lat, lon), quality)
        grid_size: Resolution of the heatmap
    """
    # Extract coordinates and qualities
    lats = [coord[0][0] for coord in quality_list]
    lons = [coord[0][1] for coord in quality_list]
    qualities = [coord[1] for coord in quality_list]

    # Create grid
    lat_min, lat_max = min(lats), max(lats)
    lon_min, lon_max = min(lons), max(lons)
    
    lat_grid = np.linspace(lat_min, lat_max, grid_size)
    lon_grid = np.linspace(lon_min, lon_max, grid_size)
    
    # Fill heatmap (nearest neighbor)
    heatmap = np.zeros((grid_size, grid_size))
    for i, lat in enumerate(lat_grid):
        for j, lon in enumerate(lon_grid):
            distances = [(abs(lat - lats[k]) + abs(lon - lons[k]), k) for k in range(len(lats))]
            _, idx = min(distances)
            heatmap[i, j] = qualities[idx]
    
    central_idx = np.argmin(qualities)
    central_coord = (lats[central_idx], lons[central_idx])

    # Plot with Cartopy
    fig = plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())

    # Overlay heatmap
    extent = [lon_min, lon_max, lat_min, lat_max]
    im = ax.imshow(heatmap, extent=extent, origin='lower', cmap='hot', alpha=0.6)

    # Add USA features
    ax.add_feature(cfeature.STATES, edgecolor='black')
    ax.add_feature(cfeature.BORDERS, edgecolor='black')
    ax.coastlines()

    # Plot blue dots for locations_list
    if locations_list:
        loc_lats = [coord[0] for coord in locations_list]
        loc_lons = [coord[1] for coord in locations_list]
        ax.scatter(loc_lons, loc_lats, color='blue', s=20, label='Locations', zorder=5)

    #Plot the central location
    ax.scatter(central_coord[1], central_coord[0], color='green', s=100, marker='o', label='Central Location', zorder=6)

    
    # Colorbar
    plt.colorbar(im, ax=ax, label='Average distance to 2029 techers (km)')
    plt.title('Average distance heatmap')
    plt.show()


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

    #output heatmap 
    plot_quality_heatmap_us(quality_appended_list, techer_locations, 100)
    

if __name__ == "__main__":
        main()