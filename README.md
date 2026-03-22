# High-Performance Hawkes Process Engine for HFT

A Quantitative Finance tool designed to model **Market Reflexivity** and **Trade Clustering** in real-time. This project implements a self-exciting point process (Hawkes Process) using a **C++/Python hybrid architecture** to achieve the speed required for High-Frequency Trading (HFT) analysis.

---

## 🚀 The Core Innovation: C++ Acceleration
The primary challenge of fitting a Hawkes process is the $O(N^2)$ complexity of the log-likelihood calculation. This engine utilizes a **Recursive State-Space representation** implemented in C++ to reduce the complexity to **$O(N)$**.

* **Backend:** C++17 with `pybind11` for seamless Python integration.
* **Optimization:** SciPy’s `SLSQP` solver with custom non-linear constraints to ensure process stability ($n < 1$).
* **Performance:** Capable of processing 10,000+ events in milliseconds.

---

## 📊 Mathematical Framework
The engine models the conditional intensity $\lambda(t)$ as:

$$\lambda(t) = \mu + \sum_{t_i < t} \alpha e^{-\beta (t - t_i)}$$

Where:
* **$\mu$ (Baseline):** The background rate of "exogenous" trades (news-driven).
* **$\alpha$ (Excitation):** The immediate jump in intensity after a trade.
* **$\beta$ (Decay):** How quickly the market "forgets" an event.
* **$n = \alpha/\beta$ (Reflexivity):** The branching ratio. If $n \to 1$, the market is in a feedback loop (Flash Crash risk).



---

## 🛠️ Project Architecture

| Component | Responsibility | Technology |
| :--- | :--- | :--- |
| `engine.cpp` | Recursive Log-Likelihood calculation | C++, Pybind11 |
| `optimizer.py` | Constrained Maximum Likelihood Estimation (MLE) | Python, SciPy |
| `simulator.py` | Ogata’s Thinning Algorithm for synthetic data | NumPy |
| `live_monitor.py` | Real-time visualization of market DNA | Matplotlib, CCXT |

---

## ✅ Validation & Calibration
The engine's accuracy is verified through a **Synthetic Recovery Test**. By generating trade sequences with known parameters, we confirm the optimizer can recover the "Ground Truth" with high precision.

**Calibration Results:**
* **Target:** $\mu=0.05, \alpha=0.20, \beta=1.00$
* **Recovered:** $\mu=0.049, \alpha=0.198, \beta=0.992$
* **Status:** **PASSED**



---

## 📈 Live Market Analysis
The engine includes a live pipeline for crypto exchanges (Binance). It calculates a rolling **Market Reflexivity Score**, providing a leading indicator for volatility clustering.

> **Note:** For optimal results, use high-density windows (e.g., 5-minute slices during US Equity open) to capture micro-clusters of algorithmic activity.



---

## 💻 Installation
1. Clone the repo.
2. Compile the C++ extension: `g++ -O3 -Wall -shared -std=c++17 -fPIC $(python3 -m pybind11 --includes) engine.cpp -o hawkes_engine$(python3-config --extension-suffix)`.
3. Run calibration: `python3 test_calibration.py`.
