import keras
import tensorflow as tf
from keras.layers import TextVectorization, Conv1D, MaxPooling1D, Flatten
from architectures.layers.GLoVe_embeddings import GLoVeEmbeddings
from keras import layers

from architectures.utils.math import cosine_distance

class SiameseCNN_v1():

    def __init__(self, trainable=False, name="SiameseCNN_v1"):
        self.trainable = trainable
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

    def build_conv_part(self, verbose=False):
        x1_input = keras.Input(shape=(128, 100), name="x1")
        x2_input = keras.Input(shape=(128, 100), name="x2")

        # create two siamese LSTM networks
        conv_1 = Conv1D(512, 5, activation='relu', padding='same')
        max_pooling_1 = MaxPooling1D(5)
        conv_2 = Conv1D(256, 3, activation='relu', padding='same')
        max_pooling_2 = MaxPooling1D(3)
        conv_3 = Conv1D(128, 3, activation='relu', padding='same')
        max_pooling_3 = MaxPooling1D(3)

        x1 = conv_1(x1_input)
        x1 = max_pooling_1(x1)
        x1 = conv_2(x1)
        x1 = max_pooling_2(x1)
        x1 = conv_3(x1)
        x1 = max_pooling_3(x1)
        x1 = Flatten()(x1)

        x2 = conv_1(x2_input)
        x2 = max_pooling_1(x2)
        x2 = conv_2(x2)
        x2 = max_pooling_2(x2)
        x2 = conv_3(x2)
        x2 = max_pooling_3(x2)
        x2 = Flatten()(x2)

        

        x3 = layers.Subtract()([x1, x2]) # calculate the difference between x1 and x2
        x4 = layers.Lambda(cosine_distance)([x1, x2]) # calculate the cosine distance between x1 and x2

        conc = layers.Concatenate()([x3, x4]) # concatenate the difference and cosine distance

        x = layers.Dense(256, activation='relu', name="conc_layer")(conc)
        x = layers.Dropout(0.01)(x)
        output = layers.Dense(1, activation='sigmoid', name="output_layer")(x)

        model = keras.Model(inputs=[x1_input, x2_input], outputs=output, name=f"{self.name}-conv_part")
        if verbose: model.summary()
        return model

    def build(self, vectorizer: TextVectorization, embeddings: GLoVeEmbeddings, verbose=False) -> tuple[keras.Model, keras.Model, keras.Model]:
        
        embeddings_model = self.build_embedding_part(vectorizer, embeddings, verbose)
        print("Embeddings model built")

        conv_model = self.build_conv_part(verbose)
        print("Convolution model built")

        full_model = keras.Model(inputs=embeddings_model.input, outputs=conv_model(embeddings_model.output), name=self.name)
        print("Full model built")
        
        if verbose: full_model.summary()
        return (full_model, embeddings_model, conv_model)
