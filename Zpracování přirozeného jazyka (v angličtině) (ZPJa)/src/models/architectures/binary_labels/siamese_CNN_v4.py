import keras
import tensorflow as tf
from keras.layers import Conv1D, MaxPooling1D, Flatten
from keras import layers

from src.models.architectures.utils.math import cosine_distance

class SiameseCNN_v4():

    def __init__(self, trainable=False, name="SiameseCNN_v4"):
        self.trainable = trainable
        self.name = name

    def build_conv_part(self, verbose=False):
        x1_input = keras.Input(shape=(128, 100), name="x1", dtype=tf.float32)
        x2_input = keras.Input(shape=(128, 100), name="x2", dtype=tf.float32)

        # Define the first convolutional layer
        conv_1 = tf.keras.layers.Conv1D(256, 3, activation='relu')
        conv_2 = tf.keras.layers.Conv1D(128, 3, activation='relu')
        conv_3 = tf.keras.layers.Conv1D(64, 5, activation='relu')
        conv_4 = tf.keras.layers.Conv1D(256, 3, activation='relu')

        global_maxpool = tf.keras.layers.GlobalMaxPool1D()

        x1 = conv_1(x1_input)
        x1 = conv_2(x1)
        x1 = conv_3(x1)
        x1 = conv_4(x1)
        x1 = global_maxpool(x1)

        x2 = conv_1(x2_input)
        x2 = conv_2(x2)
        x2 = conv_3(x2)
        x2 = conv_4(x2)
        x2 = global_maxpool(x2)

        x3 = layers.Subtract()([x1, x2]) # calculate the difference between x1 and x2
        x4 = layers.Lambda(cosine_distance)([x1, x2]) # calculate the cosine distance between x1 and x2

        conc = layers.Concatenate()([x3, x4]) # concatenate the difference and cosine distance
        x = layers.Dropout(0.01)(conc)

        x = layers.Dense(256, activation='relu', name="conc_layer")(x)
        output = layers.Dense(1, activation='sigmoid', name="output_layer")(x)

        model = keras.Model(inputs=[x1_input, x2_input], outputs=output, name=f"{self.name}-conv_part")
        if verbose: model.summary()
        return model

    def build(self, verbose=False):

        conv_model = self.build_conv_part(verbose)
        print("Convolution model built")
        
        if verbose: conv_model.summary()
        return conv_model
