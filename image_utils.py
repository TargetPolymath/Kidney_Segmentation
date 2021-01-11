import numpy
from PIL import Image, ImageDraw
import subprocess
import json
from pathlib import Path

import pickle

import RL_utils

TRAIN_CSV_PATH = Path("./DB/train.csv")
TRAIN_RASTER_DIR = Path("./DB/train")



def get_rasterized_mask(im_string):
    raster_path = TRAIN_RASTER_DIR.joinpath(Path(im_string+".pkl"));
    # print(raster_path)
    
    if raster_path.exists():

        rasterized_im = pickle.loads(raster_path.read_bytes())
        return rasterized_im
    
    else:
        # rle_im_string = subprocess.run(["cat", f"./{TRAIN_CSV_PATH} | grep {im_string}"], stdout=subprocess.PIPE).stdout.decode('utf-8')
        reader = subprocess.Popen(["cat", f"./{TRAIN_CSV_PATH}"], stdout=subprocess.PIPE)
        grepper = subprocess.Popen(["grep", im_string], stdin=reader.stdout, stdout=subprocess.PIPE)
        reader.stdout.close()
        
        rle_text, err = grepper.communicate()
        rle_text = rle_text.decode('utf-8')

        
        rle_split = [int(k) for k in rle_text.split(",")[1].split(" ")]
        
        lb_len = rle_split[-2]
        print(lb_len)
        
        
        rle_data = list(zip(rle_split[0::2], rle_split[1::2]))
        
        rle_array = RL_utils.rldecode(rle_data)
        print("Array Encoded")
        
        raster_path.touch()
        print("File Created")
        raster_path.write_bytes(pickle.dumps(rle_array))
        print("File Written")
        return rle_array

    
def get_rle(im_string):
    raster_path = TRAIN_RASTER_DIR.joinpath(Path(im_string+".pkl"));
    # print(raster_path)
    

        # rle_im_string = subprocess.run(["cat", f"./{TRAIN_CSV_PATH} | grep {im_string}"], stdout=subprocess.PIPE).stdout.decode('utf-8')
    reader = subprocess.Popen(["cat", f"./{TRAIN_CSV_PATH}"], stdout=subprocess.PIPE)
    grepper = subprocess.Popen(["grep", im_string], stdin=reader.stdout, stdout=subprocess.PIPE)
    reader.stdout.close()

    rle_text, err = grepper.communicate()
    rle_text = rle_text.decode('utf-8')


    rle_split = [int(k) for k in rle_text.split(",")[1].split(" ")]

    lb_len = rle_split[-2]
    print(lb_len)


    rle_data = list(zip(rle_split[0::2], rle_split[1::2]))

    return rle_data

def preload_all_masks():
    strings = ["0486052bb",
        "095bf7a1f",
        "1e2425f28",
        "2f6ecfcdf",
        "54f2eec69",
        "aaa6a05cc",
        "cb2d976f4",
        "e79de561c",
        ]
    
    from multiprocessing import Pool
    p = Pool()
    p.map(get_rasterized_mask, strings)
    

if __name__ == "__main__":
    preload_all_masks();
    test_im_string = "095bf7a1f"
    
    print(get_rasterized_mask(test_im_string))
        
        
        
        
    
    
