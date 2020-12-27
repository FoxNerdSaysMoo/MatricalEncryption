#include <iostream>
#include <Eigen/Dense>
#include <math.h>

using namespace std;
using Eigen::MatrixXd;
using Eigen::MatrixXi;

MatrixXi rand_gen(int dim, int max) {
    MatrixXd r = MatrixXd::Random(dim, dim);
    return (r * max).cast<int>();
}

MatrixXi form_array(MatrixXi priv, MatrixXi shared, bool is_client) {
    return (is_client)? priv * shared : shared * priv;
}

MatrixXi rm_det(MatrixXi matrix) {
    matrix.row(0).setZero();
    return matrix;
}

MatrixXi find_shared(MatrixXi priv, MatrixXi recv, bool is_client) {
    return (is_client)? priv * recv : recv * priv;
}

MatrixXi add_det(MatrixXi matrix) {
    matrix.row(0).setOnes();
    return matrix;
}

MatrixXi encrypt_str(MatrixXi matrix, string str) {
    int length = matrix.size() * ceil(float(str.length()) / matrix.size());

    MatrixXi chars;
    chars.resize(1, length);
    chars.setZero();

    for (int x = 0; x < str.length(); x++) {
        chars(0, x) = int(str.at(x));
    }

    chars.resize(matrix.rows(), chars.size()/matrix.rows());
    return matrix * chars;
}

string decrypt_str(MatrixXi shared, MatrixXi recv) {
    MatrixXd chars = shared.cast<double>().inverse() * recv.cast<double>();
    chars.resize(1, chars.size());

    string result = "";

    for (int x = 0; x < chars.size(); x++) {
        if (int(chars(0, x)) == 0) { break; }
        result += char(round(chars(0, x)));
    }

    return result;
}

int main() {
    MatrixXi a, b, G, Ga, Gb, bGa, aGb;
    a = rand_gen(5, 255);
    b = rand_gen(5, 255);
    G = rm_det(rand_gen(5, 255));

    cout << "A:\n" << a << endl;

    Ga = form_array(a, G, true);
    Gb = form_array(b, G, false);

    cout << "Ga:\n" << Ga << endl;

    bGa = add_det(find_shared(b, Ga, false));
    aGb = add_det(find_shared(a, Gb, true));

    cout << "aGb - bGa:\n" << aGb - bGa << endl;

    cout << decrypt_str(a, encrypt_str(a, "hello world"));
}
