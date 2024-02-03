from turtle import color
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
# Read the CSV file
data = pd.read_csv('out/effi_extended.csv')

# Extract the columns for plotting
columns_to_plot = ['optimal', 'backpack', 'backpack_relaxed']
M= 0.97
data['optimal'] -= data['true']*M
data['optimal_relaxed'] -= data['true']*M
data['backpack'] -= data['true']*M
data['backpack_relaxed'] -= data['true']*M
data['optimal_deviation'] = 100 * data['optimal'] / data['true']
data['optimal_rel_deviation'] = 100 * data['optimal_relaxed'] / data['true']
data['binpack_deviation'] = 100 * data['backpack'] / data['true']
data['binpack_rel_deviation'] = 100 * data['backpack_relaxed'] / data['true']

xlim = 20100
xmin = 400
# y_ticks = list(range(0, 111, 10))
y_ticks_percentage = list(range(0, 25, 5))
x_ticks = list(range(500, xlim+1, 1500))


axis_number_font_size = 15
subplot_font_size = 20
plot_font_size = 30


fig, (ax1, ax2) = plt.subplots(2, 1, layout='constrained')

w = 70

ax1.bar(data['true']-w ,data['backpack'], color='green', width=w, label="BinPack solution")
# ax1.bar(data['true']-w ,data['backpack_relaxed'], color='dodgerblue', width=w/2, label="BinPack relaxed")
ax1.bar(data['true']+w ,data['optimal_relaxed'], color='red', width=w, label="Optimal relaxed")
ax1.bar(data['true'] ,data['optimal'], color='orange', width=w, label="Optimal solution")

# ax1.set_xlim(400,20500)
# ax1.spines['left'].set_position(('data', 500))
# ax1.spines['left'].set_position('zero')
ax1.grid(True)
ax1.set_ylabel('Excess of base rods\nover optimal solution', fontsize=subplot_font_size)
ax1.set_xlabel('Number of base rods in optimal solution', fontsize=subplot_font_size)
ax1.set_xticks(x_ticks)
ax1.tick_params(axis='both', which='major', labelsize=axis_number_font_size)
ax1.tick_params(axis='both', which='minor', labelsize=axis_number_font_size)
# ax1.set_yticks(fontsize=axis_number_font_size)
ax1.set_xlim(xmin,xlim)
ax1.set_ylim(1,20000)
ax1.set_yscale('log')

lim = 5
data['smooth'] = data['binpack_deviation'][:lim]
data['smooth'] = data['binpack_deviation'].rolling(lim, closed="right").sum()/lim
data['smooth'][:lim] = data['binpack_deviation'][:lim]

optimal_opt_spline = make_interp_spline(data['true'], data['optimal_deviation'])
optimal_rel_spline = make_interp_spline(data['true'], data['optimal_rel_deviation'])
bin_bin_spline = make_interp_spline(data['true'], data['smooth'])
# bin_rel_spline = make_interp_spline(data['true'], data['binpack_rel_deviation'])
seriesBase = np.linspace(data['true'].min(), data['true'].max(), 500)
optSeries = optimal_opt_spline(seriesBase)
optRelSeries = optimal_rel_spline(seriesBase)
binSeries = bin_bin_spline(seriesBase)
# binRelSeries = bin_rel_spline(seriesBase)

ax2.plot(seriesBase, optSeries, color='orange', label="Optimal solution", linewidth=2)
ax2.plot(seriesBase, optRelSeries+0.05, color='red', label="Optimal relaxed", linewidth=2)
ax2.plot(seriesBase, binSeries, color='green', label="BinPack solution", linewidth=4)
# ax2.plot(seriesBase, binRelSeries, color='dodgerblue', label="BinPack relaxed", linewidth=2)

ax2.tick_params(axis='both', which='major', labelsize=axis_number_font_size)
ax2.tick_params(axis='both', which='minor', labelsize=axis_number_font_size)
ax2.grid(True)
ax2.set_ylabel('Percentage excess of base rods \nover optimal solution [%]', fontsize=subplot_font_size)
ax2.set_xlabel('Number of base rods in optimal solution', fontsize=subplot_font_size)
ax2.set_xticks(x_ticks)
ax2.set_xlim(xmin,xlim)


fig.suptitle('Algorithms efficiency - number of rods exceding optimal solution', fontsize=plot_font_size)

legend = plt.legend(loc='lower right', prop={'size': 22})

for legobjs in legend.legendHandles:
    legobjs.set_linewidth(4.0)

plt.show()
