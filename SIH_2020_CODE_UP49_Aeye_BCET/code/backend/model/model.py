'''
file name : model.py
'''

# import numpy
import numpy as np

from tensorflow import keras
from tensorflow.keras import layers, Input, Model


def create(maskValue=None) -> None:
    Input1 = Input(shape=(34), name='static')
    Dense1 = layers.Dense(35, activation='relu')(Input1)
    Dense2 = layers.Dense(35, activation='relu')(Dense1)
    Dropout1 = layers.Dropout(0.5)(Dense2)

    Input2 = Input(shape=(None, 8), name='timeSeries')
    Masking1 = layers.Masking(mask_value=maskValue)(Input2)
    RNN1 = layers.LSTM(9, return_sequences=True)(Masking1)
    RNN2 = layers.LSTM(9)(RNN1)

    concatenated = layers.concatenate([Dropout1, RNN2], axis=-1)
    Dense4 = layers.Dense(45, activation='relu')(concatenated)
    Dense5 = layers.Dense(45, activation='relu')(Dense4)
    Dropout2 = layers.Dropout(0.5)(Dense5)
    output = layers.Dense(1, activation='sigmoid')(Dropout2)

    model = Model([Input1, Input2], output)

    METRICS = [
        keras.metrics.TruePositives(name='tp'),
        keras.metrics.FalsePositives(name='fp'),
        keras.metrics.TrueNegatives(name='tn'),
        keras.metrics.FalseNegatives(name='fn'),
        keras.metrics.BinaryAccuracy(name='accuracy'),
        keras.metrics.Precision(name='precision'),
        keras.metrics.Recall(name='recall'),
        keras.metrics.AUC(name='auc'),
    ]

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=METRICS)

    return model

