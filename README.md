# How the matrix encryption works
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FFoxNerdSaysMoo%2FPyEncryptors.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FFoxNerdSaysMoo%2FPyEncryptors?ref=badge_shield)

## Basics
The matrix encryption function by utilizing matrix division as a trapdoor function ('matrix division' refers to multiplying by inverse).

Using a determinant-free global variable (or just in standard encryption), the maximum amount of repetitions for a brute-force attack is 256^(n*n) where n is the matrix side length.

## Example scenario

Allow there to be 2 users: Alice and Bob. Let's assign Alice as the client. 

- Firstly, a dimension is agreed upon (Alice proposes, Bob agrees).
- Then both parties generate a private matrix in the dimensions previously agreed upon. 
- Alice (the client) generates a public array to be sent to Bob. 
- Both parties multiply their private array with the public array (Alice generates `private * public`, Bob vise versa).
- Now both parties send their multiplied array to the other party.
- Once the arrays have been recieved each party multiplies their private array with the recieved array (Alice generates `private * recieved`, Bob vise versa).
- Now both parties have a shared private array. Alice has `alice * (public * bob)`, and Bob has `(alice * public) * bob`, which due to the associative property of matrices are equal (both have `alice * public * bob`).

## Updates and improvements

- It is now possible to remove the determinant of the global matrix, thus making it much harder to find the private arrays. A extra function is used to ensure the shared arrays can have values encrypted in them.

- You can now convert a vector into a valid key, which allows you to make valid keys of any size (PYTHON ONLY)

## Example Usage

### Python 3

To begin, choose your key dimensions
```py
dims = (7, 7)  # Most efficient key size depending on your usage
```
Now you can generate the global key and the private keys
```py
a = generate_array(dims, 255, 'uint8')  # generate_array takes in 3 args:
b = generate_array(dims, 255, 'uint8')  # dimensions, maximum value, numpy datatype
G = make_no_det(generate_array(dims, 255, 'uint16'))
```
`make_no_det` is used to ensure that the global key has no inverse. It replaces the first row with a row of zeros.

Now you must generate the public arrays which will be sent
```py
Ga = form_array(a, G, True)  # Assuming `a` is the client
Gb = form_array(b, G, False)  # Assuming `b` is the server
```
Once the parties have recieved the public arrays, you must multiply the public array and the private array
```py
A = finish_array(get_shared(a, Gb, True))  # Assuming `a` is the client
B = finish_array(get_shared(b, Ga, False))  # Assuming `b` is the server
```
Check to make sure the arrays are equal
```py
print('Are the final arrays equal?', (A == B).flatten()[0])
```
And encrypt/decrypt some data
```py
from time import perf_counter_ns

start = perf_counter_ns()
decrypt_str(encrypt_str(B, '.'*int(1000000/8)), A)
end = perf_counter_ns()

print('Total encryption/decryption time for 1Mb was', (end-start)/1000000000, 's')
```

## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FFoxNerdSaysMoo%2FPyEncryptors.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2FFoxNerdSaysMoo%2FPyEncryptors?ref=badge_large)