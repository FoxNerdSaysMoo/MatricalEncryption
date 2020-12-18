# How the matrix encryption works
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FFoxNerdSaysMoo%2FPyEncryptors.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FFoxNerdSaysMoo%2FPyEncryptors?ref=badge_shield)

## Basics
The matrix encryption function by utilizing matrix division as a trapdoor function ('matrix division' refers to multiplying by inverse).

Using a determinant-free global variable (or just in standard encryption), the maximum amount of repetitions for a brute-force attack is 256^(n*n) where n is the matrix size.

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

## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FFoxNerdSaysMoo%2FPyEncryptors.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2FFoxNerdSaysMoo%2FPyEncryptors?ref=badge_large)