from src.models.architectures.binary_labels.siamese_BERT_v2 import SiameseBERT_v2
from src.models.architectures.binary_labels.siamese_BERT_v2_1 import SiameseBERT_v2_1
from src.models.architectures.binary_labels.siamese_CNN_v4 import SiameseCNN_v4
from src.models.architectures.binary_labels.siamese_LSTM_v6 import SiameseLSTM_v6
from src.models.architectures.layers.GLoVe_embeddings import load_glove_embeddings, load_vectorizer
import src.datasets.utils.tf_records_utils as tf_records_utils
import src.datasets.utils.preprocessing as preprocessing
from src.models.backend.metrics import thresholded_accuracy, thresholded_positive_accuracy
import tensorflow as tf
import time

def train(arch_specs, data, epochs=10, batch_size=64, lr=0.0001):

    (train_dataset, val_dataset), (train_size, val_size) = data

    training_timestamp = time.strftime('%Y%m%d-%H%M%S')
    logs = "logs/" + training_timestamp

    for arch_spec in arch_specs:
        arch = arch_spec['arch']
        loss = arch_spec['loss']
        metrics = arch_spec['metrics']
        preprocessing = arch_spec['preprocessing']

        preprocessed_train_dataset = train_dataset.shuffle(10000).batch(batch_size).apply(preprocessing).prefetch(tf.data.AUTOTUNE).repeat()
        preprocessed_val_dataset = val_dataset.shuffle(10000).batch(batch_size).apply(preprocessing).prefetch(tf.data.AUTOTUNE).repeat()

        tboard_callback = tf.keras.callbacks.TensorBoard(
            log_dir = logs + '-' + arch.name,
            histogram_freq = 0,)

        path = "weights/epochs/" + arch.name
        checkpoint_cb = tf.keras.callbacks.ModelCheckpoint(
            filepath=path + '_{epoch}.h5',
            monitor='loss',
            mode='min',
            save_weights_only=True,
            save_best_only=True)

        tf.print("Training architecture:", arch.name)
        model = arch.build(verbose=True)
        model: tf.keras.Model = model
        model.compile(
            loss=loss,
            optimizer=tf.keras.optimizers.Adam(learning_rate=lr),
            metrics=metrics,
        )

        # load weights if needed
        # model.load_weights("weights/20221211-180542-10-512-SiameseBERT_v2-bert_part.h5")

        model.fit(
            x= preprocessed_train_dataset,
            epochs=epochs,
            batch_size=batch_size,
            steps_per_epoch=train_size // batch_size,
            validation_data= preprocessed_val_dataset,
            validation_steps=val_size // batch_size,
            callbacks=[tboard_callback,  checkpoint_cb]
        )
        model.save(f"weights/{training_timestamp}-{epochs}-{batch_size}-{model.name}.h5",save_format='h5')

def prepare_dataset(dataset_type: tf_records_utils.DatasetFormat, tf_resords_path=["datasets/custom/binary_labels.tfrecord"]):
    # load dataset
    dataset_size = tf_records_utils.count_samples_in_tfrecords(tf_resords_path)
    dataset = tf_records_utils.load_tf_records(tf_resords_path, dtype=dataset_type)
    
    # take any number of samples for testing
    #dataset = dataset.take(100000)
    #dataset_size = 100000

    vectorizer = load_vectorizer("embeddings/vectorizer_40000_128_full.pickle")
    embeddings = load_glove_embeddings("embeddings/embeddings_40000_128_full.pickle")

    dataset_size -= 1
    # split dataset into train and validation
    train_size = int(0.8 * dataset_size)
    val_size = int(0.2 * dataset_size)
    train_dataset = dataset.take(train_size)
    val_dataset = dataset.skip(train_size).take(val_size)

    return (train_dataset, val_dataset), (train_size, val_size), embeddings, vectorizer
    

def main():
    EPOCHS = 30
    BATCH_SIZE = 512
    LR = 0.001

    # train, validation and test dataset + sizes
    splits, sizes, embeddings, vectorizer = prepare_dataset(tf_records_utils.DatasetFormat.BINARY_LABELS, tf_resords_path=["datasets/custom/binary_labels.tfrecord"])
    # splits, sizes, embeddings, vectorizer = prepare_dataset(tf_records_utils.DatasetFormat.MULTICLASS_LABELS, tf_resords_path=["datasets/custom/multiclass_labels_full.tfrecord"])

    arch_specs = [
        {
            'arch': SiameseLSTM_v6(),
            'loss': tf.keras.losses.BinaryCrossentropy(),
            'metrics': [thresholded_accuracy, thresholded_positive_accuracy],
            'preprocessing': lambda x: preprocessing.preprocess_binary_labels(x, embeddings, vectorizer),
        },
        {
             'arch': SiameseCNN_v4(),
             'loss': tf.keras.losses.BinaryCrossentropy(),
             'metrics': [thresholded_accuracy, thresholded_positive_accuracy],
             'preprocessing': lambda x: preprocessing.preprocess_binary_labels(x, embeddings, vectorizer),
        },
        {
             'arch': SiameseBERT_v2(),
             'loss': tf.keras.losses.BinaryCrossentropy(),
             'metrics': [thresholded_accuracy, thresholded_positive_accuracy],
             'preprocessing': preprocessing.preprocess_for_bert_binary_labels,
        },
        {
             'arch': SiameseBERT_v2_1(),
             'loss': tf.keras.losses.BinaryCrossentropy(),
             'metrics': [thresholded_accuracy, thresholded_positive_accuracy],
             'preprocessing': preprocessing.preprocess_for_bert_binary_labels,
        },
    ]

    train(arch_specs, (splits, sizes), epochs=EPOCHS, batch_size=BATCH_SIZE, lr=LR)


if __name__ == "__main__":
    main()

