from PIL import Image
import os


# Get the path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)

# # Get the parent directory
# parent_dir = os.path.dirname(current_dir)
# print(parent_dir)

# Construct the full path to the file
file_path = f'{current_dir}/images'

for file in os.listdir(file_path):
    name, extension = os.path.splitext(file)
    if extension.endswith('jpg'):
        filename = f'./images/{file}'
        print(filename)
        im = Image.open(filename)
        new_filename = f'./images/{name}.gif'
        im.save(new_filename, format='GIF')
        print(type(im))