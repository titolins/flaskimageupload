#!/usr/bin/env python

import requests
import numpy as np
from PIL import Image

URI = 'http://chipos.pythonanywhere.com/classify'
IMAGE_FILE = 'titu.jpg'

def load_image_data():
    pic = Image.open(IMAGE_FILE)
    print(pic)
    return dict(
        data=list(np.array(pic).flatten()))

#pixa = list(pix)
#for i in range(len(df.iloc[0])-len(pix)):
#   pixa.append(0)
#   pixa = np.array(pixa)
#
#   print('Prediction:', neural.predict([pixa, pixa])[0], 'Truth:' , photo)
#   print(neural.predict([pixa, pixa])[0] ==  photo)

def make_request():
    r = requests.get(url=URI,params=load_image_data())
    print(r.json)

    # supposed to be 201

if __name__ == '__main__':
    make_request()

