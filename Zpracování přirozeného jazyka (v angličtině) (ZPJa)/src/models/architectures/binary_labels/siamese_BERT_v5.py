import keras
import tensorflow as tf
from keras import layers
import tensorflow_hub as hub
import tensorflow_text as text

from src.models.architectures.utils.math import cosine_distance

class SiameseBERT_v5():

    def __init__(self, trainable=False, name="SiameseBERT_v5"):
        self.trainable = trainable
        self.name = name

    class BERTencoder(layers.Layer):
        def __init__(self, trainable=True, name="BERTencoder", **kwargs):
            super().__init__(name=name)
            self.trainable = trainable
            self.encoder = hub.KerasLayer(
                "https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-2_H-128_A-2/2",
                trainable=self.trainable)

        def call(self,  query_input_word_ids, query_input_mask, query_input_type_ids,
                        doc_input_word_ids, doc_input_mask, doc_input_type_ids):
            # input_ids, token_type_ids=token_type_ids, attention_mask=attention_mask
            x1 = self.encoder(
                {
                    'input_word_ids': query_input_word_ids,
                    'input_mask': query_input_mask,
                    'input_type_ids': query_input_type_ids
                }
            )
            x2 = self.encoder(
                {
                    'input_word_ids': doc_input_word_ids,
                    'input_mask': doc_input_mask,
                    'input_type_ids': doc_input_type_ids
                }
            )
            # calculate the cosine distance between x1 and x2 (needs to be here, because cases errors when importing Lambda from h5)
            # x3 = layers.Lambda(cosine_distance)([x1['pooled_output'], x2['pooled_output']]) # calculate the cosine distance between x1 and x2
            return [x1, x2]

    def build_encoder_part(self, verbose=False):
        # query['input_word_ids'], query['input_mask'], query['input_type_ids'], doc['input_word_ids'], doc['input_mask'], doc['input_type_ids']
        # inputs are preprocessed by BERT preprocessor dictionaries
        query_input_word_ids = keras.Input(shape=(128,), name="query_input_word_ids", dtype=tf.int32)
        query_input_mask = keras.Input(shape=(128,), name="query_input_mask", dtype=tf.int32)
        query_input_type_ids = keras.Input(shape=(128,), name="query_input_type_ids", dtype=tf.int32)
        
        doc_input_word_ids = keras.Input(shape=(128,), name="doc_input_word_ids", dtype=tf.int32)
        doc_input_mask = keras.Input(shape=(128,), name="doc_input_mask", dtype=tf.int32)
        doc_input_type_ids = keras.Input(shape=(128,), name="doc_input_type_ids", dtype=tf.int32)

        # query_input_word_ids = keras.Input(shape=(128,), name="query_input_word_ids", dtype=tf.int32)

        bert_encoder = self.BERTencoder(trainable=True)

        # query and doc are encoded by the BERT encoder
        x1, x2 = bert_encoder(query_input_word_ids, query_input_mask, query_input_type_ids,
                               doc_input_word_ids, doc_input_mask, doc_input_type_ids)

        # emb_sub = layers.Subtract()([x1['pooled_output'], x2['pooled_output']]) # calculate the difference between x1 and x2
        
        x_1 = layers.Dense(512, activation='relu')(x1['pooled_output']) # , kernel_regularizer=keras.regularizers.l1(0.01)
        x_2 = layers.Dense(512, activation='relu')(x2['pooled_output'])
        # drop
        x_1 = layers.Dropout(0.01)(x_1)     
        x_2 = layers.Dropout(0.01)(x_2)
        # conc
        x3 = layers.Concatenate()([x_1, x_2])
        # dense
        x3 = layers.Dense(512, activation='relu', kernel_regularizer=keras.regularizers.l1(0.0001))(x3)
        # drop
        x3 = layers.Dropout(0.01)(x3)
        # dense
        x = layers.Dense(256, activation='relu', name="conc_layer")(x3)
        output = layers.Dense(1, activation='sigmoid', name="output_layer")(x)

        model = keras.Model(inputs=[query_input_word_ids, query_input_mask, query_input_type_ids, doc_input_word_ids, doc_input_mask, doc_input_type_ids], outputs=output, name=f"{self.name}-bert_part")
        if verbose: model.summary()
        return model

    def build(self, verbose=False, **kwargs) -> tuple[keras.Model, keras.Model, keras.Model]:
    
        encoder_model = self.build_encoder_part(verbose)
        print("Encoder model built")

        if verbose: encoder_model.summary()
        return encoder_model
