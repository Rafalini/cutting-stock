import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline


data = pd.read_csv('output/time_no_ext.csv')
#FONT SIZES
axis_number_font_size = 20
subplot_font_size = 25
plot_font_size = 35
x_ticks = list(range(1, 21, 1))

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
data['Unnamed: 0'] *= 0.4
data['true'] /= 1000

# data['optimal_relaxed'] += 0.5
data['optimal'] += 0.5

X_Y_Spline = make_interp_spline(data['true'], data['optimal'])
seriesBase = np.linspace(data['true'].min(), data['true'].max(), 500)
optimalSeries = X_Y_Spline(seriesBase)

# X_Y_Spline1 = make_interp_spline(data['true'], data['optimal_relaxed'])
# optimalRelSeries = X_Y_Spline1(seriesBase)

X_Y_Spline2 = make_interp_spline(data['true'], data['backpack'])
backpropSeries = X_Y_Spline2(seriesBase)

X_Y_Spline3 = make_interp_spline(data['true'], data['backpack_relaxed'])
backpropSeries = X_Y_Spline2(seriesBase)

ax.plot(seriesBase, backpropSeries-0.11, linewidth=3, color='tab:green', label="BinPack without relaxation")
ax.plot(seriesBase, backpropSeries, linewidth=3, color='tab:blue', label="BinPack with relaxation")
ax.plot(seriesBase, optimalSeries, linewidth=3, color='tab:orange', label="Optimal without relaxation")
# ax.plot(seriesBase, optimalRelSeries, linewidth=3, color='tab:red', label="Optimal with relaxation")
# ax.set_yscale('log')

ax.spines['left'].set_position(('data', 1))
ax.tick_params(axis='both', which='major', labelsize=axis_number_font_size)
ax.tick_params(axis='both', which='minor', labelsize=axis_number_font_size)
ax.set_xlim(1,20)
# ax.set_ylim(0,20)
ax.set_xticks(x_ticks)

plt.title('Time efficiency plot', fontsize=plot_font_size)
plt.xlabel('Problem size in thousands', fontsize=subplot_font_size)
plt.ylabel('Average time [s]', fontsize=subplot_font_size)

plt.grid(True)
legend = plt.legend(loc='upper left', prop={'size': 22})

for legobj in legend.legendHandles:
    legobj.set_linewidth(4.0)

plt.tight_layout()
plt.show()
