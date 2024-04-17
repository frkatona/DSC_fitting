import pandas as pd
from scipy.optimize import curve_fit
import numpy as np

import matplotlib.pyplot as plt

# Load the CSV data
file_path = r'CSVs\10_10Cmin_temp_alpha.csv'
data = pd.read_csv(file_path)


# Define the sigmoid function
def sigmoid(T, A, B, T_m):
    return A / (1 + np.exp(-B * (T - T_m)))

# Initial guess for the parameters [A, B, T_m]
initial_guess = [1e-5, 1, 80]  # Example: A = 1e-5, B = 1, T_m = midpoint guess around 80

# Fit the curve
popt, pcov = curve_fit(sigmoid, data['Temp'], data['Alpha'], p0=initial_guess)

# Extracting the fitted parameters and the standard deviations of the parameters
A_fit, B_fit, T_m_fit = popt
std_errors = np.sqrt(np.diag(pcov))  # Standard deviations of the fitted parameters

print(A_fit, B_fit, T_m_fit, std_errors)

# Plot the data and the fitted curve
fontsize = 25
plt.plot(data['Temp'], data['Alpha'], 'o', label='DSC data', markersize=5)
plt.plot(data['Temp'], sigmoid(data['Temp'], A_fit, B_fit, T_m_fit), label='fit: A=%5.3e, B=%5.3f, T_m=%5.3f' % tuple(popt), linewidth=3)
plt.xlabel('Temperature (°C)', fontsize=fontsize)
plt.ylabel('Alpha', fontsize=fontsize)

# Plot the standard deviation of the parameters
plt.fill_between(data['Temp'], sigmoid(data['Temp'], A_fit - std_errors[0], B_fit - std_errors[1], T_m_fit - std_errors[2]),
                 sigmoid(data['Temp'], A_fit + std_errors[0], B_fit + std_errors[1], T_m_fit + std_errors[2]), color='gray', alpha=0.5)

plt.legend()

plt.xticks(fontsize=fontsize)
plt.yticks(fontsize=fontsize)


plt.show()
