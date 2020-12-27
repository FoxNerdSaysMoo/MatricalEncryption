#include <iostream>
#include <Eigen/Dense>
#include <math.h>
#include <time.h>

using namespace std;
using Eigen::MatrixXd;
using Eigen::MatrixXi;

/*
typedef Eigen::Matrix<uint8_t, Eigen::Dynamic, Eigen::Dynamic> Int8Matrix;
typedef Eigen::Matrix<uint16_t, Eigen::Dynamic, Eigen::Dynamic> Int16Matrix;
typedef Eigen::Matrix<uint32_t, Eigen::Dynamic, Eigen::Dynamic> Int32Matrix;
*/

MatrixXi rand_gen(int dim, int max) {
    MatrixXd r = MatrixXd::Random(dim, dim);
    return (r * max).cast<int>();
}

MatrixXi form_array(MatrixXi priv, MatrixXi shared, bool is_client, int max) {
    return ((is_client)? priv * shared : shared * priv)
    .unaryExpr([max](const int x) { return x % max; });
}

MatrixXi rm_det(MatrixXi matrix) {
    matrix.row(0).setZero();
    return matrix;
}

MatrixXi find_shared(MatrixXi priv, MatrixXi recv, bool is_client, int max) {
    return ((is_client)? priv * recv : recv * priv)
    .unaryExpr([max](const int x) { return x % max; });
}

MatrixXi add_det(MatrixXi matrix) {
    matrix.row(0).setOnes();
    return matrix;
}

MatrixXi encrypt_str(MatrixXi matrix, string str) {
    int length = matrix.size() * ceil(float(str.length()) / matrix.size());

    MatrixXi chars;
    chars.resize(1, length);
    chars = MatrixXi::Constant(1, length, 5);

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
        if (int(chars(0, x)) == 5) { break; }
        result += char(round(chars(0, x)));
    }

    return result;
}

int main() {
    MatrixXi a, b, G, Ga, Gb, bGa, aGb;
    a = rand_gen(5, 256);
    b = rand_gen(5, 256);
    G = rm_det(rand_gen(5, 256));

    cout << "A:\n" << a << endl;

    Ga = form_array(a, G, true, 255);
    Gb = form_array(b, G, false, 255);

    cout << "Ga:\n" << Ga << endl;

    bGa = add_det(find_shared(b, Ga, false, 255));
    aGb = add_det(find_shared(a, Gb, true, 255));

    cout << "aGb - bGa:\n" << aGb - bGa << endl;

    cout << decrypt_str(bGa, encrypt_str(bGa, "hello world")) << endl;
  
    string test_string = "";
    for (int x = 0; x < 1048576; x++) { test_string += "."; }
  
    clock_t t = clock();
    decrypt_str(bGa, encrypt_str(aGb, test_string));
    t = clock() - t;

    cout << "Encryption/decryption time for 10mb was " << float(t)/CLOCKS_PER_SEC << "s" << endl;

    return 0;
}
