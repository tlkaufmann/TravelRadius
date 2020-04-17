# TravelRadius

Create maps that displays the travel times around my home using the *Google Distance Matrix API* to compute travel times and `folium` to display the results.

[Link to the interactive map](https://tomkau93.github.io/TravelRadius/index)

## Setup
You need an API Key for the [Google Distance Matrix API](https://developers.google.com/maps/documentation/distance-matrix/start) and place it in the file `API_key.txt`. 
*WARNING: I used the free test version of the Distance Matrix API but testing thousands of distances can easily add up to severall 100$ so be careful!*

The script can easily be used for any location by simply adjusting the values in the configuration file `config.json` and then run `run.sh`.

## Next steps
- [x] Implement the four different modes (walking, biking, driving and transit)
- [ ] Add colorbar
- [ ] Create nicer folder structure and a `setup.py` file
- [ ] Create a clustering of points similar to Sebastian Strug (see below)

## Similar projects
While working on this I found [this great article](https://towardsdatascience.com/travel-map-8407796c9219) by Sebastian Strug. I forced myself not to look at it until I was done so I would have to figure things out by myself.
Sebastian also uses folium but utilizes a clever way to cluster the datapoints instead of displaying them as a heatmap (definitely worth checking out).
