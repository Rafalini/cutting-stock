from turtle import color, width
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Read the CSV file
data = pd.read_csv('output/effi_summary3.csv')

# Extract the columns for plotting
columns_to_plot = ['optimal', 'backpack', 'backpack_relaxed']

data['optimal_deviation'] = 100 * data['optimal'] / data['true']
data.loc[data['optimal_deviation'] > 100 , 'optimal_deviation'] = 100
data['optimal'] -=  data['true']
data['backpack'] -= data['true']
data['backpack_relaxed'] -= data['true']


y_ticks = list(range(0, 111, 10))
y_ticks_percentage = list(range(90, 101, 2))
x_ticks = list(range(0, 1001, 50))


axis_number_font_size = 15
subplot_font_size = 20
plot_font_size = 40

fig, (ax1, ax2) = plt.subplots(2, 1, layout='constrained')

lim = 25
data['smooth_backpack'] = 0
data['smooth_backpack_relaxed'] = data['backpack_relaxed'].rolling(lim, closed="right").sum()/lim
data['smooth_optimal'] = data['optimal'].rolling(lim, closed="right").sum()/lim
data['smooth_optimal_deviation'] = data['optimal_deviation'].rolling(lim, closed="right").sum()/lim
data['smooth_backpack_relaxed'][:lim] = 0.5
data['smooth_optimal_deviation'][:lim] = 100
data['smooth_optimal'][:lim] = 0

ax1.plot(data['true'] ,data['smooth_backpack'], color='green', linewidth=3, label="True non-relaxed optimum")
ax1.plot(data['true'] ,data['smooth_backpack_relaxed'], color='blue', linewidth=3, label="BinPack relaxed solution")
ax1.plot(data['true'] ,data['smooth_optimal'], color='orange', linewidth=3, label="AMPL relaxed solution")

# ax1.set_ylim(0,20)
# ax1.spines['left'].set_position(('axes', 0.03))
ax1.spines['right'].set_color('none')
ax1.grid(True)
ax1.set_ylabel('Difference of number\nof base rods', fontsize=subplot_font_size)
ax1.set_xlabel('Difference between solutionfound and optimal', fontsize=subplot_font_size)
ax1.set_xticks(x_ticks)
ax1.tick_params(axis='both', which='major', labelsize=axis_number_font_size)
ax1.tick_params(axis='both', which='minor', labelsize=axis_number_font_size)
# ax1.set_yticks(fontsize=axis_number_font_size)
ax1.set_xlim(50,1000)


ax2.plot(data['true'], data['smooth_optimal_deviation'], color='orange', linewidth=4)

# ax2.spines['left'].set_position('zero')
ax2.spines['right'].set_color('none')
ax2.set_yticks(y_ticks_percentage)
ax2.set_xticks(x_ticks)
ax2.tick_params(axis='both', which='major', labelsize=axis_number_font_size)
ax2.tick_params(axis='both', which='minor', labelsize=axis_number_font_size)
ax2.grid(True)
ax2.set_ylabel('Relaxed result in\ncompareto non-relaxed, [%]', fontsize=subplot_font_size)
ax2.set_xlabel('Percentage difference betweensolution found and optimal', fontsize=subplot_font_size)
ax2.set_xlim(50,1000)


fig.suptitle('Relaxation effect', fontsize=plot_font_size)
legend = ax1.legend(loc='center right', prop={'size': 22})

for legobj in legend.legendHandles:
    legobj.set_linewidth(4.0)
plt.show()
