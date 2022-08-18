from PIL import Image
import imagehash
import os
import numpy as np
from dotenv import load_dotenv

load_dotenv()


def find_duplicates(location, size, hash_size=8):
    """
    Find and delete duplicated images. If duplicated images are in different size, the one nearer to the optimal
    size will be kept.

    Parameters:
        location (str): Location of the image folder
        size (int): Optimal length of the image
        hash_size (int): The hash size, default 8

    Returns:
        None
    """

    # calculate the area of optimal size of the image
    optimal_size = size * size

    fnames = os.listdir(location)
    hashes = {}
    for image in fnames:
        if not image.endswith('.DS_Store'):
            try:
                with Image.open(os.path.join(location, image)) as img:
                    temp_hash = imagehash.average_hash(img, hash_size)
                    if temp_hash in hashes:
                        # compare 2 image size and keep the appropriate one
                        print(hashes[temp_hash], '      ', [image, img.size])
                        image_1 = hashes[temp_hash][0]
                        image_2 = image
                        diff_1 = np.abs(hashes[temp_hash][1][0] * hashes[temp_hash][1][1] - optimal_size)
                        diff_2 = np.abs(img.size[0] * img.size[1] - optimal_size)

                        if diff_1 >= diff_2:
                            # replace hash information if the original one is deleted
                            os.remove(os.path.join(location, image_1))
                            hashes[temp_hash] = [image, img.size]
                            print(image_1, 'removed')

                        else:
                            os.remove(os.path.join(location, image_2))
                            print(image_2, 'removed')
                    else:
                        # if not duplicated, save hash is dictionary for comparison with other images
                        hashes[temp_hash] = [image, img.size]
            except:
                print('cannot read', image)


TARGET_PATH = os.getenv('TARGET_PATH')
folder_name = 'donkey'
image_folder = os.path.join(TARGET_PATH, folder_name)

# optimal image size will be 224 * 224 since we do not need very high quality image for image classification
find_duplicates(image_folder, 224)
