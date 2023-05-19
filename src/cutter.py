import cv2
from pathlib import Path

from src.helpers import get_all_images
from config import IMAGE_WIDTH

ROOT = Path(__file__).parent.parent
IMG_DIR = ROOT / 'static' / 'data'


def crop_image(image_name, cuts_per_axis, project):
    print(cuts_per_axis)
    coordinates = image_name.split('.')[0][-9:].split('-')
    start_x = int(coordinates[0]) * 1000
    start_y = int(coordinates[1]) * 1000
    PROJECT_DIR = IMG_DIR / project
    OUT_DIR = PROJECT_DIR / 'crops'
    OUT_DIR.mkdir(exist_ok=True)
    
    image = cv2.imread(str(PROJECT_DIR / image_name))
    image_width = image.shape[0]
    image_height = image.shape[1]
    cropped_width = int(image_width / cuts_per_axis)
    cropped_height = int(image_height / cuts_per_axis)
    print(image_height)
    print(cropped_height)

    for i in range(cuts_per_axis):
        for j in range(cuts_per_axis):
            x = i * cropped_width
            y = j * cropped_height
            new_x = start_x + int(x/10)
            new_y = start_y + int(y/10)
            cv2.imwrite(str(OUT_DIR / f'{new_x}_{new_y}.png'), image[x : x + cropped_width, y : y + cropped_height, :])

    (PROJECT_DIR / image_name).unlink()


def crop_all_images(project):
    images = get_all_images(IMG_DIR / project, 'tif')
    cuts_per_image = int(1000 / IMAGE_WIDTH)
    for img_name in images:
        crop_image(img_name, cuts_per_image, project)


if __name__ == '__main__':
    crop_all_images()
