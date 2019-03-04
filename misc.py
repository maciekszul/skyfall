import json
from collections import OrderedDict
from skimage import data, img_as_float
from skimage.measure import compare_ssim as ssim
   
def update_key_value(file, key, value):
    """
    Function to update a key value in a JSON file. If passed
    key is not in the JSON file, it is going to be appended 
    at the end of the file.
    """
    with open(file, "r") as json_file:
        data = json.load(json_file, object_pairs_hook=OrderedDict)
        data[key] = value
    
    with open(file, "w") as json_file:
        json.dump(data, json_file, indent=4)

def SSIM(img1, img2):
    """
    Function returns SSIM measure from two images as numpy array
    """
    ssim_score = ssim(
        img1,
        img2,
        data_range=img2.max() - img2.min(),
        multichannel=True
    )
    return ssim_score

def SSIM_temp_gen(ix_mx):
    pass