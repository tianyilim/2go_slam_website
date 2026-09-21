import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# Set Arial font family globally
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

# Methods
methods = [
    'VINS-\nFusion',
    'VINS-Fusion\n+ PGO',
    'ORB-\nSLAM3',
    'Maplab-\nBIN',
    'Maplab-\nSP',
    '2GO\n(Ours)'
]
target_method_name = '2GO\n(Ours)'
target_index = methods.index(target_method_name)

# Total Runtimes (sec)
# Maplab-BIN: 110 + 29 = 139s
# Maplab-SP: 14,139 + 271 = 14,410s
runtimes = [1564, 6206, 1755, 139, 14410, 1167]

# RMSE ATE values (m) for colormap
ate_values = [21.14, 13.22, 5.62, 20.83, 20.35, 3.73]

# Colormap setup: RdYlGn_r with min=0, max=max(ate_values)
norm = mcolors.Normalize(vmin=0, vmax=max(ate_values))
cmap = plt.get_cmap('RdYlGn_r')
bar_colors = [cmap(norm(val)) for val in ate_values]

x = np.arange(len(methods))
width = 0.55

fig, ax = plt.subplots(figsize=(10, 4), dpi=300)

# Single bar chart colored by RMSE ATE
bars = ax.bar(x, runtimes, width, color=bar_colors, edgecolor='none')

# Log scale for y-axis
ax.set_yscale('log')

# Add black horizontal line at 1414s
hline_val = 1414
ax.axhline(y=hline_val, color='black', linestyle='--', linewidth=1.0,
           label='Real-Time Trajectory Duration (1,414s)')

# # Label for the horizontal line centered along the line
# ax.text(2.5, hline_val * 1.18, 'Real-Time Trajectory Duration (1414s)',
#         color='black', fontsize=10, fontweight='bold', ha='center', va='bottom',
#         bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.8))

# Title and axis styling
ax.set_title(
    'Runtime Comparison Across Methods on VBR $\it{spagna\_train0}$', fontsize=15, fontweight='bold', pad=20)
ax.set_ylabel('Runtime (sec, log scale)', fontsize=12, fontweight='bold')
ax.set_xticks(x)
# Set normal weight for all initially
ax.set_xticklabels(methods, fontsize=11, fontweight='normal')
tick_labels = ax.get_xticklabels()
tick_labels[target_index].set_fontweight('bold')  # Specific override

# Values above bars (scaled relative to log height)
for i, rect in enumerate(bars):
    height = rect.get_height()

    # Determine the font weight based on whether it's the target bar
    weight = 'bold' if i == target_index else 'normal'

    # Add the text label
    ax.text(rect.get_x() + rect.get_width() / 2, height * 1.2,
            f"{int(height):,}s\nATE: {ate_values[i]:.2f}m",  # Format as integer with comma separator
            ha='center', va='bottom',
            fontsize=10, fontweight=weight)

# Gridlines and Spines
ax.set_axisbelow(True)
ax.yaxis.grid(True, which='both', linestyle='--', alpha=0.4, color='#CCCCCC')
for spine in ax.spines.values():
    spine.set_visible(False)

# Adjust y-limit for comfortable log padding
ax.set_ylim(10, 60000)

# Colorbar on the right side
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, pad=0.03, aspect=20)
cbar.set_label('RMSE ATE (m)', fontsize=11, fontweight='bold')
plt.legend()

plt.tight_layout()
plt.show()
