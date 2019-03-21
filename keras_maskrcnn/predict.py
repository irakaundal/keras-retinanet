# import keras
import keras

# import keras_retinanet
from keras_maskrcnn import models
from keras_maskrcnn.utils.visualization import draw_mask
from keras_retinanet.utils.visualization import draw_box, draw_caption, draw_annotations
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from keras_retinanet.utils.colors import label_color

# import miscellaneous modules
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
import time

# set tf backend to allow memory to grow, instead of claiming everything
import tensorflow as tf

def get_session():
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    return tf.Session(config=config)

# use this environment flag to change which GPU to use
#os.environ["CUDA_VISIBLE_DEVICES"] = "1"

# set the modified tf session as backend in keras
keras.backend.tensorflow_backend.set_session(get_session())

# LINE TO CHANGE --------------------------------------------------------------------------------------------------
model_path = os.path.join('..', 'snapshots', 'resnet50_coco_v0.2.0.h5')

# load retinanet model
model = models.load_model(model_path, backbone_name='resnet50')
#print(model.summary())

# load label to names mapping for visualization purposes
labels_to_names = {0: 'pristine', 1: 'fake'}

# path to detections LINE TO CHANGE -------------------------------------------------------------------------------
dir_detection = 'Data/Detected'

images = os.listdir('Data/Test')
for filename in images:
    image = read_image_bgr('Data/Test/' + filename)

    # copy to draw on
    draw = image.copy()
    draw = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)

    # preprocess image for network
    image = preprocess_image(image)
    image, scale = resize_image(image)

    # process image
    start = time.time()
    outputs = model.predict_on_batch(np.expand_dims(image, axis=0))
    print("processing time: ", time.time() - start)

    boxes  = outputs[-4][0]
    scores = outputs[-3][0]
    labels = outputs[-2][0]
    masks  = outputs[-1][0]

    # correct for image scale
    boxes /= scale

    # visualize detections
    for box, score, label, mask in zip(boxes, scores, labels, masks):
        if score < 0.5:
            break

        color = label_color(label)
        
        b = box.astype(int)
        draw_box(draw, b, color=color)
        
        mask = mask[:, :, label]
        draw_mask(draw, b, mask, color=label_color(label))
        
        caption = "{} {:.3f}".format(labels_to_names[label], score)
        #draw_caption(draw, b, caption)
        
    plt.figure(figsize=(15, 15))
    plt.axis('off')

    if not os.path.isdir(dir_detection):
        os.makedirs(dir_detection)

    plt.savefig(dir_detection + '/' + filename)