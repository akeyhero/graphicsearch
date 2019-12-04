import os
import sys
import numpy as np
from skimage.io import imread
import matplotlib.pyplot as plt
from keras.applications.imagenet_utils import decode_predictions
from efficientnet.keras import EfficientNetB0
from efficientnet.keras import center_crop_and_resize, preprocess_input

class Vectorizer():
    def prepare(self):
        self.model = EfficientNetB0(weights='imagenet')
        return self
