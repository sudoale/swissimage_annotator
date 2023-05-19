import json
import glob
from pathlib import Path

from pyproj import Proj, itransform

from config import IMAGE_WIDTH


ROOT = Path(__file__).parent.parent


def convert_coordinates(coordinates, source_crs, target_crs, swap_coordinates=False):
    if swap_coordinates:
        coordinates = [[coord[1], coord[0]] for coord in coordinates]
    source_crs = Proj(projparams=source_crs)
    target_crs = Proj(projparams=target_crs)
    result = list(itransform(source_crs, target_crs, coordinates))
    return [list(coord) for coord in result]


def get_all_images(image_dir, i_format='png'):
    images = glob.glob(str(image_dir / f'*.{i_format}'))
    images = [img_path.split('\\')[-1] for img_path in images]
    return sorted(images)


def get_image_by_radius(image, radius, i_format='png'):
    coords = image[:-4].split('_')
    start_x = int(coords[0])
    start_y = int(coords[1])
    result = []
    for x in range(start_x, start_x + radius, IMAGE_WIDTH):
        for y in range(start_y, start_y + radius, IMAGE_WIDTH):
            result.append(f'{x}_{y}.{i_format}')
    return result


def get_projects():
    project_dir = ROOT / 'static' / 'data'
    return [str(dir).split("\\")[-1] for dir in project_dir.iterdir() if dir.is_dir()]


def order_images(images, img_dir):
    y_dir = img_dir.parent / 'y'
    n_dir = img_dir.parent / 'n'
    y_dir.mkdir(exist_ok=True)
    n_dir.mkdir(exist_ok=True)

    for image in images:
        img_name = image['src'].split('/')[-1]
        if image['selected']:
            _move_image(img_name, img_dir, y_dir)
        else:
            _move_image(img_name, img_dir, n_dir)


def _move_image(img_name, source, destination):
    source = source / img_name
    destination = destination / img_name
    if not destination.exists():
        source.replace(destination)


def get_gapi_key(fn='credentials.json'):
    credentials_path = Path(__file__).parent.parent / fn
    if credentials_path.exists():
        credentials = json.load(open(credentials_path))
        return credentials['key']
    else:
        return ''
