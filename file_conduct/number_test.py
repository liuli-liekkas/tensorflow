# """Functions for downloading and reading MNIST data."""
# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function
#
# # pylint: disable=unused-import
# import gzip
# import os
# import tempfile
#
# import numpy
# from six.moves import urllib
# from six.moves import xrange # pylint: disable=redefined-builtin
# import tensorflow as tf
# from tensorflow.contrib.learn.python.learn.datasets.mnist import read_data_sets # pylint: enable=unused-import
# import tensorflow.examples.tutorials.mnist.input_data as input_data
#
# mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

import tensorflow as tf

x = tf.placeholder(tf.float32, [None, 784])
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))
y = tf.nn.softmax(tf.matmul(x, W) + b)