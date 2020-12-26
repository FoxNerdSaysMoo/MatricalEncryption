#include <iostream>
#include <Eigen/Dense>

using namespace std;
using Eigen::MatrixXd;

MatrixXd rand_gen(int dim, int max) {
    MatrixXd r = MatrixXd::Random(dim, dim);
    return r * max;
}


int main() {
    MatrixXd a, b, G;
    a = rand_gen(5, 255);
    b = rand_gen(5, 255);
    G = rand_gen(5, 255);
    cout << a;
}

