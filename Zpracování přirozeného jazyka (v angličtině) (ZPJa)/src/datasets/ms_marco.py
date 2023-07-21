
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
from keras.layers import TextVectorization
import tensorflow_text as text
from src.models.architectures.layers.GLoVe_embeddings import GLoVeEmbeddings
import numpy as np

# MS MARCO Passage Ranking Dataset
class MSMarcoPassageRankingDataset():    

    def __init__(self, corpus_path="datasets/MSMARCO/collection.tsv",
                       queries_path="datasets/MSMARCO/queries.train.tsv",
                       qrel_path="datasets/MSMARCO/qrels.train.tsv",
                       n_rows=None, shuffle=False, seed=42, vocab_size=40000, sequence_length=128):
        
        self.corpus_path = corpus_path
        self.queries_path = queries_path
        self.qrel_path = qrel_path
        self.n_rows = n_rows
        self.seed = seed
        self.vocab_size = vocab_size
        self.sequence_length = sequence_length
        self.preprocess_type = None
        self.preprocess = hub.load('https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/1')

    def load_data(self):
        print("Loading data...")
        self.df_corpus = pd.read_csv(self.corpus_path, sep='\t', nrows=self.n_rows, header=None, usecols=[0, 1], names=['docID', 'text'])
        self.df_queries = pd.read_csv(self.queries_path, sep='\t', header=None, usecols=[0, 1], names=['queryID', 'query'])
        self.df_qrel = pd.read_csv(self.qrel_path, sep='\t', header=None, usecols=[0, 2], names=['queryID', 'docID'])
    
    def create_text_vectorizer_and_embeddings(self):
        self.load_data()
        print("Creating text vectorizer and embeddings...")
        # create vectorizer layer
        self.vectorizer = TextVectorization(
        max_tokens=self.vocab_size,
        output_mode='int',
        output_sequence_length=self.sequence_length)
        self.vectorizer.adapt(self.df_corpus['text'].values)
        self.glove = GLoVeEmbeddings(self.vectorizer)
        return self.vectorizer, self.glove

    def get_max_doc_len(self):
        if self.df_corpus is None:
            self.load_data()
        return self.df_corpus['text'].str.split().str.len().max()

    def get_min_doc_len(self):
        if self.df_corpus is None:
            self.load_data()
        return self.df_corpus['text'].str.split().str.len().min()
    
    def get_average_doc_len(self):
        if self.df_corpus is None:
            self.load_data()
        return self.df_corpus['text'].str.split().str.len().mean()
    
    # each data point contains (text, query, label), where label is either 1 (positive) or 0 (negative)
    def create_binary_labels_dataset(self):
        self.load_data()
        print("Creating binary labels dataset...")
        # take only relevances of docIDs, which are present in corpus subset
        df_qrel = self.df_qrel
        if self.n_rows != None:
            df_qrel = self.df_qrel[self.df_qrel['docID'] < self.n_rows]
        # now merge on querryID, resulting df will contain only queries, which appeared in some relevance
        # final columns of this merge will be: 'queryID', 'query (text)', 'docID (relevant doc)'
        df_qrel = pd.merge(self.df_queries, df_qrel, on="queryID")
        df_positive =  pd.merge(self.df_corpus, df_qrel, on="docID")
        df_positive['label'] = 1.0
        # take ony 100000 positive samples
        df_positive = df_positive[:100000]
        
        
        df_union = pd.merge(self.df_corpus, df_qrel, how='outer', on="docID")
        df_negative = df_union[df_union.isnull().any(axis=1)].copy().reset_index()
        df_negative = df_negative[:int(df_positive.shape[0]*10)] # create same # of positive/negative samples
        s = df_positive['query'].sample(len(df_negative), random_state=42, replace=True).reset_index()
        df_negative['query'] = s['query']
        df_negative['label'] = 0.0
        df_negative = df_negative[['query', 'text', 'label']]
        df_positive = df_positive[['query', 'text', 'label']]
        self.df = pd.concat([df_negative, df_positive])

        # shuffle self.df
        self.df = self.df.sample(frac=1, random_state=self.seed).reset_index(drop=True)

    # each data point contains (query, set of documents (100,), set of relevance (100,)), where label is either 1 (positive) or 0 (negative)
    def create_multiclass_labels_dataset(self):
        self.load_data()
        print("Creating multiclass problem dataset...")
        # take only relevances of docIDs, which are present in corpus subset
        df_qrel = self.df_qrel
        if self.n_rows != None:
            df_qrel = self.df_qrel[self.df_qrel['docID'] < self.n_rows]
        # now merge on querryID, resulting df will contain only queries, which appeared in some relevance
        # final columns of this merge will be: 'queryID', 'query (text)', 'docID (relevant doc)'
        df_qrel = pd.merge(self.df_queries, df_qrel, on="queryID")
        df_positive =  pd.merge(self.df_corpus, df_qrel, on="docID")
        # df_positive['label'] = 1.0
        
        df_union = pd.merge(self.df_corpus, df_qrel, how='outer', on="docID")
        df_negative = df_union[df_union.isnull().any(axis=1)].copy().reset_index()
        # now we have all negative samples, but we need to create 100 samples per query,
        # where each sample contains 100 documents and 100 relevance labels
        # and each sample must contain at least one positive sample
        # so we need to create 100 samples per query, where each sample contains < 100 negative samples and > 1 positive sample
        df = pd.DataFrame(columns=['query', 'docs', 'labels'])
        for query in df_positive['query'].unique():
            df_query = df_positive[df_positive['query'] == query]
            texts = df_query['text'].values
            labels = np.ones(len(texts))
            negative_texts = df_negative.sample(100, replace=True)[['text']].reset_index()
            negative_texts = negative_texts['text'].values
            negative_labels = np.zeros(100)
            # replace random samples of the negative samples with the positive samples
            random_indices = np.random.choice(100, len(texts), replace=False)
            for i in range(len(texts)):
                negative_texts[random_indices[i]] = texts[i]
                negative_labels[random_indices[i]] = labels[i]

            # df = df.append({'query': query, 'texts': negative_texts, 'labels': negative_labels}, ignore_index=True)
            # with pandas concat
            df = pd.concat([df, pd.DataFrame({'query': [query], 'docs': [negative_texts], 'labels': [negative_labels]})])

        # shuffle self.df
        self.df = df.sample(frac=1, random_state=self.seed).reset_index(drop=True)
        
if __name__ == "__main__":
    records_path = "datasets/custom/binary_labels.tfrecord"
    marco = MSMarcoPassageRankingDataset(n_rows=1000,)
    marco.to_tf_record(records_path)
    dataset = marco.load_tf_records([records_path])
    for query, doc, label in dataset.take(1):
        print(query)
        print(doc)
        print(label)


