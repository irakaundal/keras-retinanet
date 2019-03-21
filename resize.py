import cv2
import os
import numpy as np

# create blank mask for pristine images

blank_img_dir = 'Data/Training/Masks'
if not os.path.isdir(blank_img_dir):
    os.makedirs(blank_img_dir)

blank_img = np.ones((320,320,3),np.uint8)*255
cv2.imwrite(blank_img_dir + '/general.png', blank_img)

# resize fake images, pristine images, fake masks, real masks

# fake images
dir_fake_images = 'Data/Training/Fake/Images'
files = os.listdir(dir_fake_images)

for iter, file in enumerate(files):
    img_path = os.path.join(dir_fake_images, file)
    img = cv2.imread(img_path)
    img = cv2.resize(img, (320,320))
    cv2.imwrite(img_path, img)
    print(iter+1)

# fake masks
dir_fake_masks = 'Data/Training/Fake/Masks'
files = os.listdir(dir_fake_masks)

for iter, file in enumerate(files):
    img_path = os.path.join(dir_fake_masks, file)
    img = cv2.imread(img_path)
    img = cv2.resize(img, (320,320))
    cv2.imwrite(img_path, img)
    print(iter+1)

# pristine images
dir_prist_img = 'Data/Training/Pristine'
files = os.listdir(dir_prist_img)

for iter, file in enumerate(files):
    img_path = os.path.join(dir_prist_img, file)
    img = cv2.imread(img_path)
    img = cv2.resize(img, (320,320))
    cv2.imwrite(img_path, img)
    print(iter+1)