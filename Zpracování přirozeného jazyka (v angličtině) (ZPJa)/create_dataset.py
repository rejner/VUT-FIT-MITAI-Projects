from src.datasets.ms_marco import MSMarcoPassageRankingDataset
import src.datasets.utils.tf_records_utils as tf_records_utils

def create_binary_labels(corpus_path, queries_path, qrel_path, output_path, n_rows=None, shuffle=True):
    marco = MSMarcoPassageRankingDataset(corpus_path=corpus_path, queries_path=queries_path, qrel_path=qrel_path, n_rows=n_rows, shuffle=True) # n_rows=None means all rows
    marco.create_binary_labels_dataset()
    print("Size of dataset: ", marco.df.shape[0]) 
    tf_records_utils.pandas_to_tf_record(output_path, marco.df, tf_records_utils.DatasetFormat.BINARY_LABELS)

def create_multiclass(corpus_path, queries_path, qrel_path, output_path, n_rows=None, shuffle=True):
    marco = MSMarcoPassageRankingDataset(corpus_path=corpus_path, queries_path=queries_path, qrel_path=qrel_path, n_rows=n_rows, shuffle=True)
    marco.create_multiclass_labels_dataset()
    print("Size of dataset: ", marco.df.shape[0]) 
    tf_records_utils.pandas_to_tf_record(output_path, marco.df, tf_records_utils.DatasetFormat.MULTICLASS_LABELS)

if __name__ == "__main__":
    # corpus is common for both train and evaluation dataset
    corpus_path = "datasets/MSMARCO/collection.tsv"

    # train dataset
    queries_path = "datasets/MSMARCO/queries.train.tsv"
    qrel_path = "datasets/MSMARCO/qrels.train.tsv"
    output_path = "datasets/custom/binary_labels.tfrecord"

    # evaluation dataset
    # queries_path = "datasets/MSMARCO/queries.eval.tsv"
    # qrel_path = "datasets/MSMARCO/qrels.eval.tsv"
    # output_path = "datasets/custom/binary_labels_eval.tfrecord"

    create_binary_labels(corpus_path, queries_path, qrel_path, output_path, n_rows=None, shuffle=True)
    # create_multiclass(corpus_path, queries_path, qrel_path, output_path, n_rows=None, shuffle=True)