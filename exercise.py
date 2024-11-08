import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sklearn
from sklearn.model_selection import train_test_split

def huber(input, delta = 1.0):
    return np.where(abs(input) < delta , 0.5 * input**2 , abs(input)-0.5)

def prediction(input, a, b):

    return input @ a + b

def loss(xs, ys, a, b):

    predictions = prediction(xs, a, b)

    return np.mean(huber((ys-predictions)))

def derivative_huber(xs):
    return np.minimum(1, np.maximum(-1, xs))

def gradient(xs, a, b, ys):

    predictions = prediction(xs, a, b)

    gradient_res_a = derivative_huber((ys-predictions)).reshape(-1, 1) * (-xs)
    gradient_res_b = -derivative_huber((ys-predictions))

    return np.mean(gradient_res_a, axis=0), np.mean(gradient_res_b)



diamonds = sns.load_dataset("diamonds")
diamonds.info()
print()

diamonds = diamonds.select_dtypes("number")

y = diamonds.pop("price").to_numpy()
X = diamonds.to_numpy()

print(y.shape)
print(X.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8)

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

from sklearn.utils import shuffle
from sklearn.metrics import r2_score

batch_size = 100
epochs = 200
learning_rate = 0.5

d = X_train.shape[1]
a = np.zeros((d,)) # we separated w into a and b
b = np.zeros((1,))

for e in range(epochs):
    X_train, y_train = shuffle(X_train, y_train, random_state=42) # re-shuffle the training data in each epoch
    maxit = X_train.shape[0] // batch_size

    print(X_train.shape)
    print(y_train.shape)
    for i in range(maxit):
        X_batch = X_train[i*batch_size : i*batch_size + batch_size]
        y_batch = y_train[i*batch_size : i*batch_size + batch_size]
        grad_a,grad_b = gradient(X_batch, a, b, y_batch)
        a -= learning_rate*grad_a
        b -= learning_rate*grad_b
        

    print(f"test Huber loss after epoch {e}:", loss(X_test, y_test, a, b))
    print(f"test R^2 after epoch {e}:", r2_score(y_test, prediction(X_test, a, b)))
    print()
