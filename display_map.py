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

# longs = longs[int(grid_size/2*(1-display_sizes[1])):int(grid_size/2*(1+display_sizes[1]))]
# lats = lats[int(grid_size/2*(1-display_sizes[0])):int(grid_size/2*(1+display_sizes[0]))]

#########################
# FOLIUM
#########################

fmap = folium.Map(location=home_coords, zoom_start=15, max_zoom=18, min_zoom=12,
                  # tiles="Stamen Terrain",
                  # tiles = "Stamen Toner",
                  name = 'Map'
                  )

folium.Marker(home_coords, popup='Home',
              icon=folium.Icon(color='red',icon='home', prefix='fa') ).add_to(fmap)

#########################
# FOLIUM ImageOverlay
#########################

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


#########################
# FOLIUM zones
#########################
# spacing = 10
#
# cmap = cm.linear.RdYlGn_11.scale(np.min(all_times[mode]), np.max(all_times[mode]))
# map_time = np.max(all_times[mode])
#
#
# url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
# state_geo = f'{url}/us-states.json'
# state_unemployment = f'{url}/US_Unemployment_Oct2012.csv'
# state_data = pd.read_csv(state_unemployment)
#
# with open('test.json') as f:
#   test = json.load(f)
#
# geos = []
# time_data = {}
# spacing_lat = lats[1] - lats[0]
# spacing_long = longs[1] - longs[0]
#
# for i, (dest, time) in enumerate(zip(destinations, all_times[mode].flatten())):
#     cur_polygon = np.array(dest) + np.array([[0, 0], [0, spacing_lat], [spacing_long, spacing_lat], [spacing_long, 0], [0, 0]])
#
#     time_data[i] = {'id': str(i) ,'time': time}
#
#     poly = {
#         'type': 'Feature',
#         'id': str(i),
#         'properties': {'name': str(i)},
#         'geometry': {'type': 'Polygon',
#                      'coordinates': [[[edge[1], edge[0]] for edge in cur_polygon]]
#                      }
#     }
#     geos.append(poly)
# time_data = pd.DataFrame(time_data).T
# geometries = {
#     'type': 'FeatureCollection',
#     'features': geos,
# }
# json.dump(geometries, open('geometries.json', 'w'))
#
# folium.Choropleth(
#     geo_data={},
#     name='test',
#     data=all_times,
#     columns=['id', 'time'],
#     key_on='feature.id',
#     fill_color='YlOrRd',
#     fill_opacity=0.5,
#     line_opacity=0.0,
#     legend_name='Time (min)',
#     smooth_factor=1.0
# ).add_to(fmap)


#########################
# FOLIUM Save
#########################
folium.LayerControl(collapsed=False).add_to(fmap)
fmap.save('index.html')
