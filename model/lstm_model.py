import pandas as pd
import numpy as np

import tensorflow as tf
from tensorflow.keras.layers import LSTM,Embedding,Dense,Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam


class Model:

    def __init__(self,max_len,vocab_size,embedding_dim=64):
        self.max_len = max_len
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
    
    def build_model(self):
        model = Sequential()
        model.add(Embedding(self.vocab_size, self.embedding_dim, input_length=self.max_len))
        model.add(LSTM(128,return_sequences = True, dropout = 0.2))
        model.add(LSTM(128, dropout = 0.2))
        model.add(Dense(self.vocab_size, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.001))
        return model
    
    def build_summary(self,model):
        return model.summary()
    
    def train(self,model,X,y,epochs=100,batch_size=128):
        model.fit(X,y,epochs=epochs,batch_size=batch_size)
        return model
    
    def store_weights(self,model,weights_path):
        model.save_weights(weights_path)
    
    def load_weights(self,model,weights_path):
        model.load_weights(weights_path)
        return model
    