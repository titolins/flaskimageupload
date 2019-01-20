#!/usr/bin/env python

import requests
#import json
import numpy as np
import pandas as pd
from PIL import Image

URI = 'https://chipos.pythonanywhere.com/classify'
IMAGE_FILE = 'titu.jpg'

def load_image_data():
    pic = Image.open(IMAGE_FILE)
    img_data = pd.Series(np.array(pic).flatten()).to_json(orient='values')
    return dict(
        data=img_data)

#pixa = list(pix)
#for i in range(len(df.iloc[0])-len(pix)):
#   pixa.append(0)
#   pixa = np.array(pixa)
#
#   print('Prediction:', neural.predict([pixa, pixa])[0], 'Truth:' , photo)
#   print(neural.predict([pixa, pixa])[0] ==  photo)
def make_request():
    print('image_data')
    print(load_image_data())
    #print(URI)
    #r = requests.get(url=URI,params=load_image_data())
    r = requests.get('http://chipos.pythonanywhere.com/classify', data=load_image_data())
    print(r.json())

    # supposed to be 201

if __name__ == '__main__':
    make_request()

