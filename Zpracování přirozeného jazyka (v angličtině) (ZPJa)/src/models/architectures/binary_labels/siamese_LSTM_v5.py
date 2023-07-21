import keras
import tensorflow as tf
from keras import layers
from keras import backend as K
from src.models.architectures.utils.math import cosine_distance

# Siamese LSTM architecture in Keras using Keras API for TensorFlow backend
class SiameseLSTM_v5():

    def __init__(self, lstm_hidden_size=256, name="SiameseLSTM_v5"):
        self.lstm_hidden_size = lstm_hidden_size
        self.name = name

    def build_lstm_part(self, verbose=False):
        x1_input = keras.Input(shape=(128, 100), name="x1", dtype=tf.float32)
        x2_input = keras.Input(shape=(128, 100), name="x2", dtype=tf.float32)

        # create two siamese LSTM networks
        lstm = layers.LSTM(self.lstm_hidden_size, return_sequences=False)

        # pass the features to the LSTM networks
        x1 = lstm(x1_input)
        x1 = layers.Flatten()(x1)
        x2 = lstm(x2_input)
        x2 = layers.Flatten()(x2)

        x3 = layers.Subtract()([x1, x2]) # calculate the difference between x1 and x2
        x4 = layers.Lambda(cosine_distance)([x1, x2]) # calculate the cosine distance between x1 and x2

        conc = layers.Concatenate()([x3, x4]) # concatenate the difference and cosine distance

        x = layers.Dense(256, activation='relu', name="conc_layer")(conc)
        x = layers.Dropout(0.1)(x)
        # x = layers.Dense(128, activation='relu', name="last_layer")(x)
        output = layers.Dense(1, activation='sigmoid', name="output_layer")(x)

        model = keras.Model(inputs=[x1_input, x2_input], outputs=output, name=f"{self.name}-lstm_part")
        if verbose: model.summary()
        return model

    def build(self, verbose=False):
        
        lstm_model = self.build_lstm_part(verbose)
        print("LSTM model built")
        
        if verbose: lstm_model.summary()
        return lstm_model
