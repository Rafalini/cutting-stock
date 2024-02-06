import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

axis_number_font_size = 15
subplot_font_size = 20
plot_font_size = 30

def adjustData(data):
    M=0.97
    data['optimal'] -= data['true']*M
    data['optimal_relaxed'] -= data['true']*M
    data['backpack'] -= data['true']*M
    data['backpack_relaxed'] -= data['true']*M
    data['optimal_deviation'] = 100 * data['optimal'] / data['true']
    data['optimal_rel_deviation'] = 100 * data['optimal_relaxed'] / data['true']
    data['binpack_deviation'] = 100 * data['backpack'] / data['true']
    data['binpack_rel_deviation'] = 100 * data['backpack_relaxed'] / data['true']
    return data

dataNo = pd.read_csv('out/effi_no_extended.csv')
dataEx = pd.read_csv('out/effi_extended.csv')
dataNo = adjustData(dataNo)
dataEx = adjustData(dataEx)

xlim = 20100
xmin = 370

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, layout='constrained', figsize=(14, 14))
fig.suptitle('Algorithms efficiency - number of rods exceding optimal solution', fontsize=plot_font_size)

ax1.tick_params(axis='both', which='major', labelsize=axis_number_font_size)
ax1.tick_params(axis='both', which='minor', labelsize=axis_number_font_size)
ax2.tick_params(axis='both', which='major', labelsize=axis_number_font_size)
ax2.tick_params(axis='both', which='minor', labelsize=axis_number_font_size)
ax3.tick_params(axis='both', which='major', labelsize=axis_number_font_size)
ax3.tick_params(axis='both', which='minor', labelsize=axis_number_font_size)
ax1.grid(True)
ax2.grid(True)
ax3.grid(True)
ax1.set_yscale('log')
ax2.set_yscale('log')
ax3.set_yscale('log')
ax1.set_xlim(xmin,xlim)
ax2.set_xlim(xmin,xlim)
ax3.set_xlim(xmin,xlim)
x_ticks = list(range(500, xlim+1, 1500))
ax1.set_xticks(x_ticks)
ax2.set_xticks(x_ticks)
ax3.set_xticks(x_ticks)


w = 70

ax1.set_title("Standard order, no relaxation", fontsize=subplot_font_size)
ax1.set_ylabel('Percentage excess of base rods \nover optimal solution [%]', fontsize=subplot_font_size)
ax1.set_xlabel('Number of base rods in optimal solution', fontsize=subplot_font_size)
ax1.bar(dataNo['true']+w  ,dataNo['optimal'], color='orange', width=w, label="Collumn gen solution")
ax1.bar(dataNo['true'] ,dataNo['optimal_relaxed'], color='red', width=w, label="Collumn gen relaxed")
ax1.bar(dataNo['true']-w ,dataNo['backpack'], color='green', width=w, label="BinPack solution")
# ax1.bar(dataNo['true']-w ,dataNo['backpack_relaxed'], color='blue', width=w, label="BinPack relaxed")

ax1.set_title("Extended order, with relaxation", fontsize=subplot_font_size)
ax2.set_ylabel('Percentage excess of base rods \nover optimal solution [%]', fontsize=subplot_font_size)
ax2.set_xlabel('Number of base rods in optimal solution', fontsize=subplot_font_size)
ax2.bar(dataNo['true']+w  ,dataEx['optimal'], color='orange', width=w, label="Collumn gen solution")
ax2.bar(dataNo['true']+w/2,dataEx['optimal_relaxed'], color='red', width=w, label="Collumn gen relaxed")
ax2.bar(dataNo['true']-w/2 ,dataEx['backpack'], color='green', width=w, label="BinPack solution")
ax2.bar(dataNo['true']-w ,dataEx['backpack_relaxed'], color='blue', width=w, label="BinPack relaxed")

ax1.legend(loc='lower left', prop={'size': 15})  # Separate legend for the bottom plot
ax2.legend(loc='lower left', prop={'size': 15})  # Separate legend for the bottom plot
plt.show()
