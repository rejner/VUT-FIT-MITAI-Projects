import tensorflow as tf
import keras.backend as K


def thresholded_accuracy(y_true: tf.Tensor, y_pred: tf.Tensor):
    threshold_pos = 0.8
    threshold_neg = 0.2
    y_pred_pos = K.cast(K.greater(y_pred, threshold_pos), K.floatx())
    y_pred_neg = K.cast(K.less(y_pred, threshold_neg), K.floatx())
    y_pred_between = K.cast(tf.math.logical_and(K.greater_equal(y_pred, threshold_neg), K.less_equal(y_pred, threshold_pos)), K.floatx())
    y_pred = y_pred_pos * 1.0 + y_pred_neg * 0.0 + y_pred_between * 0.5
    return K.mean(K.equal(y_true, y_pred))


def thresholded_positive_accuracy(y_true: tf.Tensor, y_pred: tf.Tensor):
    threshold_pos = 0.8
    y_pred_pos = K.cast(K.greater(y_pred, threshold_pos), K.floatx())
    y_true_pos = K.cast(K.greater(y_true, 0), K.floatx())
    correct_predictions = K.cast(K.equal(y_true, y_pred_pos), K.floatx()) * y_true_pos
    return K.sum(correct_predictions) / K.sum(y_true_pos)

if __name__ == '__main__':

    # test thresholded_accuracy
    y_true = tf.constant([1, 0, 1, 0, 1, 0, 1, 0, 1, 0], dtype=tf.float32)

    # should be 1.0
    y_pred = tf.constant([0.9, 0.1, 0.9, 0.1, 0.9, 0.1, 0.9, 0.1, 0.9, 0.1])
    print(thresholded_accuracy(y_true, y_pred))

    # should be 0.0
    y_pred = tf.constant([0.1, 0.9, 0.1, 0.9, 0.1, 0.9, 0.1, 0.9, 0.1, 0.9])
    print(thresholded_accuracy(y_true, y_pred))

    # should be 0.0
    y_pred = tf.constant([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
    print(thresholded_accuracy(y_true, y_pred))

    # should be 1.0
    y_pred = tf.constant([0.9, 0.35, 0.9, 0.1, 0.9, 0.1, 0.1, 0.1, 0.75, 0.1])
    print(thresholded_accuracy(y_true, y_pred))

    # should be 1.0
    y_pred = tf.constant([0.9, 0.1, 0.9, 0.1, 0.9, 0.1, 0.9, 0.1, 0.9, 0.1])
    print(thresholded_positive_accuracy(y_true, y_pred))

    # should be 0.0
    y_pred = tf.constant([0.1, 0.9, 0.1, 0.9, 0.1, 0.9, 0.1, 0.9, 0.1, 0.9])
    print(thresholded_positive_accuracy(y_true, y_pred))

    # should be 0.8
    y_pred = tf.constant([0.68, 0.1, 0.9, 0.1, 0.9, 0.1, 0.9, 0.1, 0.9, 0.1])
    print(thresholded_positive_accuracy(y_true, y_pred))



    