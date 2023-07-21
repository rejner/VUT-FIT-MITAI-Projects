import keras
import tensorflow as tf
from keras.layers import LSTM, TextVectorization
from src.models.architectures.layers.GLoVe_embeddings import GLoVeEmbeddings
from src.models.architectures.layers.cosine_similarity_layer import CosineSimilarityLayer
from keras import layers
from keras import backend as K

from src.models.architectures.utils.math import cosine_distance

# Siamese LSTM architecture in Keras using Keras API for TensorFlow backend
class SiameseLSTM_v3():

    def __init__(self, trainable=False, lstm_hidden_size=1024, name="SiameseLSTM"):
        self.trainable = trainable
        self.lstm_hidden_size = lstm_hidden_size
        self.name = name

    def build_embedding_part(self, vectorizer: TextVectorization, embeddings: GLoVeEmbeddings, verbose=False):
        
        # embeddings = GLoVeEmbeddings(vectorizer)
        
        query_input = keras.Input(shape=(), name="query", dtype=tf.string)
        doc_input = keras.Input(shape=(), name="doc", dtype=tf.string)

        x1 = vectorizer(query_input)
        x2 = vectorizer(doc_input)

        x1 = embeddings(x1)
        x2 = embeddings(x2)

        model = keras.Model(inputs=[query_input, doc_input], outputs=[x1, x2], name=f"{self.name}-embedding_part")
        return model

    def build_lstm_part(self, verbose=False):
        x1_input = keras.Input(shape=(128, 100), name="x1")
        x2_input = keras.Input(shape=(128, 100), name="x2")

        # create two siamese LSTM networks
        lstm = LSTM(self.lstm_hidden_size, return_sequences=True)

        # pass the features to the LSTM networks
        x1 = lstm(x1_input)
        x1 = layers.Flatten()(x1)
        x2 = lstm(x2_input)
        x2 = layers.Flatten()(x2)

        x3 = layers.Subtract()([x1, x2]) # calculate the difference between x1 and x2
        x4 = layers.Lambda(cosine_distance)([x1, x2]) # calculate the cosine distance between x1 and x2

        conc = layers.Concatenate()([x3, x4]) # concatenate the difference and cosine distance

        x = layers.Dense(100, activation='relu', name="conc_layer")(conc)
        x = layers.Dropout(0.01)(x)
        output = layers.Dense(1, activation='sigmoid', name="output_layer")(x)

        model = keras.Model(inputs=[x1_input, x2_input], outputs=output, name=f"{self.name}-lstm_part")
        if verbose: model.summary()
        return model

    def build(self, vectorizer: TextVectorization, embeddings: GLoVeEmbeddings, verbose=False) -> tuple[keras.Model, keras.Model, keras.Model]:
        
        embeddings_model = self.build_embedding_part(vectorizer, embeddings, verbose)
        print("Embeddings model built")
        lstm_model = self.build_lstm_part(verbose)
        print("LSTM model built")

        full_model = keras.Model(inputs=embeddings_model.input, outputs=lstm_model(embeddings_model.output), name=self.name)
        print("Full model built")
        
        if verbose: full_model.summary()
        return (full_model, embeddings_model, lstm_model)
