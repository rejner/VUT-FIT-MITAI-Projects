import keras
import tensorflow as tf
from keras.layers import TextVectorization, Conv1D, MaxPooling1D, Flatten
from architectures.layers.GLoVe_embeddings import GLoVeEmbeddings
from keras import layers
import tensorflow_hub as hub
import tensorflow_text as text

from architectures.utils.math import cosine_distance

class SiameseBERT_v1():

    def __init__(self, trainable=False, name="SiameseBERT_v1"):
        self.trainable = trainable
        self.name = name

    class BERTencoder(layers.Layer):
        def __init__(self, trainable=True, name="BERTencoder"):
            super().__init__(name=name)
            self.trainable = trainable
            self.preprocess = hub.load('https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/1')
            self.encoder = hub.KerasLayer(
                "https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-2_H-128_A-2/2",
                trainable=self.trainable)

        def call(self, inputs):
            x1, x2 = inputs
            x1 = self.preprocess(x1)
            x2 = self.preprocess(x2)
            x1 = self.encoder(x1)
            x2 = self.encoder(x2)
            return [x1, x2]

    def build_encoder_part(self, verbose=False):
                
        query_input = keras.Input(shape=(), name="query", dtype=tf.string)
        doc_input = keras.Input(shape=(), name="doc", dtype=tf.string)

        bert_encoder = self.BERTencoder(trainable=True)

        # query and doc are encoded by the BERT encoder
        x1, x2 = bert_encoder([query_input, doc_input])

        x3 = layers.Subtract()([x1['default'], x2['default']]) # calculate the difference between x1 and x2
        x4 = layers.Lambda(cosine_distance)([x1['default'], x2['default']]) # calculate the cosine distance between x1 and x2

        conc = layers.Concatenate()([x3, x4]) # concatenate the difference and cosine distance

        x = layers.Dense(256, activation='relu', name="conc_layer")(conc)
        x = layers.Dropout(0.01)(x)
        output = layers.Dense(1, activation='sigmoid', name="output_layer")(x)

        model = keras.Model(inputs=[query_input, doc_input], outputs=output, name=f"{self.name}-bert_part")
        if verbose: model.summary()
        return model

    def build(self, verbose=False, **kwargs) -> tuple[keras.Model, keras.Model, keras.Model]:
    
        encoder_model = self.build_encoder_part(verbose)
        print("Encoder model built")
        
        if verbose: encoder_model.summary()
        return (encoder_model, None, encoder_model)
