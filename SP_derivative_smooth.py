# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 13:01:34 2024

@author: sarah
"""

#%%
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
import numpy as np

# Read the CSV file
df = pd.read_csv(r'CSVs/10_10Cmin_temp_alpha.csv')

# Smooth the 'Alpha' values using a moving average with window size 3
smoothed_alpha = df['Alpha'].rolling(window=3).mean()


# Update the 'Alpha' column with the smoothed values
df['Smoothed_Alpha'] = smoothed_alpha

# Plot the data
plt.plot(df['Temp'], df['Alpha'], color='red', label='Original Alpha')

# Plot Smoothed Alpha vs Temp
plt.plot(df['Temp'], df['Smoothed_Alpha'], color='blue', label='Smoothed Alpha')

plt.xlabel('Temp')
plt.ylabel('Alpha')
plt.title('Alpha vs Temp')
plt.legend()
plt.grid(True)
plt.show()
#%%

import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

# Drop rows with NaN values
df_cleaned = df.dropna()

# Sort the cleaned DataFrame by the 'Temp' column to ensure the fit is correct
df_sorted = df_cleaned.sort_values(by='Temp')

# Get the 'Temp' and 'Smoothed_Alpha' columns as numpy arrays
X = df_sorted['Temp'].values.reshape(-1, 1)
y = df_sorted['Smoothed_Alpha'].values

# Define the Gaussian Process regressor with a radial basis function (RBF) kernel
kernel = C(1.0, (1e-3, 1e3)) * RBF(length_scale=10.0, length_scale_bounds=(1e-2, 1e2))
gpr = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10)

# Fit the Gaussian Process model to the data
gpr.fit(X, y)

# Make predictions for every 0.5°C interval from 80°C to 140°C
temp_range = np.arange(80 , 170, 0.5).reshape(-1, 1)
alpha_pred, _ = gpr.predict(temp_range, return_std=True)

# Create a DataFrame to store the results
result_df = pd.DataFrame({'Temp': temp_range.flatten(), 'Smoothed_Alpha': alpha_pred})

# Save the DataFrame to a CSV file
result_df.to_csv(r'CSVs/10_10_spline_export_1.csv', index=False)

print("CSV file saved successfully.")

# Plot the data and the mean prediction of the Gaussian Process
plt.figure(figsize=(8, 6))
plt.scatter(X, y, label='Original Data', color='blue')
plt.plot(temp_range, alpha_pred, label='GPR Mean Prediction', color='red')
plt.xlabel('Temp')
plt.ylabel('Smoothed Alpha')
plt.title('Gaussian Process Regression')
plt.legend()
plt.grid(True)
plt.show()

#%%

df = pd.read_csv(r'CSVs/10_10_spline_export_1.csv')

derivative = df['Smoothed_Alpha'].diff() / df['Temp'].diff()

# Add the derivative values to the DataFrame
df['Derivative'] = derivative

df = df.iloc[4:]

df = df.dropna()

# Plot temperature vs. derivative
plt.figure(figsize=(8, 6))
plt.plot(df['Temp'], df['Derivative'], color='red')
plt.xlabel('Temperature')
plt.ylabel('Derivative of Smoothed Alpha')
plt.title('Temperature vs. Derivative of Smoothed Alpha')
plt.grid(True)
plt.show()
# Save the DataFrame with temp, smoothed alpha, and derivative as CSV
df[['Temp', 'Smoothed_Alpha', 'Derivative']].to_csv(r'CSVs/10_10_spline_export_2.csv', index=False)

print("CSV file with smoothed alpha and derivative saved successfully.")

