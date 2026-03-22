#include <vector>
#include <cmath>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

using namespace std;
namespace py = pybind11;

vector<double> compute_r_vector(const vector<double>& timestamps, double beta)
{
    int N = timestamps.size();
    vector<double> res(N, 0.0);
    
    for(int i = 1; i < N; i++)
    {
        double dt = timestamps[i] - timestamps[i-1];	
        res[i] = exp(-beta * dt) * (1.0 + res[i-1]);
    }
    return res;
}

double log_likelihood(double T, double mu, double alpha, double beta, const vector<double>& R, const vector<double>& t)
{
    double res = 0;
    int N = t.size();
    
    // Part 1: Intensity sum
    for(int i = 0; i < N; i++)
    {
        // Added a tiny 1e-10 to prevent log(0) which returns -infinity
        res += log(mu + alpha * R[i] + 1e-10);
    }
    
    // Part 2: Baseline intensity over total time
    res -= mu * T;
    
    // Part 3: The Kernel Integral (Compensator)
    double kernel_integral = 0;
    for(int i = 0; i < N; i++)
    {
        kernel_integral += (1.0 - exp(-beta * (T - t[i])));
    }
    res -= (alpha / beta) * kernel_integral;
    
    return -res; // Return Negative Log Likelihood
}

PYBIND11_MODULE(hawkes_engine, m) {
    m.doc() = "High-performance Hawkes Process engine for HFT"; 
    m.def("compute_r_vector", &compute_r_vector, "Compute recursive R vector");
    m.def("log_likelihood", &log_likelihood, "Compute Negative Log-Likelihood");
}
