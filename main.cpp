/* (c) 2019 ukrkyi */
#include <iostream>
#include <Eigen/Core>
#include <Eigen/Dense>
#include <fstream>
#include <vector>
#include <iomanip>

#define NO_MENTIONS_THRESHOLD 0.0005

using Eigen::Matrix;

typedef std::pair<int, std::pair<double, double> > info_t;

Matrix<double, Eigen::Dynamic, 1> pagerank_iterative(Matrix<double, Eigen::Dynamic, Eigen::Dynamic> & matrix, int n, double d, double eps)
{
	Matrix<double, Eigen::Dynamic, 1> r = Matrix<double, Eigen::Dynamic, 1>::Constant(n, 1.0/n), r_old = r;
	Matrix<double, Eigen::Dynamic, 1> one = Matrix<double, Eigen::Dynamic, 1>::Constant(n, 1);
	do r = d * matrix * (r_old = r)  + ((1 - d) / n) * one;
	while ((r - r_old).norm() >= eps);
	return r;
}

Matrix<double, Eigen::Dynamic, 1> pagerank_algebraic(Matrix<double, Eigen::Dynamic, Eigen::Dynamic> & matrix, int n, double d)
{
	Matrix<double, Eigen::Dynamic, Eigen::Dynamic> I = Matrix<double, Eigen::Dynamic, Eigen::Dynamic>::Identity(n, n);
	Matrix<double, Eigen::Dynamic, 1> one = Matrix<double, Eigen::Dynamic, 1>::Constant(n, 1);
	return (I - d * matrix).colPivHouseholderQr().solve(((1-d) / n) * one);
}

int main()
{
	std::ifstream f("matrix.txt");
	int n;
	f >> n;
	std::vector<double> data(n*n);
	double x; double sum = 0;
	int i = 0;
	// transform matrix into pagerank form
	while (f >> x) {
		data[i++] = x;
		sum += x;
		if (!(i % n)) {
			for (int j = i-1; j >= i - n; j--)
				data[j] = ((sum == 0) ? 1.0/n : data[j] / sum);
			sum = 0;
		}
	}
	f.close();
	Matrix<double, Eigen::Dynamic, Eigen::Dynamic> mx(n, n);
	for (i = 0; i < n*n; i++)
		mx(i % n, i / n) = data[i];
	//std::cout << mx << std::endl;
	// free memory
	data.resize(0);
	Matrix<double, Eigen::Dynamic, 1> result_it = pagerank_iterative(mx, n, 0.7, 0.000001),
			result_alg = Matrix<double, Eigen::Dynamic, 1>::Zero(n);//pagerank_algebraic(mx, 0.85);
	std::ifstream heroes("names.txt");
	std::vector<std::string> names(n);
	for (i = 0; i < n; i++)
		getline(heroes, names[i]);
	heroes.close();
	std::vector<info_t> result(n);
	for (i = 0; i < n; i++)
		result[i] = info_t(i, std::pair<double,double>(result_it(i), result_alg(i)));
	std::sort(result.begin(), result.end(), [](info_t & a, info_t & b){return a.second.first > b.second.first;});
	i = 0;
	freopen("out-10-0.7.txt","w",stdout);
	while (result[i].second.second > NO_MENTIONS_THRESHOLD || result[i].second.first > NO_MENTIONS_THRESHOLD) {
		std::cout << std::setw(20) << names[result[i].first] << ' ' << std::setw(15) <<
			     result[i].second.first << ' ' << std::setw(15) << result[i].second.second << std::endl;
		i++;
	}
	return 0;
}
