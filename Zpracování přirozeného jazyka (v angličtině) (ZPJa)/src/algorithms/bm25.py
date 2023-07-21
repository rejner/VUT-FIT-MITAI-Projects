from rank_bm25 import BM25Okapi
import numpy as np
import pandas as pd
from nltk import WordNetLemmatizer, PorterStemmer, word_tokenize, download
# download('punkt')
# download('wordnet')
# download('omw-1.4')

class BM25:
    
    def __init__(self, corpus: pd.DataFrame) -> None:
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = PorterStemmer()
        # 1. tokenize corpus
        self.corpus = corpus
        tokenized_corpus = [self.preprocess_text(doc) for doc in corpus['text']]
        self.corpus_len = len(tokenized_corpus)
        self.bm25 = BM25Okapi(tokenized_corpus)
        print(f"[INFO] BM25 vocab size: {len(self.bm25.idf)}")

    
    def retrieve_n_documents(self, query, n=10):
        tokenized_query = self.preprocess_text(query)
        scores = self.bm25.get_scores(tokenized_query)
        indices = np.argsort(scores)[::-1]

        return indices[:n if n < self.corpus_len else -1], self.corpus['text'].iloc[indices].iloc[:n], scores[indices][:n]
    
    # Tokenize -> stem -> lemmatize input text sequence
    def preprocess_text(self, text):
        tokens = word_tokenize(text)
        stemmed_tokens = [self.stemmer.stem(token) for token in tokens]
        return stemmed_tokens 
