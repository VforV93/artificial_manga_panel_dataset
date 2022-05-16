
import os
from preprocesing.layout_engine.page_creator import create_single_page

metadata_dir = "datasets/page_metadata/"
images_dir = "datasets/page_images/"
dry = False

filenames = [(metadata_dir+filename, images_dir, dry)
                for filename in os.listdir(metadata_dir)
                if filename.endswith(".json")]

print(filenames[0])
create_single_page(filenames[0])
