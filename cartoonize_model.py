import os
import cv2
import numpy as np

# Tensorflow v1 compatibility
import tensorflow.compat.v1 as tf 
tf.disable_v2_behavior()

from WBCartoonization.test_code import network, guided_filter
from tqdm import tqdm


class CartoonizeModel():
    def __init__(self, options):
        # reset
        tf.reset_default_graph()

        self.model_path = options['model_path']
        self.session = None
        self.final_out = None
        self.input_photo = None

    def load_session(self):
        input_photo = tf.placeholder(tf.float32, [1, None, None, 3])
        network_out = network.unet_generator(input_photo)
        final_out = guided_filter.guided_filter(input_photo, network_out, r=1, eps=5e-3)

        all_vars = tf.trainable_variables()
        gene_vars = [var for var in all_vars if 'generator' in var.name]
        saver = tf.train.Saver(var_list=gene_vars)

        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        sess = tf.Session(config=config)

        sess.run(tf.global_variables_initializer())
        saver.restore(sess, tf.train.latest_checkpoint(self.model_path))

        self.session = sess
        self.final_out = final_out
        self.input_photo = input_photo

    def resize_crop(self, image, resize=1):
        if resize == 0 or resize == 1:
            return image

        h, w, c = np.shape(image)
        max_size = min(h, w) * resize // 1
        if min(h, w) > max_size:
            if h > w:
                h, w = int(max_size*h/w), max_size
            else:
                h, w = max_size, int(max_size*w/h)
        h, w = int((h//8)*8), int((w//8)*8)
        image = cv2.resize(image, (w, h),
                           interpolation=cv2.INTER_AREA)
        image = image[:h, :w, :]
        return image

    def cartoonize(self, input_image, opts):
        print('Cartoonize, start.')
        if not self.session:
            self.load_session()

        image = self.resize_crop(np.array(input_image), resize=opts['resize'])
        print('resized')
        batch_image = image.astype(np.float32)/127.5 - 1
        batch_image = np.expand_dims(batch_image, axis=0)
        output = self.session.run(self.final_out, feed_dict={self.input_photo: batch_image})
        output = (np.squeeze(output)+1)*127.5
        output = np.clip(output, 0, 255).astype(np.uint8)

        return output
