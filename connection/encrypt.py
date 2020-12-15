import numpy as np


def encrypt_str(nparray, string):
    result = np.zeros(nparray.shape).flatten().astype(nparray.dtype)
    for index, char in enumerate(string):
        result[index] += ord(char)
    return np.matmul(nparray, np.reshape(result, nparray.shape))

def decrypt_str(nparray, shared):
    result = ''
    arr = np.matmul(np.linalg.inv(shared), nparray)
    for val in arr.flatten():
        if val == 0:
            break
        result += chr(round(val))
    return result

def generate_array(dims, max: int, nptype='int64'):
    return (np.random.rand(*dims) * max).astype(nptype)

def form_array(nparray, shared_array, is_client):
    return np.matmul(nparray, shared_array) if is_client else np.matmul(shared_array, nparray)

def get_shared(nparray, recvarray, is_client):
    return np.matmul(nparray, recvarray) if is_client else np.matmul(recvarray, nparray)

# Leave previous functions alone until the class is finished and functional
# Note to self: do not touch above functions


class Matrix(list):
    def __init__(self, max_rand=30):
        self._arr = generate_array(self, max_rand)  # One of the user's private arrays

    def encrypt_str(self, str):
        pass


if __name__ == '__main__':
    dims = (10, 10, 10, 10, 10, 10)

    a = generate_array(dims, 30)  # One of the user's private arrays
    b = generate_array(dims, 30)  # Another private array
    G = generate_array(dims, 30)  # Global/shared array

    Ga = form_array(a, G, True)  # Multiplies the public array and the private array based on the role. This is client
    Gb = form_array(b, G, False) # This one is server (The roles can be changed)

    A = get_shared(a, Gb, True)  # Multiplies the recieved array and the private array based on the role. This is client
    B = get_shared(b, Ga, False) # This is server

    print('Are the final arrays equal?', (A == B).flatten()[0])

    print(decrypt_str(encrypt_str(A, 'Hello world!'), B))
