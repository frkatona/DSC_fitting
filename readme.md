# DSC Sigmoid Fitting

This Python script is used for fitting a sigmoid function to DSC data. The dataset is expected to be in a CSV file, with columns for temperature (Temp) and alpha (Alpha).

![Sigmoid](Exports\sigmoidfit.png)

## Dependencies
The script uses the following Python libraries:

- pandas
- scipy
- numpy
- matplotlib

## How it works
The script first loads a CSV file located at CSVs\10_10Cmin_temp_alpha.csv. This file should contain the data to be fitted.

It defines a sigmoid function with parameters A, B, and T_m.

An initial guess for the parameters is provided as [1e-5, 1, 80].

The script then uses the curve_fit function from the scipy.optimize library to fit the sigmoid function to the data.

The fitted parameters and their standard deviations are extracted and printed.

Finally, the script plots the original data and the fitted curve using matplotlib.

## Usage
To use this script, simply run it in a Python environment with the necessary libraries installed. Make sure the CSV file is in the correct location and has the correct format.

Please note that you may need to adjust the file path and initial guess for the parameters depending on your specific dataset.

