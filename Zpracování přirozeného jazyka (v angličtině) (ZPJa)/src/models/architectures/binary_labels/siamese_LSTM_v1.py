import keras
import tensorflow as tf
from keras.layers import TextVectorization, LSTM
from architectures.layers.GLoVe_embeddings import GLoVeEmbeddings
from architectures.layers.cosine_similarity_layer import CosineSimilarityLayer


# Siamese LSTM architecture in Keras using Keras API for TensorFlow backend
class SiameseLSTM():

    def __init__(self, trainable=False, lstm_hidden_size=1024, name="SiameseLSTM"):
        self.trainable = trainable
        self.lstm_hidden_size = lstm_hidden_size
        self.name = name

    
    def build(self, vectorizer: TextVectorization, verbose=False):
        
        embeddings = GLoVeEmbeddings(vectorizer)
        
        query_input = keras.Input(shape=(), name="query", dtype=tf.string)
        doc_input = keras.Input(shape=(), name="doc", dtype=tf.string)

        x1 = vectorizer(query_input)
        x2 = vectorizer(doc_input)

        x1 = embeddings(x1) # query features
        x2 = embeddings(x2) # doc features

        # create two siamese LSTM networks
        model_lstm = LSTM(self.lstm_hidden_size, return_sequences=False)
        # model1_lstm = LSTM(self.lstm_hidden_size, return_sequences=False)
        # model2_lstm = LSTM(self.lstm_hidden_size, return_sequences=False)

        # pass the features to the LSTM networks
        x1 = model_lstm(x1)
        # x1 = keras.layers.Flatten()(x1)
        x2 = model_lstm(x2)
        # x2 = keras.layers.Flatten()(x2)

        # batch normalization
        x1 = keras.layers.BatchNormalization()(x1)
        x2 = keras.layers.BatchNormalization()(x2)

        # compute cosine similarity between x1 and x2 vectors
        x = CosineSimilarityLayer()(x1, x2)
        # compute sigmoid
        output = tf.keras.layers.Activation('sigmoid')(x)
        # compute the distance between x1 and x2 vectors
        # output = tf.reduce_sum(tf.keras.layers.Subtract()([x1, x2]))

        model = keras.Model(inputs=[query_input, doc_input], outputs=output, name=self.name)
        if verbose: model.summary()
        return model


