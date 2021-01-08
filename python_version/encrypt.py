import numpy as np
import math


def generate_array(dims: tuple, max: int, nptype='uint16') -> np.array:
    """
    Generate a random numpy array of shape dims, with a max of max, and type of nptype
    """
    return (np.random.rand(*dims) * max).astype(nptype)


def form_array(nparray: np.array, shared_array: np.array, is_client: bool) -> np.array:
    """
    Form public array from private array and shared array
    """
    return np.matmul(nparray, shared_array) if is_client else np.matmul(shared_array, nparray)


def get_shared(nparray: np.array, recvarray: np.array, is_client: bool) -> np.array:
    """
    Get a shared array from a recieved array and a private array
    """
    return np.matmul(nparray, recvarray) if is_client else np.matmul(recvarray, nparray)


def make_no_det(nparray: np.array) -> np.array:
    """
    Make a given numpy array have no determinant (prevents matrix inverse from being used)
    """
    arr = nparray
    arr[0] = np.zeros(arr[0].shape)
    return arr


def finish_array(shared):
    """
    Make a given numpy array have a determinant (necessary in decryption process)
    """
    arr = shared
    arr[0] = np.ones(arr[0].shape)
    return arr


def make_square(values, nptype='uint16') -> np.array:
    """
    Change a iterable into a square numpy array of type nptype
    """
    nextval = math.floor(math.sqrt(len(values))) + 1
    arr = np.ones((nextval * nextval))
    arr_ = arr.flatten()
    arr_[:len(values)] = values
    arr = arr_.reshape(arr.shape)
    return np.reshape(arr, (nextval, nextval)).astype(nptype)


def encrypt_str(nparray: np.array, string: str) -> np.array:
    """
    Encrypt a given string into a given numpy array
    """
    chunks = []
    result = np.zeros(nparray.shape).flatten()
    for chunk in [string[i:i+len(result)] for i in range(0, len(string), len(result))]:
        result = np.zeros(nparray.shape).flatten()
        for index, char in enumerate(chunk):
            result[index] += ord(char)
        chunks.append(np.reshape(result, nparray.shape))
    return np.matmul(nparray, np.concatenate(chunks, axis=1))


def decrypt_str(nparray: np.array, shared: np.array) -> str:
    """
    Decrypt a string from a given numpy array
    """
    result = ''
    arr = np.matmul(np.linalg.inv(shared), nparray)
    for val in arr.flatten():
        if val < 1:
            break
        result += chr(round(val))
    return result


if __name__ == '__main__':
    from timeit import default_timer

    dims = (7, 7)

    a = generate_array(dims, 255, 'uint8')
    b = generate_array(dims, 255, 'uint8')
    G = make_no_det(generate_array(dims, 65535, 'uint16'))

    Ga = form_array(a, G, True)
    Gb = form_array(b, G, False)

    A = finish_array(get_shared(a, Gb, True))
    B = finish_array(get_shared(b, Ga, False))

    print('Private key is', a.nbytes * 8, 'bits')
    print('Are the final arrays equal?', (A == B).flatten()[0])
    print(decrypt_str(encrypt_str(B, 'Hello world!'), A))

    start = default_timer()
    enc = encrypt_str(B, '.'*100*int(1000000/8))
    lap = default_timer()
    decrypt_str(enc, A)
    end = default_timer()

    enc_ = encrypt_str(B, '.'*(dims[0] * dims[1]))
    start_ = default_timer()
    decrypt_str(enc, A)
    end_ = default_timer()

    print(
        'Encryption time for 100Mb was', (lap-start),
        's\nDecryption time for 100Mb was', (end-lap),
        's\nTotal encryption/decryption time for 100Mb was', (end-start),
        's\nTotal theoretical time for a brute-force attack (from this machine) is',
        (end_ - start_) * (2 ** int(a.nbytes * 8)) / (2 * 3600 * 24 * 365 * 1000), 'millenia'
    )
