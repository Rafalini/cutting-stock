import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('output/time_summary_2.csv')
#FONT SIZES
axis_number_font_size = 15
subplot_font_size = 20
plot_font_size = 30
x_ticks = list(range(0, 1001, 50))

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
data['Unnamed: 0'] *= 10
ax.plot(data['Unnamed: 0'], data['optimal'], linewidth=2, color='tab:orange', label="Optimal solution")
ax.plot(data['Unnamed: 0'], data['backpack'], linewidth=2, color='tab:blue', label="BinPack solution")
ax.set_yscale('log')

ax.spines['left'].set_position('zero')
ax.tick_params(axis='both', which='major', labelsize=axis_number_font_size)
ax.tick_params(axis='both', which='minor', labelsize=axis_number_font_size)
# ax.set_xlim(0,1000)
# ax.set_ylim(0,100)
# ax.set_xticks(x_ticks)

plt.title('Time efficiency plot', fontsize=plot_font_size)
plt.xlabel('Problem size', fontsize=subplot_font_size)
plt.ylabel('Average time [s]', fontsize=subplot_font_size)

plt.grid(True)
legend = plt.legend(loc='lower right', prop={'size': 22})

for legobj in legend.legendHandles:
    legobj.set_linewidth(4.0)

plt.tight_layout()
plt.show()
