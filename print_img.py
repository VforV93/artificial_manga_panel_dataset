
import os
from PIL import Image, ImageDraw
from preprocesing.layout_engine.helpers import get_leaf_panels
from preprocesing.layout_engine.page_creator import create_single_page
from preprocesing.layout_engine.page_object_classes import Page

metadata_dir = "datasets/page_metadata/"
images_dir = "datasets/page_images/"
dry = False

filenames = [(metadata_dir+filename, images_dir, dry)
                for filename in os.listdir(metadata_dir)
                if filename.endswith(".json")]

for filename in filenames:
    path_file = filename
    json_file = os.path.split(path_file[0])[1]
    png_file = os.path.splitext(json_file)[0]+'.png'
    file_path = os.path.join(path_file[1],png_file)

    page = Page()
    page.load_data(path_file[0])
    leaf_children = []
    get_leaf_panels(page, leaf_children)

    with Image.open(file_path) as im:
        im = im.convert('RGB')
        im1 = ImageDraw.Draw(im) 
        for coord in [lc.coords for lc in leaf_children]:
            im1.line(coord, width=10, fill="blue")
        im.show()
