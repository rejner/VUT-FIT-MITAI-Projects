import src.datasets.utils.tf_records_utils as tf_records_utils
from keras.layers import TextVectorization, Embedding
from keras import Sequential
import tensorflow as tf
from src.models.architectures.layers.GLoVe_embeddings import GLoVeEmbeddings
import pickle

"""
   This script is used to save the embeddings and vectorizer on disk in pickle format,
   since adapting the vectorizer to the dataset is a time consuming operation.
"""
if __name__ == "__main__":
    tf_resords_path = ["datasets/custom/binary_labels.tfrecord"]
    vectorizer_pickle_path = "embeddings/vectorizer_40000_128_full.pickle"
    embeddings_pickle_path = "embeddings/embeddings_40000_128_full.pickle"

    # load dataset
    # dataset_size = tf_records_utils.count_samples_in_tfrecords(tf_resords_path)
    dataset = tf_records_utils.load_tf_records(tf_resords_path)

    vectorizer = TextVectorization(
        max_tokens=40000,
        output_mode='int',
        output_sequence_length=128
        )
        

    texts = dataset.map(lambda text, query, label: text, num_parallel_calls=tf.data.AUTOTUNE)
    # Make a text-only dataset (no labels) and call adapt to build the vocabulary.
    vectorizer.adapt(texts)
    embeddings = GLoVeEmbeddings(vectorizer)

    print(embeddings(vectorizer("this")))

    # embeddings.embedding_layer.trainable = True
    # save embeddings keras layer from embeddings.embeddings_layer
    pickle.dump({'config': embeddings.embedding_layer.get_config(),
                'weights': embeddings.embedding_layer.get_weights()}
                , open(embeddings_pickle_path, "wb"))

    # Pickle the config and weights
    pickle.dump({'config': vectorizer.get_config(),
                'weights': vectorizer.get_weights()}
                , open(vectorizer_pickle_path, "wb"))


    vectorizer_from_disk = pickle.load(open(vectorizer_pickle_path, "rb"))
    new_v = TextVectorization.from_config(vectorizer_from_disk['config'])
    new_v.set_weights(vectorizer_from_disk['weights'])

    glove = Sequential()
    embeddings_from_disk = pickle.load(open(embeddings_pickle_path, "rb"))
    new_e = Embedding.from_config(embeddings_from_disk['config'])
    glove.add(new_e)
    new_e.set_weights(embeddings_from_disk['weights'])
