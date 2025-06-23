# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 16:51:48 2025

@author: Uzair
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from matplotlib.lines import Line2D

# Reading the files
bikeways = gpd.read_file('bikeways.geojson')
washrooms = gpd.read_file('public-washrooms.geojson')

# Reproject to Web Mercator
bikeways_merc = bikeways.to_crs(epsg=3857)
washrooms_merc = washrooms.to_crs(epsg=3857)

# Filter active bikeways
active_bikeways = bikeways_merc[bikeways_merc['status'] == 'Active']

# Create 200m buffer around bikeways
bike_buffer = active_bikeways.buffer(200)
bike_buffer_union = gpd.GeoDataFrame(geometry=[bike_buffer.union_all()], crs=3857)

# Find washrooms within the buffer
washrooms_near_bikes = washrooms_merc[washrooms_merc.geometry.within(bike_buffer_union.geometry[0])]

print(f'Number of Washrooms near bikeways: {len(washrooms_near_bikes)}')

# Plotting
fig, ax = plt.subplots(figsize=(13, 14))

# Active bikeways with color-coded legend
active_bikeways.plot(
    ax=ax,
    column='bikeway_type',
    linewidth=2,
    cmap='tab10',
    legend=True  # Auto legend for bikeway_type
)

# Buffer zone
bike_buffer_union.plot(ax=ax, color='lightblue', alpha=0.4, edgecolor='red')

# Washrooms (outside buffer) with legend label
washrooms_merc.plot(ax=ax, color='orange', markersize=30)

#Washrooms (inside buffer)
washrooms_near_bikes.plot(ax=ax, marker='o', color='green', markersize=60)

#Basemap
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=12)

custom_handles = [
    Line2D([0], [0], marker='o', color='w', label='Public Washrooms (outside buffer)',
           markerfacecolor='orange', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Washrooms (within 200m buffer)',
           markerfacecolor='green', markersize=10)
]
fig.legend(
    handles=custom_handles,
    loc='upper right',
    bbox_to_anchor=(0.25, 0.90),
    frameon=True,
    title='Washrooms')


#Plotting
plt.title("Vancouver Bike Lanes + Washrooms Proximity")
plt.axis('off')
plt.tight_layout()
plt.show()

