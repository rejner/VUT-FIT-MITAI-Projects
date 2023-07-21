import tensorflow as tf

def triplet(margin=0.5):

    """
    def _triplet(ap_distance, an_distance):
        # Computing the Triplet Loss by subtracting both distances and
        # making sure we don't get a negative value.
        # ap_distance, an_distance = distances
        loss = ap_distance - an_distance
        loss = tf.maximum(loss + margin, 0.0)
        return loss
    """

    def _triplet_distance(y_true, y_pred):
        # Computing the Triplet Loss by subtracting both distances and
        # making sure we don't get a negative value.
        # ap_distance, an_distance = distances
        ap_distance = y_pred[:, 0]
        an_distance = y_pred[:, 1]
        # try to maximize the similarity between the anchor and the positive
        # and minimize the similarity between the anchor and the negative
        loss = ap_distance - an_distance
        loss = tf.maximum(loss + margin, 0.0)
        #tf.print("\n", ap_distance, an_distance)
        return loss

    def _triplet_similarity(y_true, y_pred):
        # Computing the Triplet Loss by subtracting both similarities and
        # making sure we don't get a negative value.
        # ap_distance, an_distance = distances
        ap_sim = y_pred[:, 2]
        an_sim = y_pred[:, 3]

        # try to maximize the similarity between the anchor and the positive
        # and minimize the similarity between the anchor and the negative
        # loss = ap_sim - an_sim
        loss = an_sim - ap_sim

        loss = tf.maximum(loss + margin, 0.0)
        #tf.print("\n", ap_distance, an_distance)
        return loss

    return _triplet_similarity

def contrastive_loss(margin=1.0):
    """Provides 'constrastive_loss' an enclosing scope with variable 'margin'.

    Arguments:
        margin: Integer, defines the baseline for distance for which pairs
                should be classified as dissimilar. - (default is 1).

    Returns:
        'constrastive_loss' function with data ('margin') attached.
    """

    # Contrastive loss = mean( (1-true_value) * square(prediction) +
    #                         true_value * square( max(margin-prediction, 0) ))
    def contrastive_loss(y_true, y_pred):
        """Calculates the constrastive loss.

        Arguments:
            y_true: List of labels, each label is of type float32.
            y_pred: List of predictions of same length as of y_true,
                    each label is of type float32.

        Returns:
            A tensor containing constrastive loss as floating point value.
        """

        square_pred = tf.math.square(y_pred)
        margin_square = tf.math.square(tf.math.maximum(margin - (y_pred), 0))
        return tf.math.reduce_mean(
            (1 - y_true) * square_pred + (y_true) * margin_square
        )

    return contrastive_loss

