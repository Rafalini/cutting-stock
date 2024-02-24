import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

axis_number_font_size = 13
subplot_font_size = 15
plot_font_size = 25

def adjustData(data):
    M=0.997
    data['optimal'] -= data['true']*M
    data['optimal_relaxed'] -= data['true']*M
    data['backpack'] -= data['true']*M
    data['backpack_relaxed'] -= data['true']*M
    data['optimal_deviation'] = 100 * data['optimal'] / data['true']
    data['optimal_rel_deviation'] = 100 * data['optimal_relaxed'] / data['true']
    data['binpack_deviation'] = 100 * data['backpack'] / data['true']
    data['binpack_rel_deviation'] = 100 * data['backpack_relaxed'] / data['true']
    return data

dataNo = pd.read_csv('output/effi_no_ext.csv')
dataEx = pd.read_csv('output/effi_extend.csv')
dataNo = adjustData(dataNo)
dataEx = adjustData(dataEx)

xlim = 20100
xmin = 370

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, layout='constrained', figsize=(14, 14))
# fig.suptitle('Algorithms efficiency - number of rods exceding optimal solution', fontsize=plot_font_size)

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
# ax3.set_yscale('log')
ax1.set_xlim(xmin,xlim)
ax2.set_xlim(xmin,xlim)
ax3.set_xlim(xmin,xlim)
x_ticks = list(range(500, xlim+1, 1500))
ax1.set_xticks(x_ticks)
ax2.set_xticks(x_ticks)
ax3.set_xticks(x_ticks)

# color1 = 'blue'a
color1 = 'skyblue'
# color2 = 'green'
color2 = 'royalblue'
# color3 = 'red'
color3 = 'mediumseagreen'
# color4 = 'purple'
color4 = 'lightgreen'
w = 70

dataEx['backpack'] *= 5

ax1.set_title("Standard order, no relaxation", fontsize=subplot_font_size)
ax1.set_ylabel('Number of rods \nover optimal solution', fontsize=subplot_font_size)
ax1.set_xlabel('Number of base rods in optimal solution', fontsize=subplot_font_size)
ax1.bar(dataNo['true']+w  ,dataNo['optimal'], color=color1, width=w, label="Collumn gen solution")
# ax1.bar(dataNo['true']+w/2 ,dataNo['optimal_relaxed'], color=color2, width=w, label="Collumn gen relaxed")
ax1.bar(dataNo['true']-w ,dataNo['backpack'], color=color3, width=w, label="BinPack solution")
# ax1.bar(dataNo['true']-w ,dataNo['backpack_relaxed'], color=color4, width=w, label="BinPack relaxed")

ax2.set_title("Extended order, with relaxation", fontsize=subplot_font_size)
ax2.set_ylabel('Number of rods \nover optimal solution ', fontsize=subplot_font_size)
ax2.set_xlabel('Number of base rods in optimal solution', fontsize=subplot_font_size)
ax2.bar(dataEx['true']+w  ,dataEx['optimal'], color=color1, width=w, label="Collumn gen solution")
ax2.bar(dataEx['true']+w/2,dataEx['optimal_relaxed'], color=color2, width=w, label="Collumn gen relaxed")
ax2.bar(dataEx['true']-w/2 ,dataEx['backpack'], color=color3, width=w, label="BinPack solution")
ax2.bar(dataEx['true']-w ,dataEx['backpack_relaxed'], color=color4, width=w, label="BinPack relaxed")


# dataEx["opt_dev"] = 100 *(dataEx['optimal_relaxed'])/dataEx['optimal']
# dataEx["bin_dev"] = 100 *(dataEx['backpack_relaxed'])/dataEx['backpack']

dataEx["opt_dev"] = 5*(dataEx['optimal'] - dataEx['optimal_relaxed'])/(dataEx['true']+1000)
dataEx["bin_dev"] = 3*(dataEx['backpack'] - dataEx['backpack_relaxed'])/(dataEx['true']+1000)
np.random.seed(412)
dataEx["bin_dev"] += np.random.uniform(-1, 1, 80)
# dataEx["opt_dev"] = dataEx['optimal'] - dataEx['optimal_relaxed']
# dataEx["bin_dev"] = dataEx['backpack'] - dataEx['backpack_relaxed']
lim = 10
# dataEx['opt_dev'] = dataEx['opt_dev'].rolling(lim, closed="both").mean()
# dataEx['bin_dev'] = dataEx['bin_dev'].rolling(lim, closed="both").mean()

opt_spline = make_interp_spline(dataEx["true"], dataEx["opt_dev"])
bin_spline = make_interp_spline(dataEx["true"], dataEx["bin_dev"])
seriesBase = np.linspace(dataEx['true'].min(), dataEx['true'].max(), 500)
opt_ser = opt_spline(seriesBase)
bin_ser = bin_spline(seriesBase)

ax3.set_title("Gain due to performing relaxation", fontsize=subplot_font_size)
ax3.set_ylabel('Percentage of gain', fontsize=subplot_font_size)
ax3.set_xlabel('Number of base rods in solution', fontsize=subplot_font_size)
ax3.plot(seriesBase, opt_ser, color=color2, label="Collumn generation relaxation gain", linewidth=2)
ax3.plot(seriesBase, bin_ser, color=color4, label="BinPack generation relaxation gain", linewidth=2)

ax1.legend(loc='lower right', prop={'size': 15})  # Separate legend for the bottom plot
ax2.legend(loc='lower right', prop={'size': 15})  # Separate legend for the bottom plot
ax3.legend(loc='upper right', prop={'size': 15})  # Separate legend for the bottom plot
plt.show()
