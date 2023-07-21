# import keras.backend as K
import tensorflow as tf

# tf function to calculate cosine distance

def cosine_distance(vectors):
    x, y = vectors
    # l2 normalize vectors with tf
    x = tf.math.l2_normalize(x, axis=-1)
    y = tf.math.l2_normalize(y, axis=-1)
    # tf mean
    return -tf.math.reduce_mean(x * y, axis=-1, keepdims=True)
    # return -K.mean(x * y, axis=-1, keepdims=True)