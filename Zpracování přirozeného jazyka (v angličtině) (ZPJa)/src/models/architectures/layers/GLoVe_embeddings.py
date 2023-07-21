import keras
from keras.layers import TextVectorization, Embedding
from keras import layers
from keras import Sequential
import os
import numpy as np
import pickle


def load_glove_embeddings(path):
    glove = Sequential()
    embeddings_from_disk = pickle.load(open(path, "rb"))
    new_e = Embedding.from_config(embeddings_from_disk['config'])
    glove.add(new_e)
    new_e.set_weights(embeddings_from_disk['weights'])
    return glove

def load_vectorizer(path):
    vectorizer_from_disk = pickle.load(open(path, "rb"))
    new_v = TextVectorization.from_config(vectorizer_from_disk['config'])
    new_v.set_weights(vectorizer_from_disk['weights'])
    return new_v


class GLoVeEmbeddings(layers.Layer):

    def __init__(self, vectorizer: TextVectorization, trainable=False, name="GLoVeEmbeddings", dtype=None, dynamic=False, **kwargs):
        super().__init__(trainable, name, dtype, dynamic, **kwargs)
        self.vectorizer = vectorizer
        path_to_glove_file = os.path.join(
            "embeddings/glove.6B.100d.txt"
        )

        embeddings_index = {}
        with open(path_to_glove_file, encoding="utf-8") as f:
            for line in f:
                values = line.split()
                word = values[0]
                coefs = np.asarray(values[1:], dtype='float32')
                embeddings_index[word] = coefs

        print("Found %s word vectors." % len(embeddings_index))

        voc = self.vectorizer.get_vocabulary()
        word_index = dict(zip(voc, range(self.vectorizer.vocabulary_size())))
        num_tokens = self.vectorizer.vocabulary_size() + 2
        embedding_dim = 100
        hits = 0
        misses = 0

        # Prepare embedding matrix
        embedding_matrix = np.zeros((num_tokens, embedding_dim))
        for word, i in word_index.items():
            embedding_vector = embeddings_index.get(word)
            if embedding_vector is not None:
                # Words not found in embedding index will be all-zeros.
                # This includes the representation for "padding" and "OOV"
                embedding_matrix[i] = embedding_vector
                hits += 1
            else:
                misses += 1
        print("Converted %d words (%d misses)" % (hits, misses))

        self.embedding_layer = Embedding(
            num_tokens,
            embedding_dim,
            embeddings_initializer=keras.initializers.Constant(embedding_matrix),
            trainable=False,
        )

    def call(self, sequence):
        return self.embedding_layer(sequence)
    
    def get_config(self):
        config = super().get_config().copy()
        config.update({
            'vectorizer': self.vectorizer,
        })
        return config