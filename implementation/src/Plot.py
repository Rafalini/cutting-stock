import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
data = pd.read_csv('output/effi_summary2.csv')
# data = pd.read_csv('output/time_summary2.csv')

# Extract the columns for plotting
columns_to_plot = ['optimal', 'backpack', 'backpack_relaxed']

data['optimal'] -= data['optimal']
data['backpack'] -= data['true']
data['backpack_relaxed'] -= data['true']
data['binpack_deviation'] = data['backpack'] / data['true']

y_ticks = list(range(0, 111, 10))
x_ticks = list(range(0, 1000, 25))

# Plotting the columns as a bar plot
# plt.figure(figsize=(10, 6))  # Adjust figure size if needed

data[columns_to_plot].plot(kind='bar', width=1, label=columns_to_plot)

# plt.xticks(data.index,data["optimal"].values)
# plt.xticks(range(0, len(data), 25), data['optimal'][::25])

plt.title('Bar Plot of Columns', fontsize=30)
plt.xlabel('Base steel rods in order')
plt.ylabel('Base steel rods difference to optimal')
plt.yticks(y_ticks)
plt.xticks(x_ticks)
plt.grid(True)
plt.legend(loc='upper right')
plt.tight_layout()
plt.legend()
plt.show()
