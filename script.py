import os

import tensorflow as tf
from PIL import Image

mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
train_dir = "mnist/train"
test_dir = "mnist/test"

os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)


def save_images(images, labels, directory):
    for i, (image, label) in enumerate(zip(images, labels)):
        # Create a directory for each label
        label_dir = os.path.join(directory, str(label))
        os.makedirs(label_dir, exist_ok=True)
        img = Image.fromarray(image)
        img.save(os.path.join(label_dir, f"{i:05}.png"))


save_images(x_train, y_train, train_dir)
save_images(x_test, y_test, test_dir)
