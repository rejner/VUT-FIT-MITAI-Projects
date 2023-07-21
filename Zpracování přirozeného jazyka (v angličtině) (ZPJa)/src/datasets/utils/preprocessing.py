import tensorflow_hub as hub
import tensorflow as tf

def preprocess_for_bert_binary_labels(ds):
    preprocessor = hub.load('https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/1')
    def _preprocess_for_bert(query, doc, label):
        #expand query and doc dimensions
        query = preprocessor(query)
        doc = preprocessor(doc)

        #return query, doc
        return (query['input_word_ids'], query['input_mask'], query['input_type_ids'], doc['input_word_ids'], doc['input_mask'], doc['input_type_ids']), label

    return ds.map(_preprocess_for_bert, num_parallel_calls=tf.data.experimental.AUTOTUNE)

def preprocess_binary_labels(ds, embeddings, vectorizer):
    def _preprocess(query, doc, label):
        #expand query and doc dimensions
        query = vectorizer(query)
        doc = vectorizer(doc)
        query = embeddings(query)
        doc = embeddings(doc)

        #return query, doc
        return (query, doc), label

    return ds.map(_preprocess, num_parallel_calls=tf.data.experimental.AUTOTUNE)

def preprocess_multiclass_labels(ds, embeddings, vectorizer):
    def _preprocess(query, doc, label):
        #expand query and doc dimensions
        query = vectorizer(query)
        doc = tf.reshape(doc, (-1, 100, 1))
        doc = vectorizer(doc)
        query = embeddings(query)
        doc = embeddings(doc)

        #return query, doc
        return (query, doc), label

    return ds.map(_preprocess, num_parallel_calls=tf.data.experimental.AUTOTUNE)
