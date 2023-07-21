import tensorflow as tf
from keras import layers

def cosine_similarity(a, b):
    # shapes: (batch_size, 50), (batch_size, 50)
    mag_a = tf.sqrt(tf.reduce_sum(tf.multiply(a, a), axis=1))
    mag_b = tf.sqrt(tf.reduce_sum(tf.multiply(b, b), axis=1))
    return tf.reduce_sum(tf.multiply(a, b)) / (mag_a * mag_b)


class CosineSimilarityLayer(layers.Layer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def call(self, a, b):        
        mag_a = tf.sqrt(tf.reduce_sum(tf.multiply(a, a), axis=1))
        mag_b = tf.sqrt(tf.reduce_sum(tf.multiply(b, b), axis=1))
        return tf.reduce_sum(tf.multiply(a, b)) / (mag_a * mag_b)


