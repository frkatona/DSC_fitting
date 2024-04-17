#%%
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

print('A_fit: ', A_fit, '+/-', std_errors[0])
print('B_fit: ', B_fit, '+/-', std_errors[1])
print('T_m_fit: ', T_m_fit, '+/-', std_errors[2])

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

#%%

## Chang plot

beta = 10 # K/min
n = 1 # order of reaction (maybe fit later)

# Filter data for a specific temperature range
temperature_lower_bound = 80
temperature_upper_bound = 110
filtered_data = data[(data['Temp'] >= temperature_lower_bound) & (data['Temp'] <= temperature_upper_bound)]

# Convert temperature to Kelvin for the plot
filtered_data['Temp_K'] = filtered_data['Temp'] + 273.15

# Calculate the derivative of alpha with respect to temperature
filtered_data['dAlpha_dT'] = np.gradient(filtered_data['Alpha'], filtered_data['Temp'])

# Apply the formula ln((beta*(da/dT))/((1-alpha)^n))
filtered_data['plot_y'] = np.log((beta * filtered_data['dAlpha_dT']) / ((1 - filtered_data['Alpha'])**n))

# Compute 1000/T (in Kelvin)
filtered_data['plot_x'] = 1000 / filtered_data['Temp_K']

# Create the plot
plt.figure(figsize=(10, 6))
plt.scatter(filtered_data['plot_x'], filtered_data['plot_y'], color='blue', label='Modified Arrhenius Plot')
plt.xlabel('1000/T (1/K)', fontsize=fontsize)
plt.ylabel('ln(beta * dAlpha/dT / (1-alpha)^n)', fontsize=fontsize)
plt.title('unmodified Chang plot', fontsize=fontsize)
plt.legend()
plt.grid(True)

# Fit to line and report the slope and intercept
slope, intercept = np.polyfit(filtered_data['plot_x'], filtered_data['plot_y'], 1)
print('Ea (slope): ', slope)
print('k0 (intercept): ', intercept)

# Plot the fitted line
plt.plot(filtered_data['plot_x'], slope * filtered_data['plot_x'] + intercept, color='red', label='fit: Ea=%5.3f, k0=%5.3e' % (slope, np.exp(intercept)))
plt.legend()


plt.xticks(fontsize=fontsize)
plt.yticks(fontsize=fontsize)

plt.show()
# %%
