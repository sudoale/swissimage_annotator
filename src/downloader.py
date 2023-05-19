import requests
import json

from pathlib import Path

from src.helpers import convert_coordinates


BASE_URL = "https://data.geo.admin.ch/api/stac/v0.9/collections/ch.swisstopo.swissimage-dop10/items"
DATA_DIR = Path(__file__).parent.parent / 'static' / 'data'


def download_tif(x_min=None, x_max=None, y_min=None, y_max=None, data_dir=None, crs=4326):
    if not data_dir:
        data_dir = DATA_DIR

    if crs == 2056:
        coordinates = convert_coordinates([[x_min+100, y_min+100], [x_max-100, y_max-100]], 2056, 4326)
        x_min = coordinates[0][1]
        y_min = coordinates[0][0]
        x_max = coordinates[1][1]
        y_max = coordinates[1][0]

    query = ""
    if x_min and x_max and y_min and y_max:
        query += '?bbox=' + ','.join([str(x_min), str(y_min), str(x_max), str(y_max)])

    url = BASE_URL + query
    response = requests.get(url)
    data = json.loads(response.content.decode('utf-8'))
    for feature in data['features']:
        asset = list(filter(lambda a: a['eo:gsd'] == 0.1, feature['assets'].values()))[0]
        fn = f'{asset["href"].split("/")[-2]}.tif'
        r = requests.get(asset['href'])
        with open(data_dir / fn, 'wb') as f:
            f.write(r.content)


if __name__ == '__main__':
    download_tif(2752000, 2753000, 1212000, 1213000, crs=2056)

