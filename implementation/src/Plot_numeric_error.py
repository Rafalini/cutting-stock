from turtle import color, width
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

# Read the CSV file
data = pd.read_csv('output/effi_cut2.csv')

# Extract the columns for plotting
columns_to_plot = ['optimal', 'backpack', 'backpack_relaxed']

data['true'] /= 10
data['optimal'] /= 10
data['optimal_relaxed'] /= 10
data['backpack'] /= 10
data['backpack_relaxed'] /= 10

data['optimal'] -=  data['true']
data['optimal_relaxed'] -=  data['true']
data['backpack'] -= data['true']
data['backpack_relaxed'] -= data['true']

column_means = data.mean()
for index, row in data.iterrows():
    data.at[index, 'optimal'] += (row['optimal'] - column_means['optimal'])*10
    data.at[index, 'optimal_relaxed'] += (row['optimal_relaxed'] - column_means['optimal_relaxed'])*10
    data.at[index, 'backpack'] += (row['backpack'] - column_means['backpack'])*10
    data.at[index, 'backpack_relaxed'] += (row['backpack_relaxed'] - column_means['backpack_relaxed'])*10

# y_ticks = list(range(0, 111, 10))
# y_ticks_percentage = list(range(90, 101, 2))
x_ticks = list(range(0, 501, 50))


axis_number_font_size = 25
subplot_font_size = 25
plot_font_size = 35

fig, (ax1,ax2) = plt.subplots(2, 1, layout='constrained')
# w=40
# ax1.bar(data['true']-w ,data['backpack'], color='green', width=w, label="BinPack solution")
# # ax1.bar(data['true']-w ,data['backpack_relaxed'], color='dodgerblue', width=w/2, label="BinPack relaxed")
# ax1.bar(data['true']+w ,data['optimal_relaxed'], color='red', width=w, label="Optimal relaxed")
# ax1.bar(data['true'] ,data['optimal'], color='orange', width=w, label="Optimal solution")

backpack = make_interp_spline(data['true'], data['backpack'])
backpackrel = make_interp_spline(data['true'], data['backpack_relaxed'])
optimal_relaxed = make_interp_spline(data['true'], data['optimal_relaxed'])
optimal = make_interp_spline(data['true'], data['optimal'])
seriesBase = np.linspace(data['true'].min(), data['true'].max(), 50)

bacSer = backpack(seriesBase)
bacRel = backpackrel(seriesBase)
optRel = optimal_relaxed(seriesBase)
optSer = optimal(seriesBase)

ax1.plot(seriesBase ,bacRel, color='red', linewidth=3, label="BinPack relaxed")
ax1.plot(seriesBase ,bacSer, color='orange', linewidth=3, label="BinPack solution")
ax2.plot(seriesBase ,optRel, color='red', linewidth=3, label="Optimal relaxed")
ax2.plot(seriesBase ,optSer, color='orange', linewidth=3, label="Optimal solution")


# ax1.set_ylim(-2,2)
ax1.set_yticks([-1, 1, 5, 10, 15, 20, 25])
# ax1.spines['left'].set_position(('axes', 0.03))
# ax1.spines['right'].set_color('none')
ax1.grid(True)
ax1.set_ylabel('Difference of number\nof base rods', fontsize=subplot_font_size)
ax1.set_xlabel('Difference between solutionfound and optimal', fontsize=subplot_font_size)
ax1.set_xticks(x_ticks)
ax1.tick_params(axis='both', which='major', labelsize=axis_number_font_size)
ax1.tick_params(axis='both', which='minor', labelsize=axis_number_font_size)
# ax1.set_yticks(fontsize=axis_number_font_size)
ax1.set_xlim(0,500)


fig.suptitle('Excess of base rods with reduced lentghs by 5cm', fontsize=plot_font_size)
legend = ax1.legend(loc='upper right', prop={'size': 22})

for legobj in legend.legendHandles:
    legobj.set_linewidth(4.0)
plt.show()
