import math
from pathlib import Path

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import redirect
from flask import url_for

from src.helpers import (get_all_images,
                         get_image_by_radius,
                         order_images,
                         get_projects,
                         get_gapi_key)
from src.downloader import download_tif
from src.cutter import crop_all_images

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD']=True

IMG_DIR = Path(__file__).parent / 'static' / 'data'
IMG_DIR.mkdir(exist_ok=True)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/find')
def find():
    return render_template('find.html', projects=get_projects(), gapi_key=get_gapi_key())


@app.route('/<project_name>/annotate', methods=['GET', 'POST'])
def annotate(project_name):
    if request.method == 'POST':
        request_data = request.json
        order_images(request_data, IMG_DIR / project_name / 'crops')
        return 'Annotated'
    else:
        images = get_next_image_batch(200, project_name)
        return render_template('annotate.html', images=images, project=project_name, grid_size=int(math.sqrt(len(images))))


@app.route('/<project_name>/annotate/next')
def annotate_image(project_name):
    return jsonify(images=get_next_image_batch(200, project_name))


def get_next_image_batch(radius, project):
    all_crops = get_all_images(IMG_DIR / project / 'crops')
    if all_crops:
        images = get_image_by_radius(all_crops[0], radius)
        return [f'/static/data/{project}/crops/{image}' for image in images]
    else:
        return ['No images found']


@app.route('/view/<x>/<y>')
def view(x,y):
    base_url = 'https://wms.geo.admin.ch/?service=WMS&version=1.3.0&request=GetMap&width=250&height=250&styles=&layers=ch.swisstopo.images-swissimage&format=image/png&crs=EPSG:2056&BBOX='
    coords = f'{base_url}{x},{y},{int(x)+1000},{int(y)+1000}'
    left = f'/view/{int(x)-1000}/{y}'
    right = f'/view/{int(x) + 1000}/{y}'
    up = f'/view/{x}/{int(y) + 1000}'
    down = f'/view/{x}/{int(y) - 1000}'
    return render_template('view.html', coords=coords,
                           left=left, right=right, up=up, down=down, x=x, y=y)


def valid_bounds(x_min, x_max, y_min, y_max):
    x_range = x_max - x_min
    y_range = y_max - y_min
    print(x_range)
    print(y_range)
    if x_range > 0.1:
        return False
    elif y_range > 0.1:
        return False
    return True


@app.route('/download', methods=['POST'])
def download():
    request_data = request.json
    project_name = request_data['project_name']
    y_min = round(request_data['south'], 2)
    y_max = round(request_data['north'], 2)
    x_min = round(request_data['west'], 2)
    x_max = round(request_data['east'], 2)
    if valid_bounds(x_min, x_max, y_min, y_max):
        download_tif(x_min, x_max, y_min, y_max, IMG_DIR / project_name)
        crop_all_images(project_name)
        return jsonify({'success': True,
                        'message': 'Success'})
    return jsonify({'success': False,
                    'message': 'Too big map extent. Zoom closer to the area of interest.'})


@app.route('/create_project', methods=['POST'])
def create_project():
    request_data = request.json
    project_name = request_data['project_name'].lower()

    project_img_dir = IMG_DIR / project_name
    project_img_dir.mkdir(exist_ok=True)

    return jsonify({'success': True,
                    'message': 'Project created!'})


if __name__ == '__main__':
    app.run(debug=True)
