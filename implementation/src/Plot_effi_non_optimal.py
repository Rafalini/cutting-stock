from turtle import color
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Read the CSV file
data = pd.read_csv('output/effi_summary_dense.csv')

# Extract the columns for plotting
columns_to_plot = ['optimal', 'backpack', 'backpack_relaxed']

data['optimal'] -= data['true']
data['backpack'] -= data['true']
data['backpack_relaxed'] -= data['true']
data['binpack_deviation'] = 100 * data['backpack'] / data['true']

y_ticks = list(range(0, 111, 10))
y_ticks_percentage = np.arange(0.0, 0.25, 0.05)
y_ticks_percentage = list(range(0, 25, 5))
x_ticks = list(range(0, 1001, 50))


axis_number_font_size = 20
subplot_font_size = 25
plot_font_size = 35


fig, (ax1, ax2) = plt.subplots(2, 1, layout='constrained')

ax1.bar(data['true'] ,data['backpack'], color='green', width=1)

# ax1.set_ylim(0,20)
ax1.spines['left'].set_position('zero')
ax1.spines['right'].set_color('none')
ax1.grid(True)
ax1.set_ylabel('Excess of base rods\nover optimal solution', fontsize=subplot_font_size)
ax1.set_xlabel('Number of base rods in optimal solution', fontsize=subplot_font_size)
ax1.set_xticks(x_ticks)
ax1.tick_params(axis='both', which='major', labelsize=axis_number_font_size)
ax1.tick_params(axis='both', which='minor', labelsize=axis_number_font_size)
# ax1.set_yticks(fontsize=axis_number_font_size)
ax1.set_xlim(0,1000)

lim = 10
data['smooth'] = data['binpack_deviation'][:lim]
data['smooth'] = data['binpack_deviation'].rolling(lim, closed="right").sum()/lim
data['smooth'][:lim] = data['binpack_deviation'][:lim]

ax2.plot(data['true'], data['smooth'], color='orange')
# ax2.plot(data['true'], data['binpack_deviation'], color='red')

ax2.spines['left'].set_position('zero')
ax2.spines['right'].set_color('none')
ax2.set_yticks(y_ticks_percentage)
ax2.set_xticks(x_ticks)
ax2.tick_params(axis='both', which='major', labelsize=axis_number_font_size)
ax2.tick_params(axis='both', which='minor', labelsize=axis_number_font_size)
ax2.grid(True)
ax2.set_ylabel('Percentage excess of base rods \nover optimal solution [%]', fontsize=subplot_font_size)
ax2.set_xlabel('Number of base rods in optimal solution', fontsize=subplot_font_size)
ax2.set_xlim(0,1000)

fig.suptitle('Algorithm efficiency - number of rods exceding true optimal solution', fontsize=plot_font_size)
plt.show()
