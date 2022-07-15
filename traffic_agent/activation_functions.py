import numpy as np


# Standard sigmoid activation function
def sigmoid(input):
    return 1/(1+np.exp(-input))


# Standard relu
def relu(x):
    return (x > 0) * x