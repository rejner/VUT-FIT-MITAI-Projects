import keras
import tensorflow as tf
from keras.layers import LSTM, TextVectorization
from architectures.layers.GLoVe_embeddings import GLoVeEmbeddings
from architectures.layers.cosine_similarity_layer import CosineSimilarityLayer
from keras import layers
from keras import backend as K

from architectures.utils.math import cosine_distance


# Siamese LSTM architecture in Keras using Keras API for TensorFlow backend
class SiameseLSTM_2():

    def __init__(self, trainable=False, lstm_hidden_size=1024, name="SiameseLSTM"):
        self.trainable = trainable
        self.lstm_hidden_size = lstm_hidden_size
        self.name = name

    def build(self, vectorizer: TextVectorization, embeddings: GLoVeEmbeddings, verbose=False):
        
        # embeddings = GLoVeEmbeddings(vectorizer)
        
        query_input = keras.Input(shape=(), name="query", dtype=tf.string)
        doc_input = keras.Input(shape=(), name="doc", dtype=tf.string)

        x1 = vectorizer(query_input)
        x2 = vectorizer(doc_input)

        x1 = embeddings(x1) # query features
        x2 = embeddings(x2) # doc features

        # create two siamese LSTM networks
        model_lstm = LSTM(self.lstm_hidden_size, return_sequences=True)
        # model1_lstm = LSTM(self.lstm_hidden_size, return_sequences=False)
        # model2_lstm = LSTM(self.lstm_hidden_size, return_sequences=False)

        # pass the features to the LSTM networks
        x1 = model_lstm(x1)
        x1 = layers.Flatten()(x1)
        x2 = model_lstm(x2)
        x2 = layers.Flatten()(x2)

        x3 = layers.Subtract()([x1, x2]) # calculate the difference between x1 and x2
        x4 = layers.Lambda(cosine_distance)([x1, x2]) # calculate the cosine distance between x1 and x2

        conc = layers.Concatenate()([x3, x4]) # concatenate the difference and cosine distance

        x = layers.Dense(100, activation='relu', name="conc_layer")(conc)
        x = layers.Dropout(0.01)(x)
        output = layers.Dense(1, activation='sigmoid', name="output_layer")(x)

        model = keras.Model(inputs=[query_input, doc_input], outputs=output, name=self.name)
        if verbose: model.summary()
        return model

