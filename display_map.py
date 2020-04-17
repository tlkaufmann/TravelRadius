import folium
import json
import pickle
import numpy as np
import matplotlib.pyplot as plt

with open('API_KEY.txt', 'r') as f:
    API_KEY = f.read()

all_times = pickle.load(open('data/all_times_processed.p', 'rb'))
with open('configs.json', 'r') as f:
    configs = json.load(f)
home_coords = tuple(configs['home_coords'])
grid_size = configs['grid_size']
max_extent = configs['max_extent']
display_sizes = configs['display_sizes']

# create grid
grid_size = grid_size + grid_size % 5
lats = home_coords[0] + np.linspace(-max_extent, max_extent, grid_size)
longs = home_coords[1] + np.linspace(-max_extent, max_extent, grid_size)

longs = longs[int(grid_size/2*(1-display_sizes[1])):int(grid_size/2*(1+display_sizes[1]))]
lats = lats[int(grid_size/2*(1-display_sizes[0])):int(grid_size/2*(1+display_sizes[0]))]


# Create map
fmap = folium.Map(location=home_coords, zoom_start=15, max_zoom=18, min_zoom=12,
                  # tiles="Stamen Terrain",
                  # tiles = "Stamen Toner",
                  name = 'Map'
                  )

folium.Marker(home_coords, popup='Home',
              icon=folium.Icon(color='red',icon='home', prefix='fa') ).add_to(fmap)

# ImageOverlay
for mode in all_times:

    folium.raster_layers.ImageOverlay(
        image=all_times[mode].T / np.max(all_times[mode]),
        name=mode,
        bounds=[[min(lats), min(longs)], [max(lats), max(longs)]],
        opacity=0.75,
        pixelated=False,
        colormap=plt.get_cmap('viridis'),
        show=mode=='transit',
        zindex=1
    ).add_to(fmap)

# Save map
folium.LayerControl(collapsed=False).add_to(fmap)
fmap.save('index.html')
