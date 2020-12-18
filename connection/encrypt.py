import numpy as np


def encrypt_str(nparray, string):
    result = np.zeros(nparray.shape).flatten()
    for index, char in enumerate(string):
        result[index] += ord(char)
    return np.matmul(nparray, np.reshape(result, nparray.shape))

def decrypt_str(nparray, shared):
    result = ''
    arr = np.matmul(np.linalg.inv(shared), nparray)
    for val in arr.flatten():
        if val < 1:
            break
        result += chr(round(val))
    return result

def generate_array(dims, max: int, nptype='longlong'):
    return (np.random.rand(*dims) * max).astype(nptype)

def form_array(nparray, shared_array, is_client):
    return np.matmul(nparray, shared_array) if is_client else np.matmul(shared_array, nparray)

def get_shared(nparray, recvarray, is_client):
    return np.matmul(nparray, recvarray) if is_client else np.matmul(recvarray, nparray)

def make_no_det(nparray):
    arr = nparray
    arr[-1] = np.zeros(arr[-1].shape)
    return arr

def finish_array(shared):
    arr = shared
    arr[-1] = np.ones(arr[-1].shape)
    return arr

# Leave previous functions alone until the class is finished and functional
# Note to self: do not touch above functions


class Matrix(list):  # Make this a subclass of np.array
    def __init__(self, max_rand=30):
        self._arr = generate_array(self, max_rand)  # One of the user's private arrays

    def encrypt_str(self, str):
        pass


if __name__ == '__main__':
    dims = (450, 450)

    a = generate_array(dims, 10000000000000000000)
    b = generate_array(dims, 10000000000000000000)
    G = make_no_det(generate_array(dims, 10000))

    Ga = form_array(a, G, True)
    Gb = form_array(b, G, False)

    A = finish_array(get_shared(a, Gb, True))
    B = finish_array(get_shared(b, Ga, False))

    print('Are the final arrays equal?', (A == B).flatten()[0])
    print(decrypt_str(encrypt_str(B, 'Hello world!'), B))
