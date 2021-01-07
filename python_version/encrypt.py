import numpy as np
import math


def encrypt_str(nparray, string):
    chunks = []
    result = np.zeros(nparray.shape).flatten()
    for chunk in [string[i:i+len(result)] for i in range(0, len(string), len(result))]:
        result = np.zeros(nparray.shape).flatten()
        for index, char in enumerate(chunk):
            result[index] += ord(char)
        chunks.append(np.reshape(result, nparray.shape))
    return np.matmul(nparray, np.concatenate(chunks, axis=1))

def decrypt_str(nparray, shared):
    result = ''
    arr = np.matmul(np.linalg.inv(shared), nparray)
    for val in arr.flatten():
        if val < 1:
            break
        result += chr(round(val))
    return result

def generate_array(dims, max: int, nptype='uint16'):
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

def make_square(values, nptype='uint16'):
    nextval = math.floor(math.sqrt(len(values))) + 1
    arr = np.zeros((nextval * nextval))
    arr[:len(values)] = values
    return np.reshape(arr, (nextval, nextval)).astype(nptype)

# Leave previous functions alone until the class is finished and functional

class Matrix(list):  # Make this a subclass of np.array
    def __init__(self, max_rand=30):
        self._arr = generate_array(self, max_rand)  # One of the user's private arrays

    def encrypt_str(self, str):
        pass


if __name__ == '__main__':
    from time import perf_counter_ns

    dims = (7, 7)

    a = generate_array(dims, 255, 'uint8')
    b = generate_array(dims, 255, 'uint8')
    G = make_no_det(generate_array(dims, 255, 'uint16'))

    Ga = form_array(a, G, True)
    Gb = form_array(b, G, False)

    A = finish_array(get_shared(a, Gb, True))
    B = finish_array(get_shared(b, Ga, False))

    print('Private key is', a.nbytes * 8, 'bits')
    print('Are the final arrays equal?', (A == B).flatten()[0])
    print(decrypt_str(encrypt_str(B, 'Hello world!'), B))

    start = perf_counter_ns()
    decrypt_str(encrypt_str(B, '.'*int(1000000/8)), A)
    end = perf_counter_ns()

    print('Total encryption/decryption time for 1Mb was', (end-start)/1000000000, 's')
