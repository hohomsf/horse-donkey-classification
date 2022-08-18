import os
from dotenv import load_dotenv

load_dotenv()


def rename_img(f, prefix, suffix):
    """
    Rename images for easier management.

    Parameters:
        f (str): The file name
        prefix (str): The prefix to indicate what the image is about
        suffix (str): The suffix to indicate the order of the image

    Returns:
        None
    """

    file_type = f.split('.')[-1]
    if file_type == 'DS_Store':
        pass

    old_path = os.path.join(path, f)
    new_name = f'{prefix}_{suffix}.{file_type}'
    new_path = os.path.join(path, new_name)

    os.rename(old_path, new_path)

    print(new_name)


path = os.getenv('DATASET_PATH')
folder = os.listdir(path)
img_name = 'donkey'

i = 1
for fname in folder:
    num = str(i).zfill(4)
    rename_img(fname, img_name, num)
    i = i + 1
