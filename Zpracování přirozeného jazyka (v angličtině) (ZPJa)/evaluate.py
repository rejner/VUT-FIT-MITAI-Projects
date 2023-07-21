
import tensorflow as tf
import time
import pandas as pd
import tqdm
import numpy as np
import pickle
import matplotlib.pyplot as plt
import tensorflow_hub as hub
from src.algorithms.bm25 import BM25
from src.models.architectures.binary_labels.siamese_BERT_v2 import SiameseBERT_v2
from src.models.architectures.binary_labels.siamese_BERT_v2_1 import SiameseBERT_v2_1
from src.models.architectures.binary_labels.siamese_CNN_v4 import SiameseCNN_v4
from src.models.architectures.binary_labels.siamese_LSTM_v6 import SiameseLSTM_v6
from src.models.architectures.layers.GLoVe_embeddings import load_vectorizer, load_glove_embeddings
import src.datasets.utils.tf_records_utils as tf_records_utils
from src.models.backend.metrics import thresholded_accuracy

def load_MSMARCO_passage_data(corpus_path, queries_path, qrel_path, n_rows) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df_corpus = pd.read_csv(corpus_path, sep='\t', nrows=n_rows, header=None, usecols=[0, 1], names=['docID', 'text'])
    df_queries = pd.read_csv(queries_path, sep='\t', header=None, usecols=[0, 1], names=['queryID', 'query'])
    df_qrel = pd.read_csv(qrel_path, sep='\t', header=None, usecols=[0, 2], names=['queryID', 'docID'])
    return df_corpus, df_queries, df_qrel

# each data point contains (text, query, label), where label is either 1 (positive) or 0 (negative)
def get_dataset_subset_binary_labels(corpus_path, queries_path, qrel_path, n_rows=1000, shuffle=False):
    df_corpus, df_queries, df_qrel = load_MSMARCO_passage_data(corpus_path, queries_path, qrel_path, n_rows)

    # take only relevances of docIDs, which are present in corpus subset
    df_qrel = df_qrel[df_qrel['docID'] < n_rows]
    # now merge on querryID, resulting df will contain only queries, which appeared in some relevance
    # final columns of this merge will be: 'queryID', 'query (text)', 'docID (relevant doc)'
    df_qrel = pd.merge(df_queries, df_qrel, on="queryID")
    df_positive =  pd.merge(df_corpus, df_qrel, on="docID")
    df_positive['label'] = 1
    
    df_union = pd.merge(df_corpus, df_qrel, how='outer', on="docID")
    df_negative = df_union[df_union.isnull().any(axis=1)].copy().reset_index()
    df_negative = df_negative[:df_positive.shape[0]] # create same # of positive/negative samples
    s = df_positive['query'].sample(len(df_negative), random_state=42, replace=True).reset_index()
    df_negative['query'] = s['query']
    df_negative['label'] = 0
    df_negative = df_negative[['query', 'text', 'label']]
    df_positive = df_positive[['query', 'text', 'label']]
    df = pd.concat([df_negative, df_positive])
    if shuffle:
        df = df.sample(frac = 1).reset_index()

    return df_corpus, df_qrel, df

def process_by_BM25(n_rows=10000):
    df_corp, df_qrel, _ = get_dataset_subset_binary_labels(
                        corpus_path="datasets/MSMARCO/collection.tsv",
                        queries_path="datasets/MSMARCO/queries.train.tsv",
                        qrel_path="datasets/MSMARCO/qrels.train.tsv",
                        n_rows=n_rows)
    bm25 = BM25(df_corp)

    match_cnt = 0
    for i, row in tqdm.tqdm(df_qrel.iterrows(), desc="Evaluation progress", total=df_qrel.shape[0]):
        query = row['query']
        mostRelevantDoc = row['docID']
        indices, texts, scores = bm25.retrieve_n_documents(query, n=100)
        top_indices, top_texts, top_scores = indices[:5], texts[:5], scores[:5]
        if mostRelevantDoc in top_indices: match_cnt += 1
    
    print(f"Accuracy: {match_cnt/df_qrel.shape[0]} ({match_cnt}/{df_qrel.shape[0]})")

def prepare_dataset(tf_resords_path=["datasets/custom/binary_labels.tfrecord"]):
    # load dataset
    dataset_size = tf_records_utils.count_samples_in_tfrecords(tf_resords_path)
    dataset = tf_records_utils.load_tf_records(tf_resords_path)

    vectorizer = load_vectorizer("embeddings/vectorizer_40000_128_full.pickle")
    embeddings = load_glove_embeddings("embeddings/embeddings_40000_128_full.pickle")

    dataset_size -= 1
    # split dataset into train, validation and test
    train_size = int(0.8 * dataset_size)
    val_size = int(0.1 * dataset_size)
    test_size = int(0.1 * dataset_size)
    train_dataset = dataset.take(train_size)
    val_dataset = dataset.skip(train_size).take(val_size)
    test_dataset = dataset.skip(train_size + val_size).take(test_size)

    return (train_dataset, val_dataset, test_dataset), (train_size, val_size, test_size), embeddings, vectorizer

def measure_ranking_accuracy(bm25: BM25, model, df, top_k, embeddings, vectorizer, bert_preprocessing=None, samples=1000, k_rerank_only=True):
        bm25_ranks = []
        bm25_match_cnt = 0
        bm25_parcial_precisions = []
        bm25_parcial_recalls = []
        model_ranks = []
        model_match_cnt = 0
        model_parcial_precisions = []
        model_parcial_recalls = []
        data_len = samples
        
        for i, query in tqdm.tqdm(enumerate(df['query'].unique()[:samples]), desc="Evaluation progress", total=data_len):
            df_query = df[df['query'] == query]
            mostRelevantDocIDs = df_query['docID'].values
            indices, texts, scores = bm25.retrieve_n_documents(query, n=100)
            k_indices, k_texts, k_scores = indices[:top_k], texts.iloc[:top_k], scores[:top_k]
            # if any of most relevant Document ids is in top 20 retrieved by BM25

            # ---- BM25 measure ----
            precision = 0
            matches_for_query = 0
            if any([docID in k_indices for docID in mostRelevantDocIDs]):
                bm25_match_cnt += 1 
            
            tmp_ranks = []
            for docID in mostRelevantDocIDs:
                if docID in k_indices:
                    matches_for_query += 1
                    # indices is a numpy array, so we can use index method to get the rank of the document
                    tmp_ranks.append(k_indices.tolist().index(docID) + 1)
                    precision += 1

            bm25_ranks.append(tmp_ranks.copy())
            bm25_parcial_precisions.append(precision/top_k)
            bm25_parcial_recalls.append(matches_for_query/len(mostRelevantDocIDs))

            # ---- Model measure ----

            # convert query and texts to byte strings
            # copy query to all documents in tensorflow
            query_pred = tf.constant([query] * len(k_texts if k_rerank_only else texts), dtype=tf.string)
            texts_pred = tf.constant(k_texts if k_rerank_only else texts, dtype=tf.string)
            # convert query_pred and texts_pred to byte strings
            

            if not bert_preprocessing:
                query_pred = vectorizer(query_pred)
                texts_pred = vectorizer(texts_pred)
                query_pred = embeddings(query_pred)
                texts_pred = embeddings(texts_pred)
            else:
                query_pred = bert_preprocessing(query_pred)
                texts_pred = bert_preprocessing(texts_pred)
                query_pred = query_pred['input_word_ids'], query_pred['input_mask'], query_pred['input_type_ids']
                texts_pred = texts_pred['input_word_ids'], texts_pred['input_mask'], texts_pred['input_type_ids']
            
            # inputs=[query_input_word_ids, query_input_mask, query_input_type_ids, doc_input_word_ids, doc_input_mask, doc_input_type_ids]
            pred = model.predict([query_pred, texts_pred], verbose=0)

            # sort by relevance, keep indices
            sorted_indices = tf.argsort(pred, axis=0, direction='DESCENDING')

            # get top 5 indices
            top_k_indices = sorted_indices[:top_k]
            top_k_indices = indices[top_k_indices]
            # reshape from (5, 1) to (5,)
            top_k_indices = tf.reshape(top_k_indices, (top_k,))
            # check if most relevant doc is in top 5
            if any([docID in mostRelevantDocIDs for docID in top_k_indices]):
                model_match_cnt += 1
            
            precision = 0
            matches_for_query = 0
            tmp_ranks = []
            for docID in mostRelevantDocIDs:
                if docID in top_k_indices:
                    matches_for_query += 1
                    # indices is a numpy array, so we can use index method to get the rank of the document
                    tmp_ranks.append(list(top_k_indices.numpy()).index(docID) + 1)
                    precision += 1

            model_ranks.append(tmp_ranks.copy())
            model_parcial_precisions.append(precision/top_k)
            model_parcial_recalls.append(matches_for_query/len(mostRelevantDocIDs))

        # calculate metrics for information retrieval task
        print(f"BM25 Accuracy: {bm25_match_cnt/data_len} ({bm25_match_cnt}/{data_len})")
        # print(f"BM25 Precision@{top_k}: {np.mean(bm25_parcial_precisions):.4f}")
        print(f"BM25 Recall@{top_k}: {np.mean(bm25_parcial_recalls):.4f}")
        print(f"BM25 Mean rank: {np.mean([np.min(rank) for rank in bm25_ranks if len(rank) > 0])}")

        # calculate mean reciprocal rank, where each entry in rank is an array with all ranks for a given query
        mrr = np.mean([1/np.min(rank) for rank in bm25_ranks if len(rank) > 0])
        print(f"BM25 Mean reciprocal rank: {mrr:.4f}") 

        # calculate metrics for information retrieval task
        if not k_rerank_only:
            print(f"Model Accuracy: {model_match_cnt/data_len} ({model_match_cnt}/{data_len})")
            print(f"Model Recall@{top_k}: {np.mean(model_parcial_recalls):.4f}")
        # print(f"Model Precision@{top_k}: {np.mean(model_parcial_precisions):.4f}")
        print(f"Model Mean rank: {np.mean([np.min(rank) for rank in model_ranks if len(rank) > 0])}")

        # calculate mean reciprocal rank, where each entry in rank is an array with all ranks for a given query
        mrr = np.mean([1/np.min(rank) for rank in model_ranks if len(rank) > 0])
        print(f"Model Mean reciprocal rank: {mrr:.4f}") 

        # plot scatter plot of ranks
        plt.scatter(range(len([rank for rank in bm25_ranks])), [np.min(rank) if len(rank) > 0 else None for rank in bm25_ranks], s=20)
        # add another scatter plot to the same plot with different color and lesser size
        plt.scatter(range(len([rank for rank in model_ranks])), [np.min(rank) if len(rank) > 0 else None for rank in model_ranks], color='orange', s=15)
        # add scatter plot for model predictions which were ranked better than bm25
        plt.scatter(range(len([rank for rank in model_ranks])), [np.min(rank) if len(rank) > 0 and (len(bm25_ranks[i]) == 0 or np.min(rank) < np.min(bm25_ranks[i])) else None for i, rank in enumerate(model_ranks)], color='green', s=15)
        # add scatter plot for model predictions which were ranked worse than bm25
        plt.scatter(range(len([rank for rank in model_ranks])), [np.min(rank) if (len(rank) > 0 and len(bm25_ranks[i]) > 0) and np.min(rank) > np.min(bm25_ranks[i]) else None for i, rank in enumerate(model_ranks)], color='red', s=15)

        # count number of time model ranked better than bm25
        better_cnt = 0
        worse_cnt = 0
        equal_cnt = 0
        better_ranks_diff = []
        worse_ranks_diff = []
        for i, rank in enumerate(model_ranks):
            if len(rank) > 0 and (len(bm25_ranks[i]) == 0 or np.min(rank) < np.min(bm25_ranks[i])):
                better_cnt += 1
                if len(bm25_ranks[i]) > 0:
                    better_ranks_diff.append(np.min(bm25_ranks[i]) - np.min(rank))
            elif (len(rank) > 0 and len(bm25_ranks[i]) > 0) and np.min(rank) > np.min(bm25_ranks[i]):
                worse_cnt += 1
                worse_ranks_diff.append(np.min(rank) - np.min(bm25_ranks[i]))
            elif len(rank) > 0 and len(bm25_ranks[i]) > 0 and np.min(rank) == np.min(bm25_ranks[i]):
                equal_cnt += 1
        
        total_cnt = better_cnt + worse_cnt + equal_cnt
    	
        print(f"Model ranked better than BM25: {better_cnt}/{total_cnt} ({better_cnt/total_cnt*100:.2f}%)")
        print(f"Model ranked worse than BM25: {worse_cnt}/{total_cnt} ({worse_cnt/total_cnt*100:.2f}%)")
        print(f"Model ranked equal to BM25: {equal_cnt}/{total_cnt} ({equal_cnt/total_cnt*100:.2f}%)")
        print(f"Mean rank difference when model ranked better than BM25: {np.mean(better_ranks_diff):.2f}")
        print(f"Mean rank difference when model ranked worse than BM25: {np.mean(worse_ranks_diff):.2f}")
        print(f"Max rank difference when model ranked better than BM25: {np.max(better_ranks_diff):.2f}")
        print(f"Max rank difference when model ranked worse than BM25: {np.max(worse_ranks_diff):.2f}")

        #set legend
        plt.legend(["BM25 rank", "Model rank", "Model rank better than BM25", "Model rank worse than BM25"], loc='upper right')
        # add grid lines for better visualization, frequency of grid lines is 1
        # set x axis to count from 0 to 100 with step 1, but set labels only from 0 to 100 with step 10
        # labels should be none, every 10th label will be shown

        # create list of 100 None values
        labels = [None] * samples
        # set every 10th label to 0, 10, 20, 30, ...
        labels[::10] = np.arange(0, samples, 10)
        plt.xticks(np.arange(0, samples, 1), labels)
    

        # plt.xticks(np.arange(0, 100, 1), np.arange(0, 100, 10))
        plt.grid(axis='x', alpha=0.5, linestyle='--', linewidth=0.5)


        plt.title("Ranks")
        # plt.show()

        # plt.title("Ranks (logaritmic scale)")
        # # set y to logaritmic scale
        # plt.yscale('log')
        # plt.show()
        
        # # plot scatter plot of ranks
        # plt.scatter(range(len([rank for rank in model_ranks])), [np.min(rank) if len(rank) > 0 else None for rank in model_ranks])
        # # set name to plot
        # plt.title("Model ranks")
        # plt.show()

def main():
    # train, validation and test dataset + sizes
    splits, sizes, embeddings, vectorizer = prepare_dataset(tf_resords_path=["datasets/custom/binary_labels_small.tfrecord"])

    arch_specs = [ 
        {
            'arch': SiameseBERT_v2(),
            'loss': tf.keras.losses.BinaryCrossentropy(),
            'metrics': [thresholded_accuracy],
            'preprocessing': hub.load('https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/1'),
            'weights': 'weights/BERT_V2_30.h5',
        },
        {
            'arch': SiameseBERT_v2_1(),
            'loss': tf.keras.losses.BinaryCrossentropy(),
            'metrics': [thresholded_accuracy],
            'preprocessing': hub.load('https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/1'),
            'weights': 'weights/BERT_V2_1_30.h5',
        },
        {
            'arch': SiameseCNN_v4(),
            'loss': tf.keras.losses.BinaryCrossentropy(),
            'metrics': [thresholded_accuracy],
            'preprocessing': None,
            'weights': 'weights/CNN_v4_30.h5',
        },
        {
            'arch': SiameseLSTM_v6(),
            'loss': tf.keras.losses.BinaryCrossentropy(),
            'metrics': [thresholded_accuracy],
            'preprocessing': None,
            'weights': 'weights/LSTM_v6_30.h5',
        }
    ]

    evaluation_timestamp = time.strftime('%Y%m%d-%H%M%S')
    logs = "logs/" + evaluation_timestamp

    for k in [5, 10]:
        print(f"\n\nEvaluating k={k}\n\n")
        
        for arch_spec in arch_specs:
            arch = arch_spec['arch']
            preprocessing = arch_spec['preprocessing']
            model = arch.build(verbose=False)
            model: tf.keras.Model = model
            model.compile(
                optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
                loss=arch_spec['loss'],
                metrics=arch_spec['metrics']
            )
            model.load_weights(arch_spec['weights'])

            print(f"\n\nEvaluating model: {model.name}\n\n")

            # load bm25 model from pickle file
            with open('bm25_eval_model.pkl', 'rb') as f:
                bm25 = pickle.load(f)
            
            with open('df_eval_corpus.pkl', 'rb') as f:
                df_corp = pickle.load(f)
            
            with open('df_eval_qrel.pkl', 'rb') as f:
                df_qrel = pickle.load(f)

            measure_ranking_accuracy(bm25, model, df_qrel, k, embeddings, vectorizer, bert_preprocessing=preprocessing, samples=1000, k_rerank_only=True)


if __name__ == "__main__":
    main()

