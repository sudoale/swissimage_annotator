from pathlib import Path
import glob
from PIL import Image

DATA_DIR = Path(__file__).parent / 'static' / 'data'


def annotate_images(project):
    IMG_DIR = DATA_DIR / project / 'crops'
    Y_DIR = IMG_DIR / 'y'
    N_DIR = IMG_DIR / 'n'
    Y_DIR.mkdir(exist_ok=True)
    N_DIR.mkdir(exist_ok=True)
    images = glob.glob(str(IMG_DIR / '*.tif'))
    images = [img_path.split('\\')[-1] for img_path in images]
    for image_name in images:
        annotate_image(image_name)


def annotate_image(image_name, project):
    IMG_DIR = DATA_DIR / project / 'crops'
    Y_DIR = IMG_DIR / 'y'
    N_DIR = IMG_DIR / 'n'
    img_path = IMG_DIR / image_name
    img = Image.open(img_path)
    img.show()
    annotation = input("Do you see a soccer pitch?")
    img.close()
    if annotation == 'y':
        destination = Y_DIR / image_name
    else:
        destination = N_DIR / image_name
    img_path.replace(destination)


if __name__ == '__main__':
    annotate_images('football')
