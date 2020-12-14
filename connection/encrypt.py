import numpy as np


class ArrayEncryptor:
    def __init__(self, dims: tuple):
        self.dims = dims

    def generate_array(self, max: int, nptype='int32', division_factor: int = 1):
        return ((np.random.rand(*self.dims) * max) / division_factor).astype(nptype)

    def form_array(self, nparray, shared_array, is_client):
        return np.matmul(nparray, shared_array) if is_client else np.matmul(shared_array, nparray)

    def get_shared(self, nparray, recvarray, is_client):
        return np.matmul(nparray, recvarray) if is_client else np.matmul(recvarray, nparray)

    def encrypt_str(self, nparray, string):
        result = nparray.flatten()
        for index, char in enumerate(string):
            result[index] += ord(char)
        return np.reshape(result, nparray.shape)

    def decrypt_str(self, nparray, shared):
        result = ''
        for val in (nparray - shared).flatten():
            if val == 0:
                break
            result += chr(abs(val))
        return result


arr = ArrayEncryptor((400, 400))

gen = arr.generate_array(256)
gen2 = arr.generate_array(256, division_factor=100)
shared = arr.generate_array(256, division_factor=100)

a = arr.form_array(gen, shared, True)
b = arr.form_array(gen2, shared, False)

print(A := arr.get_shared(a, gen2, True))  # The namings are confusing
print(B := arr.get_shared(b, gen, False))
print(A == B)

print(arr.encrypt_str(A, 'Hello world!') - B)
print(arr.decrypt_str(arr.encrypt_str(A, 'Hello world!'), A))
