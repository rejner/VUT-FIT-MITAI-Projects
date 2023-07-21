import tensorflow as tf
from keras import layers
from keras.losses import cosine_similarity

class DistanceLayer(layers.Layer):
    """
    This layer is responsible for computing the distance between the anchor
    embedding and the positive embedding, and the anchor embedding and the
    negative embedding.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.cosine_similarity = metrics.CosineSimilarity()

    def call(self, anchor, positive, negative):        
        # ap_distance = tf.reduce_sum(tf.square(anchor - positive), keepdims=True, name='ap_distance')
        # an_distance = tf.reduce_sum(tf.square(anchor - negative), keepdims=True, name='an_distance')
        ap_distance = tf.reduce_sum(tf.square(anchor - positive), keepdims=True, name='ap_distance')
        an_distance = tf.reduce_sum(tf.square(anchor - negative), keepdims=True, name='an_distance')

        #ap_similarity = tf.reduce_sum(tf.convert_to_tensor(self.cosine_similarity(anchor, positive)), keepdims=True, name='ap_similarity')
        #an_similarity = tf.reduce_sum(tf.convert_to_tensor(self.cosine_similarity(anchor, negative)), keepdims=True, name='an_similarity')
        
        ap_similarity = tf.reduce_sum(cosine_similarity(anchor, positive), keepdims=True, name='ap_similarity')
        an_similarity = tf.reduce_sum(cosine_similarity(anchor, negative), keepdims=True, name='an_similarity')
        
        
        return tf.concat([ap_distance, an_distance, tf.reshape(ap_similarity, [1, 1]), tf.reshape(an_similarity, [1, 1])], axis=1)
        # return tf.concat([ap_distance, an_distance, ap_similarity, an_similarity], axis=1)


