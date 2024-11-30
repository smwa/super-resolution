import numpy as np
import tensorflow as tf

import io

from PIL import Image

from model.edsr import edsr


model = edsr(scale=4, num_res_blocks=16)
model.load_weights('weights/edsr-16-x4/weights.h5')


DIV2K_RGB_MEAN = np.array([0.4488, 0.4371, 0.4040]) * 255

def resolve_single(model, lr):
    return resolve(model, tf.expand_dims(lr, axis=0))[0]

def resolve(model, lr_batch):
    lr_batch = tf.cast(lr_batch, tf.float32)
    sr_batch = model(lr_batch)
    sr_batch = tf.clip_by_value(sr_batch, 0, 255)
    sr_batch = tf.round(sr_batch)
    sr_batch = tf.cast(sr_batch, tf.uint8)
    return sr_batch

# ---------------------------------------
#  Normalization
# ---------------------------------------

def normalize(x, rgb_mean=DIV2K_RGB_MEAN):
    return (x - rgb_mean) / 127.5


def denormalize(x, rgb_mean=DIV2K_RGB_MEAN):
    return x * 127.5 + rgb_mean

# ---------------------------------------
#  See https://arxiv.org/abs/1609.05158
# ---------------------------------------

def pixel_shuffle(scale):
    return lambda x: tf.nn.depth_to_space(x, scale)

def load_image(file: io.BytesIO) -> np.array:
  return np.array(Image.open(file))

def super_resolution_png(low_resolution_image_file: io.BytesIO) -> io.BytesIO:
  lr = np.array(Image.open(low_resolution_image_file))
  sr = resolve_single(model, lr)
  img = Image.fromarray(sr.numpy(), 'RGB')
  byteIO = io.BytesIO()
  img.save(byteIO, format='PNG')
  return byteIO
