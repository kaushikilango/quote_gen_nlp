import pandas as pd
import numpy as np
import random
import keras
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences,to_categorical
import os

def scrutinize_dataset(data):
    tokenizer.fit_on_texts(data)
    vocab_len = 1 + len(tokenizer.word_index)
    vocab = list(tokenizer.word_index.keys())
    return vocab, vocab_len


def text_to_seq(data):
    sequences = []
    for line in data:
        sequence = tokenizer.texts_to_sequences([line])[0]
        for i in range(len(sequence)):
            sequences.append(sequence[:i+1])
    return sequences

def padding_seq(seqs,max_len):
    input_seqs = pad_sequences(seqs,max_len)
    return input_seqs

def randomize_seqs(seqs):
    indices = np.arange(seqs.shape[0])
    np.random.shuffle(indices)
    seqs = seqs[indices]
    return seqs

def input_output_seqs(seqs,vocab_len):
    X = seqs[:,:-1]
    y = seqs[:,-1]
    y = to_categorical(y,num_classes = vocab_len)
    return X,y


quote_data = pd.read_csv('/kaggle/input/quotes/sampled_quotes.csv',encoding = 'utf-8')
quote_data.head()

print(quote_data.shape)
quotes = quote_data['Quote'].drop_duplicates()
quotes = quotes.dropna()
train_quotes = quotes
print(train_quotes.shape)
quote_list = list(train_quotes)
print(quote_list[:3])
tokenizer = Tokenizer()
vocab,no_of_words = scrutinize_dataset(quotes)
sequences = text_to_seq(train_quotes)
print(sequences[:10])
max_length = max([len(x) for x in sequences])
padded_seqs = padding_seq(sequences,max_length)
print(padded_seqs[:5])
random_seqs = randomize_seqs(padded_seqs)
np.save('datasets\data.npy',random_seqs)
X,y = input_output_seqs(random_seqs,no_of_words)