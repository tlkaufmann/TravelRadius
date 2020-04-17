import json
from time import sleep
import numpy as np
import googlemaps
import pickle
from tqdm import tqdm

with open('API_KEY.txt', 'r') as f:
    API_KEY = f.read()

with open('configs.json', 'r') as f:
    configs = json.load(f)
home_coords = tuple(configs['home_coords'])
grid_size = configs['grid_size']
max_extent = configs['max_extent']

gmaps_api = googlemaps.Client(key=API_KEY)

modes = ['driving', 'walking', 'bicycling', 'transit']

# set up destinations
grid_size = grid_size + grid_size % 5
longs = home_coords[0] + np.linspace(-max_extent, max_extent, grid_size)
lats = home_coords[1] + np.linspace(-max_extent, max_extent, grid_size)
destinations = np.reshape(np.array(np.meshgrid(longs, lats)), (2, -1)).T
destinations = list(map(tuple, destinations))
nr_batches = int(np.ceil(len(destinations) / 25))

all_times = {}
for mode in modes:
    cur_times = np.zeros(len(destinations))
    for batch in tqdm(range(nr_batches), desc=mode):
        sleep(25*1/100)

        directions_result = gmaps_api.distance_matrix(origins=[home_coords],
                                                      destinations=destinations[batch*25:(batch+1)*25],
                                                      mode=mode)

        for i in range(25):
            try:
                cur_times[i + batch*25] = directions_result['rows'][0]['elements'][i]['duration']['value'] / 60
            except:
                cur_times[i + batch * 25] = -1

    cur_times = np.reshape(cur_times, (grid_size, grid_size))
    all_times[mode] = cur_times

pickle.dump(all_times, open('data/all_times.p', 'wb'))
