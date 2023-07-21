import tensorflow as tf

# create enum for dataset types
class DatasetFormat():
    BINARY_LABELS = 1
    MULTICLASS_LABELS = 2

def create_tf_records_example_binary_labels(features):
    tf_example = tf.train.Example(
        features=tf.train.Features(feature={
            'query': tf.train.Feature(bytes_list=tf.train.BytesList(
                value=[features[0].encode('utf-8')])),
            'doc': tf.train.Feature(bytes_list=tf.train.BytesList(
                value=[features[1].encode('utf-8')])),
            'label': tf.train.Feature(float_list=tf.train.FloatList(
                value=[features[2]])),
    }))
    return tf_example

def create_tf_records_example_multiclass_labels(features):
    # the features are: (string, array of strings, array of floats)
    tf_example = tf.train.Example(
        features=tf.train.Features(feature={
            'query': tf.train.Feature(bytes_list=tf.train.BytesList(
                value=[features[0].encode('utf-8')])),
            'docs': tf.train.Feature(bytes_list=tf.train.BytesList(
                value=[doc.encode('utf-8') for doc in features[1]])),
            'labels': tf.train.Feature(float_list=tf.train.FloatList(
                value=[label for label in features[2]])),
    }))

    return tf_example

#Reading the TFRecord
def read_tfrecord_binary_labels(example):
    LABELED_TFREC_FORMAT = {
        "query": tf.io.FixedLenFeature([], tf.string), 
        "doc": tf.io.FixedLenFeature([], tf.string),
        "label": tf.io.FixedLenFeature([], tf.float32),
    }
    
    example = tf.io.parse_single_example(example, LABELED_TFREC_FORMAT)
    query = example['query']
    doc = example['doc']
    label = example['label']
    return query, doc, label

def read_tfrecord_multiclass_labels(example):
    LABELED_TFREC_FORMAT = {
        "query": tf.io.FixedLenFeature([], tf.string), 
        "docs": tf.io.FixedLenFeature([100,], tf.string),
        "labels": tf.io.FixedLenFeature([100,], tf.float32),
    }
    
    example = tf.io.parse_single_example(example, LABELED_TFREC_FORMAT)
    query = example['query']
    docs = example['docs']
    labels = example['labels']
    return query, docs, labels

# Load the TFRecord
def load_tf_records(filenames, dtype=DatasetFormat.BINARY_LABELS):
    dataset = tf.data.TFRecordDataset(filenames, num_parallel_reads=tf.data.experimental.AUTOTUNE) # automatically interleaves reads from multiple files
    if dtype == DatasetFormat.BINARY_LABELS:
        dataset = dataset.map(read_tfrecord_binary_labels)
    elif dtype == DatasetFormat.MULTICLASS_LABELS:
        dataset = dataset.map(read_tfrecord_multiclass_labels)
    else:
        raise ValueError("Invalid dataset type")
    return dataset

# Writing the TFRecord
def pandas_to_tf_record(out_path, df, dtype=DatasetFormat.BINARY_LABELS):
    writer = tf.io.TFRecordWriter(out_path)
    # iterate over rows of dataframe
    for index, row in df.iterrows():
        features = row.values
        if dtype == DatasetFormat.BINARY_LABELS:
            example = create_tf_records_example_binary_labels(features)
        elif dtype == DatasetFormat.MULTICLASS_LABELS:
            example = create_tf_records_example_multiclass_labels(features)
        else:
            raise ValueError("Invalid dataset type")
        writer.write(example.SerializeToString())

def count_samples_in_tfrecords(filenames):
    c = 0
    for fn in filenames:
        for record in tf.compat.v1.io.tf_record_iterator(fn):
            c += 1
    return c