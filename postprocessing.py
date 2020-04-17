import pickle
import numpy as np
import json

with open('configs.json', 'r') as f:
    configs = json.load(f)
display_sizes = configs['display_sizes']
grid_size = configs['grid_size']

all_times = pickle.load(open('data/all_times.p', 'rb'))

for mode in all_times:

    all_times[mode] = all_times[mode][int(grid_size/2*(1-display_sizes[0])):int(grid_size/2*(1+display_sizes[0])),
                                      int(grid_size/2*(1-display_sizes[1])):int(grid_size/2*(1+display_sizes[1]))]

    if configs['max_time'] == -1:
        max_time = np.quantile(all_times[mode], 0.99)
    else:
        max_time = configs['max_time']

    all_times[mode][all_times[mode] > max_time] = max_time

    if configs['missing_points'] == 'neighboorhood':
        missing_datapoints = np.stack(np.where(all_times[mode] == -1), axis = 1)
        for point in missing_datapoints:
            lon_min, lon_max = max(0, point[0]-20), min(all_times[mode].shape[0], point[0]+20)
            lat_min, lat_max = max(0, point[1]-20), min(all_times[mode].shape[1], point[1]+20)
            neighborhood = all_times[mode][lon_min:lon_max, lat_min:lat_max]
            all_times[mode][point[0], point[1]] = np.mean(neighborhood[neighborhood!=-1])
    elif configs['missing_points'] == 'max':
        all_times[mode][all_times[mode] == -1] = np.max(all_times[mode])

    all_times[mode] = np.round(all_times[mode], -1)

pickle.dump(all_times, open('data/all_times_processed.p', 'wb'))
