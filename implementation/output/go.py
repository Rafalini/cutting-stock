import pandas as pd
import numpy as np

# Read CSV file into DataFrame
dataNo = pd.read_csv('effi_no_ext.csv')
dataEx = pd.read_csv('effi_extend.csv')
# Display the DataFrame
dataNo = dataNo.apply(np.ceil)
dataEx = dataEx.apply(np.ceil)

# Save DataFrame to another CSV file
dataEx.to_csv('effi_extend.csv', index=False)  # Replace 'output.csv' with the desired output file path
dataNo.to_csv('effi_no_ext.csv', index=False)  # Replace 'output.csv' with the desired output file path
