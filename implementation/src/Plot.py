import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
data = pd.read_csv('output/effi_summary.csv')
data = pd.read_csv('output/time_summary.csv')

# Extract the columns for plotting
columns_to_plot = ['backpack', 'backpack_relaxed']

data['backpack'] -= data['optimal']
data['backpack_relaxed'] -= data['optimal']


# Plotting the columns as a bar plot
plt.figure(figsize=(10, 6))  # Adjust figure size if needed
data[columns_to_plot].plot(kind='bar', width=0.8)

plt.xticks(data.index,data["optimal"].values)

plt.xticks(range(0, len(data), 25), data['optimal'][::25])

plt.title('Bar Plot of Columns')
plt.xlabel('Base steel rods in order')
plt.ylabel('Base steel rods difference to optimal')
plt.legend(loc='upper right')
plt.tight_layout()
plt.show()
