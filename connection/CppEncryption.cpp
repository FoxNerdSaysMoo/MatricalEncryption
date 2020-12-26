#include <iostream>
#include <stdlib.h>
#include <random>
#include <cmath>

using namespace std;


template<class T>
void matmul(T mat1[],
              float mat2[],
              float res[],
              int rows,
              int cols) {
    int i, j, k;

    for (i = 0;i < rows;i++) {
        for (j = 0;j < cols;j++) {
            res[i * rows + j] = 0;

            for (k = 0;k < rows;k++) {
                res[i * rows + j] += mat1[i * 5 + k] * mat2[k * 5 + j];
            }
        }
    }
}

template<class T>
long determinant( T matrix[], int n) {
    long det = 0;
    long submatrix[n*n];

    if (n <= 2) {
        return (matrix[0] * matrix[3]) - (matrix[1] * matrix[2]);
    }

    else {
        for (int x = 0; x < n; x++) {
            int subi = 0;
            for (int i = 1; i < n; i++) {
                int subj = 0;
                for (int j = 0; j < n; j++) {
                    if (j == x) {
                        submatrix[subi * n + subj] = matrix[i * n + j];
                        continue;
                    }
                    submatrix[subi * n + subj] = matrix[i * n + j];
                    subj++;
                }
                subi++;
            }
            det = det + (pow(-1, x) * matrix[x] * determinant(submatrix, n - 1));
        }
    }
    return det;
}

template<class T>
void getCofactor(T A[], int temp[], int p, int q, int n) {
    int i = 0, j = 0;

    for (int row = 0; row < n; row++) {
        for (int col = 0; col < n; col++) {
            if (row != p && col != q) {
                temp[i * n + j++] = A[row * n + col];

                if (j == n - 1) {
                    j = 0;
                    i++;
                }
            }
        }
    }
}

template<class T>
void adjoint(T A[], int adj[], int n) {
    if (n == 1) {
        adj[0] = 1;
        return;
    }

    int sign = 1, temp[n*n];

    for (int i=0; i<n; i++) {
        for (int j=0; j<n; j++) {
            getCofactor(A, temp, i, j, n);

            sign = pow(-1, i+j);

            adj[i * n + j] = sign * determinant(temp, n-1);
        }
    }
}

template<class T>
bool inverse(T A[], float inverse[], int n) {
    long det = determinant(A, n);
    cout << "Determinant: " << det << endl;

    if (det == 0) {
        cout << "Singular matrix, can't find its inverse\n";
        return false;
    }

    int adj[n*n];
    adjoint(A, adj, n);

    for (int i=0;i<n;i++) {
        for (int j=0;j<n;j++) {
            inverse[i * n + j] = adj[i * n + j]/float(det);
        }
    }
    return true;
}

// Randomly generate a array
template<class T>
void randgen(T res[], int n, int max) {
    random_device dev;
    mt19937 rng(dev());
    uniform_int_distribution<mt19937::result_type> dist(0, max);

    for (int i=0; i < n; i++) {
        for (int j=0; j < n; j++) {
            res[i * n + j] = dist(rng);
        }
    }
}

// Function to display the matrix.
template<class T>
void display(T A[], int n) {
    for (int i=0;i<n;i++) { 
        for (int j=0;j<n;j++) {
            cout << A[i * n + j] << " ";
        }
        cout << endl;
    }
    cout << "------------" << endl;
}


int main() {
    int i, j, n;
    float res[25];// To store result
    float mat1[25];
    float mat2[25];
    float res2[25];

    randgen(mat1, 5, 5);
    randgen(mat2, 5, 5);

    display(mat1, 5);

    inverse(mat1, res, 5);

    cout << "Inverse matrix is \n";
    display(res, 5);

    matmul(mat1, res, res2, 5, 5);
    cout << "Identity matrix\n";
    display(res2, 5);
 
    return 0;
}
