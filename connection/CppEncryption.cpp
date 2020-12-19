#include <iostream>

using namespace std;


void matmul(int mat1[],
              int mat2[],
              int res[],
              int rows,
              int cols) {
    int i, j, k;
    for (i = 0; i < rows; i++) {
        for (j = 0; j < cols; j++) {
            res[i * rows + j] = 0;
            for (k = 0; k < rows; k++) {
                res[i * rows + j] += mat1[i * 5 + k] * mat2[k * 5 + j];
            }
        }
    }
}

int main() {
    int i, j;
    int res[25]; // To store result
    int mat1[25] = { 1, 1, 1, 1, 1 ,
                     2, 2, 2, 2, 2 ,
                     3, 3, 3, 3, 3 ,
                     4, 4, 4, 4, 4 ,
                     5, 5, 5, 5, 5 };

 
    int mat2[25] = { 1, 1, 1, 1, 1 ,
                     2, 2, 2, 2, 2 ,
                     3, 3, 3, 3, 3 ,
                     4, 4, 4, 4, 4 ,
                     5, 5, 5, 5, 5 };

    matmul(mat1, mat2, res, 5, 5);

    cout << "Result matrix is \n";
    for (i = 0; i < 5; i++) {
        for (j = 0; j < 5; j++)
            cout << res[i * 5 + j] << " ";
        cout << "\n";
    }
 
    return 0;
}
