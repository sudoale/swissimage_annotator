# swissimage_annotator
This project was crated for tasks of annotating image data from https://www.swisstopo.admin.ch/de/geodata/images/ortho/swissimage10.html.


# Setup

## Create conda environment
conda create --name swissimage --file requirements.txt

## Run the project
python app.py

## Workflow
1. Create a project
2. Configure your desired image crop size (config.py)
3. Download your images (/view or /find)
4. Annotate your images (/<project_name>/annotate)
5. Find your annotated images within the following project folder: 
swissimage_annotator/static/data/<project_name>


# Project routes

## /home
Main page for creating a project

## /view/x/y
Preferred method for downloading, as only one single image will be download.

Required parameters:
x: Longitude
y: Latitude

Coordinates can be looked up by accessing https://map.geo.admin.ch/ and a right click on the map.

e.g. /view/2758000/1191000 would point to the city of Chur.

## /find
Map based downloading option. Be aware that this method could take a while for downloading if zoom is set not appropriatly.

## /project_name/annotate
Annotate the download images of a project.


