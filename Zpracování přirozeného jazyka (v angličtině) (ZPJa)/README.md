# Zadání
## Varianta: Document Ranking

Implement three models for document ranking using small neural nets: CNN, LSTM, and BERT-tiny or BERT-small. Train and evaluate models on a subset of MS MACRO (passage ranking) dataset.

#### Získáno bodů: 29.6/40

# Project structure
The project is divided in the following directories and files:
- `src` - contains the source code of the project
    - `algorithms` - document retrieval algorithms
        - `bm25.py` - BM25 algorithm
    - `datasets` - dataset classes
        - `ms_marco.py` - MS MARCO dataset
        - `utils` - utilities for working with datasets
    - `models` - DL sources
        - `architectures` - DL architectures
            - `binary_labels` - architectures for binary labels
            - `multiclass_labels` - architectures for multiclass labels
            - `layers` - custom layers
        - `backend` - backend for the models
- `data` - contains the data used in the project
- `datasets` - contains the datasets used in the project
    - `MSMARCO` - MS MARCO dataset (https://microsoft.github.io/msmarco/)
        - `collection.tsv` - collection of documents
        - `queries.*.tsv` - queries
        - `qrels.*.tsv` - relevance judgements
    - `custom` - custom datasets created for the project (TFRecord format, created by create_dataset.py)
    - `glove.6B.100d.txt` - GloVe embeddings (https://nlp.stanford.edu/projects/glove/)
- `weights` - contains the weights of the trained models
- `dump` - contains prototypes and testing scripts (not used in the project directly, but could be useful for future development)
- `train.py` - script for training the models
- `train_distribute.py` - script for training the models using multiple GPUs
- `evaluate.py` - script for evaluating the models
- `create_dataset.py` - script for creating the datasets
- `save_embeddings_and_vectorizer.py` - script for saving the embeddings and vectorizer into compact format
- `requirements.txt` - requirements for the project
- `README.md` - this file



