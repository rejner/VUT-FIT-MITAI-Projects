import keras
import tensorflow as tf
from keras import layers
from keras import backend as K
from src.models.architectures.utils.math import cosine_distance

class LSTM_v1():

    def __init__(self, lstm_hidden_size=128, name="LSTM_v1"):
        self.lstm_hidden_size = lstm_hidden_size
        self.name = name

    def build_lstm_part(self, verbose=False):
        x1_input = keras.Input(shape=(128, 100), name="query_embeddings", dtype=tf.float32)
        x2_input = keras.Input(shape=(100, 128, 100), name="documents_embeddings", dtype=tf.float32)

        # create two siamese LSTM networks
        lstm = layers.LSTM(self.lstm_hidden_size, return_sequences=False, input_shape=(100, 128, 100))

        # pass the features to the LSTM networks
        x1 = lstm(x1_input)
        x1 = layers.Flatten()(x1)

        x2_list = []
        for i in range(100):
            x2 = layers.Lambda(lambda x: x[:, i, :, :])(x2_input)
            x2 = lstm(x2)
            x2 = layers.Flatten()(x2)

            if i == 0:
                x2_list = [x2]
            else:
                x2_list.append(x2)

        #x2 = lstm(x2_input)
        #x2 = layers.Flatten()(x2)

        conc = layers.Concatenate(axis=1)([x1] + x2_list)
        conc = layers.Dense(256, activation='relu')(conc)

        # need 100 outputs for 100 documents representing the probability of the document being relevant
        # multiple documents can be relevant
        output = layers.Dense(100, name="output_layer")(conc)

        

        #x3 = layers.Subtract()([x1, x2]) # calculate the difference between x1 and x2
        #x4 = layers.Lambda(cosine_distance)([x1, x2]) # calculate the cosine distance between x1 and x2

        #conc = layers.Concatenate()([x3, x4]) # concatenate the difference and cosine distance

        # x = layers.Dense(100, activation='relu', name="conc_layer")(conc)
        # x = layers.Dropout(0.01)(x)
        # output = layers.Dense(1, activation='sigmoid', name="output_layer")(x)

        model = keras.Model(inputs=[x1_input, x2_input], outputs=output, name=f"{self.name}-multiclass")
        if verbose: model.summary()
        return model

    def build(self, verbose=False):
        
        lstm_model = self.build_lstm_part(verbose)
        print("LSTM model built")
        
        if verbose: lstm_model.summary()
        return lstm_model
