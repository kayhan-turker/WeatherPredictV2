import matplotlib.pyplot as plt
import matplotlib
from core.scrapers.collect_labels import *
from common.constants import *
import numpy as np
from matplotlib.animation import FuncAnimation
import sys


# Use TkAgg for real-time updates
matplotlib.use("TkAgg")

# Define key states
key_states = {"left": False, "right": False}


# Get count of records
num_records = count_text_lines_in_directory(LABEL_SAVE_PATH) + 1
source_list = sorted(get_text_file_list_in_directory(LABEL_SAVE_PATH))
num_sources = len(source_list)

x_field = 'longitude'
y_field = 'latitude'
r_field = 'temperature'
g_field = 'pressure'
b_field = 'humidity'

r_mod = lambda r, g, b: r  # min(max(1.50 * (r - 0.80) + 0.75, 0), 1)
g_mod = lambda r, g, b: g  # min(max(2.20 * (g - 0.7) + 0.75, 0), 0.85)
b_mod = lambda r, g, b: b  # min(max(0.2 * (b - 0.30) + 0.8, 0), 1)
point_size = 1
fade_time = 0.2

# Path containing the labels
x_index = LABEL_FILE_FIELDS.index(x_field)
y_index = LABEL_FILE_FIELDS.index(y_field)
r_index = LABEL_FILE_FIELDS.index(r_field)
g_index = LABEL_FILE_FIELDS.index(g_field)
b_index = LABEL_FILE_FIELDS.index(b_field)

# Initialize lists to store x and y values
source_values = np.zeros(num_records)
x_values = np.zeros(num_records)
y_values = np.zeros(num_records)
t_values = np.zeros(num_records)
colors = np.zeros((num_records, 3))

t_max, t_min = None, None
r_max, r_min = None, None
g_max, g_min = None, None
b_max, b_min = None, None


def is_valid_value(value):
    return value != 'None' and value.replace('.', '', 1).replace('-', '', 1).isdigit()


# Iterate over all txt files in the directory
counted_records = 0
for filename in os.listdir(LABEL_SAVE_PATH):
    if filename.endswith('.txt'):
        with open(os.path.join(LABEL_SAVE_PATH, filename), 'r') as file:
            for line in file:
                if line.strip():
                    # Split the line into a list
                    columns = line.strip().split(';')

                    # Check if the selected columns are not None and are numeric
                    if (is_valid_value(columns[x_index]) and is_valid_value(columns[y_index]) and
                            is_valid_value(columns[r_index]) and is_valid_value(columns[g_index]) and
                            is_valid_value(columns[b_index])):

                        # Store values into np array
                        source_values[counted_records] = int(source_list.index(columns[0]))
                        x_values[counted_records] = float(columns[x_index])
                        y_values[counted_records] = float(columns[y_index])
                        t_values[counted_records] = float(columns[7]) + float(columns[1])
                        colors[counted_records] = np.array((
                            float(columns[r_index]) / 255.0,
                            float(columns[g_index]) / 255.0,
                            float(columns[b_index]) / 255.0))

                        counted_records += 1

source_values = source_values[:counted_records]
x_values = x_values[:counted_records]
y_values = y_values[:counted_records]
t_values = t_values[:counted_records]
t_values = (t_values - round(t_values.min())) * 100
colors = colors[:counted_records]

x_max, x_min = x_values.max(), x_values.min()
y_max, y_min = y_values.max(), y_values.min()
t_max, t_min = t_values.max(), t_values.min()
r_max, r_min = colors[:, 0].max(), colors[:, 0].min()
g_max, g_min = colors[:, 1].max(), colors[:, 1].min()
b_max, b_min = colors[:, 2].max(), colors[:, 2].min()

# Adjust the color values
for index in range(len(colors)):
    colors[index] = (
        colors[index][0] if r_max - r_min == 0 else (colors[index][0] - r_min) / (r_max - r_min),
        colors[index][1] if g_max - g_min == 0 else (colors[index][1] - g_min) / (g_max - g_min),
        colors[index][2] if b_max - b_min == 0 else (colors[index][2] - b_min) / (b_max - b_min)
    )

    colors[index] = (
        r_mod(colors[index][0], colors[index][1], colors[index][2]),
        g_mod(colors[index][0], colors[index][1], colors[index][2]),
        b_mod(colors[index][0], colors[index][1], colors[index][2]),
    )


# Plot setup
fig, ax = plt.subplots(facecolor='#222222')
ax.set_facecolor('#000000')
sc = ax.scatter([], [], c=[], s=point_size, alpha=0.0)

# Point in time setup
set_t = (t_max + t_min) / 2
t_step = (t_max - t_min) / 100
xt = np.zeros(num_sources)
yt = np.zeros(num_sources)
ct = np.zeros((num_sources, 3))
vt = np.zeros(num_sources)


def update_points_for_t():
    global set_t, xt, yt, ct, vt

    for i in range(num_sources):
        mask = np.array(source_values == i)  # Select only rows matching the category
        if not mask.any():
            continue

        t_s, x_s, y_s, c_s = t_values[mask], x_values[mask], y_values[mask], colors[mask]

        # Sort by time for safe interpolation
        sorted_idx = np.argsort(t_s)
        t_s, x_s, y_s, c_s = t_s[sorted_idx], x_s[sorted_idx], y_s[sorted_idx], c_s[sorted_idx]

        # Find closest lower and upper time indices
        low_idx = np.searchsorted(t_s, set_t, side='right') - 1
        high_idx = low_idx + 1

        if 0 <= low_idx < len(t_s) - 1 and t_s[low_idx] <= set_t <= t_s[high_idx]:
            # Linear interpolation for x and y
            t_low, t_high = t_s[low_idx], t_s[high_idx]
            x_low, x_high = x_s[low_idx], x_s[high_idx]
            y_low, y_high = y_s[low_idx], y_s[high_idx]
            c_low, c_high = c_s[low_idx], c_s[high_idx]

            interp = (set_t - t_low) / (t_high - t_low)
            xt[i] = (1 - interp) * x_low + interp * x_high
            yt[i] = (1 - interp) * y_low + interp * y_high
            ct[i] = (1 - interp) * c_low + interp * c_high
        else:
            # Assign the closest available value (out of range)
            closest_idx = np.argmin(np.abs(t_s - set_t))
            xt[i], yt[i], ct[i] = x_s[closest_idx], y_s[closest_idx], c_s[closest_idx]

        nearest_t_dist = np.min(np.abs(t_s - set_t))
        vt[i] = fade_time / (nearest_t_dist + fade_time)


def update_plot():
    global sc, ax, xt, yt, ct, vt

    sc.set_offsets(np.column_stack((xt, yt)))
    sc.set_facecolor(ct)
    sc.set_alpha(vt.astype(float))

    fig.canvas.draw_idle()


def on_key_press(event):
    global key_states
    if event.key == "right":
        key_states["right"] = True
    elif event.key == "left":
        key_states["left"] = True


def on_key_release(event):
    global key_states
    if event.key == "right":
        key_states["right"] = False
    elif event.key == "left":
        key_states["left"] = False
    elif event.key == "q":
        close_plot()


def animation_update(_):
    global t_max, t_min, set_t, t_step
    if key_states["right"]:
        set_t = min(t_max, set_t + t_step)
        update_points_for_t()
        update_plot()
    elif key_states["left"]:
        set_t = max(t_min, set_t - t_step)
        update_points_for_t()
        update_plot()


def close_plot(event=None):
    ani.event_source.stop()  # Stop FuncAnimation loop
    plt.close(fig)  # Close plot window
    sys.exit(0)  # Ensure script exits completely


# Initialize plot
update_points_for_t()
sc = ax.scatter(xt, yt, c=ct, s=point_size, alpha=vt.astype(float))
ax.set_xlim(x_min - (x_max - x_min) * 0.001, x_max + (x_max - x_min) * 0.001)
ax.set_ylim(y_min - (y_max - y_min) * 0.001, y_max + (y_max - y_min) * 0.001)

fig.canvas.mpl_connect("close_event", close_plot)
fig.canvas.mpl_connect("key_press_event", on_key_press)
fig.canvas.mpl_connect("key_release_event", on_key_release)

ani = FuncAnimation(fig, animation_update, interval=10)

# Add labels and title
plt.xlabel(f'{x_field}')
plt.ylabel(f'{y_field}')
plt.title(f'{x_field} (x-axis) against {y_field} (y-axis)\n(red: {r_field}, green {g_field}, blue {b_field})')
plt.show()


