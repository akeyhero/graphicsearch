import os
import sys
import numpy as np
from PIL import Image
from keras.applications.imagenet_utils import decode_predictions
from efficientnet.keras import EfficientNetB0
from efficientnet.keras import center_crop_and_resize, preprocess_input

class Vectorizer():
    def prepare(self):
        self.model = EfficientNetB0(weights='imagenet')
        return self

    def vectorize(self, image_file):
        image = np.array(Image.open(image_file))
        image_size = self.model.input_shape[1]
        x = center_crop_and_resize(image, image_size=image_size)
        x = preprocess_input(x)
        x = np.expand_dims(x, 0)
        y = self.model.predict(x)
        return y
