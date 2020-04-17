import folium
import json
import pickle
import numpy as np
import matplotlib.pyplot as plt
import branca
from branca.element import MacroElement
from jinja2 import Template

class BindColormap(MacroElement):
    """Binds a colormap to a given layer.
    Copied from https://nbviewer.jupyter.org/gist/BibMartin/f153aa957ddc5fadc64929abdee9ff2e

    Parameters
    ----------
    colormap : branca.colormap.ColorMap
        The colormap to bind.
    """
    def __init__(self, layer, colormap):
        super(BindColormap, self).__init__()
        self.layer = layer
        self.colormap = colormap
        self._template = Template(u"""
        {% macro script(this, kwargs) %}
            {{this.colormap.get_name()}}.svg[0][0].style.display = 'block';
            {{this._parent.get_name()}}.on('overlayadd', function (eventLayer) {
                if (eventLayer.layer == {{this.layer.get_name()}}) {
                    {{this.colormap.get_name()}}.svg[0][0].style.display = 'block';
                }});
            {{this._parent.get_name()}}.on('overlayremove', function (eventLayer) {
                if (eventLayer.layer == {{this.layer.get_name()}}) {
                    {{this.colormap.get_name()}}.svg[0][0].style.display = 'none';
                }});
        {% endmacro %}
        """)  # noqa


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


# ImageOverlay
heatmaps, colormaps = [], []
for mode in all_times:
    current_max = np.max(all_times[mode])

    current_heatmap = folium.raster_layers.ImageOverlay(image=all_times[mode].T / current_max,
                                                        name=mode,
                                                        bounds=[[min(lats), min(longs)], [max(lats), max(longs)]],
                                                        opacity=0.75,
                                                        pixelated=False,
                                                        colormap=plt.get_cmap('viridis'),
                                                        zindex=1,
                                                        show=mode=='transit')
    heatmaps.append(current_heatmap)

    # Create colormap
    colormap = branca.colormap.linear.viridis.scale(0, current_max+10)
    colormap = colormap.to_step(index=np.arange(0, current_max + 20, 10))
    colormap.caption = 'Travel time in minutes'
    colormaps.append(colormap)


# Create map
map=folium.Map(location=home_coords, zoom_start=15, max_zoom=18, min_zoom=12, name ='Map', control=False)
folium.TileLayer().add_to(map)
folium.TileLayer('Stamen Toner').add_to(map)

folium.Marker(home_coords, popup='Home',
              icon=folium.Icon(color='red',icon='home', prefix='fa') ).add_to(map)

for heatmap in heatmaps:
    map.add_child(heatmap)
for colormap in colormaps:
    map.add_child(colormap)
for heatmap, colormap in zip(heatmaps, colormaps):
    map.add_child(BindColormap(heatmap, colormap))
map.add_child(folium.map.LayerControl(collapsed=False))

map.save('index.html')
