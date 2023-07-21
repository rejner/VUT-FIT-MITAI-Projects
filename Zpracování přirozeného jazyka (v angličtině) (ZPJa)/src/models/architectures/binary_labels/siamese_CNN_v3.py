import keras
import tensorflow as tf
from keras.layers import Conv1D, MaxPooling1D, Flatten
from keras import layers

from src.models.architectures.utils.math import cosine_distance

class SiameseCNN_v3():

    def __init__(self, trainable=False, name="SiameseCNN_v3"):
        self.trainable = trainable
        self.name = name

    def build_conv_part(self, verbose=False):
        x1_input = keras.Input(shape=(128, 100), name="x1", dtype=tf.float32)
        x2_input = keras.Input(shape=(128, 100), name="x2", dtype=tf.float32)

        max_pooling_3 = MaxPooling1D(3)

        # create two siamese CNN networks
        conv_1_3 = Conv1D(128, 3, activation='relu', padding='same')
        conv_1_5 = Conv1D(128, 5, activation='relu', padding='same')
        conv_1_7 = Conv1D(128, 7, activation='relu', padding='same')

        conv_2_3 = Conv1D(64, 3, activation='relu', padding='same')
        conv_2_5 = Conv1D(64, 5, activation='relu', padding='same')
        conv_2_7 = Conv1D(64, 7, activation='relu', padding='same')

        #conv_3_3 = Conv1D(32, 3, activation='relu', padding='same')
        #conv_3_5 = Conv1D(32, 5, activation='relu', padding='same')
        #conv_3_7 = Conv1D(32, 7, activation='relu', padding='same')


        # query branch
        x1_q = conv_1_3(x1_input)
        x2_q = conv_1_5(x1_input)
        x3_q = conv_1_7(x1_input)
        x1_q = max_pooling_3(x1_q)
        x2_q = max_pooling_3(x2_q)
        x3_q = max_pooling_3(x3_q)

        x1_q = conv_2_7(x1_q)
        x2_q = conv_2_5(x2_q)
        x3_q = conv_2_3(x3_q)
        x1_q = max_pooling_3(x1_q)
        x2_q = max_pooling_3(x2_q)
        x3_q = max_pooling_3(x3_q)

        # document branch
        x1_d = conv_1_3(x2_input)
        x2_d = conv_1_5(x2_input)
        x3_d = conv_1_7(x2_input)
        x1_d = max_pooling_3(x1_d)
        x2_d = max_pooling_3(x2_d)
        x3_d = max_pooling_3(x3_d)

        x1_d = conv_2_7(x1_d)
        x2_d = conv_2_5(x2_d)
        x3_d = conv_2_3(x3_d)
        x1_d = max_pooling_3(x1_d)
        x2_d = max_pooling_3(x2_d)
        x3_d = max_pooling_3(x3_d)

        # concatenate the three branches
        x1 = layers.Concatenate()([x1_q, x2_q, x3_q])
        x2 = layers.Concatenate()([x1_d, x2_d, x3_d])

        x1 = Flatten()(x1)
        x2 = Flatten()(x2)

        x3 = layers.Subtract()([x1, x2]) # calculate the difference between x1 and x2
        x4 = layers.Lambda(cosine_distance)([x1, x2]) # calculate the cosine distance between x1 and x2

        x1 = layers.Dense(512, activation='relu')(x1)
        x2 = layers.Dense(512, activation='relu')(x2)

        x1 = layers.Dropout(0.01)(x1)
        x2 = layers.Dropout(0.01)(x2)

        x = layers.Concatenate()([x1, x2, x3, x4])
        
        x = layers.Dense(512, activation='relu', name="conc_layer", kernel_regularizer=keras.regularizers.l1(0.001))(x)
        
        output = layers.Dense(1, activation='sigmoid', name="output_layer")(x)

        model = keras.Model(inputs=[x1_input, x2_input], outputs=output, name=f"{self.name}-conv_part")
        if verbose: model.summary()
        return model

    def build(self, verbose=False) -> tuple[keras.Model, keras.Model, keras.Model]:

        conv_model = self.build_conv_part(verbose)
        print("Convolution model built")
        
        if verbose: conv_model.summary()
        return conv_model
