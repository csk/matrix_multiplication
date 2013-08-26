import numpy as np
from random import randint


def randomized_algorithm(A, B, C, k=1):

    for i in range(0, k):
        r = np.array([randint(0, 1) for i in [1]*C.shape[1]], np.int32)  # random vector

        if not (A.dot(B.dot(r)) == C.dot(r)).all():
            return False
    return True
