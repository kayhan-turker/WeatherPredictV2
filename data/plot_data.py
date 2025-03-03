import matplotlib.pyplot as plt
import numpy as np
from scripts.localConfig import *
from scripts.scraping.labels.collect_labels import *

DATA_FILE_FIELDS = ['video_id', 'year', 'month', 'day', 'hour', 'minute', 'second'] + LABEL_NAMES

print(DATA_FILE_FIELDS)

preset = 7
preset_metadata = [
    # X-AXIS, Y-AXIS, R-AXIS, G-AXIS, B-AXIS, r-mod, g-mod, b-mod, p-size, p-alph, p-blur
    ['longitude', 'latitude', 'longitude', 'longitude', 'latitude',             0, 1, 0,    0.1, 0.1, 0.0],     # 0. LOCATION MAP
    ['temperature', 'pressure', 'longitude', 'longitude', 'latitude',           0, 1, 0,    0.1, 0.05, 0.001],  # 1. T P LOCATION
    ['temperature', 'humidity', 'longitude', 'longitude', 'latitude',           0, 1, 0,    0.1, 0.05, 0.001],  # 2. T H LOCATION
    ['temperature', 'pressure', 'sun_altitude', 'sun_altitude', 'date',         0, 0, 1,    0.1, 0.05, 0.001],  # 3. T P DATETIME
    ['temperature', 'humidity', 'sun_altitude', 'sun_altitude', 'date',         0, 0, 1,    0.1, 0.05, 0.001],  # 4. T H DATETIME
    ['temperature', 'pressure', 'latitude', 'date', 'sun_altitude',             2, 0, 0,    0.1, 0.05, 0.001],  # 5. T P DTLOC
    ['temperature', 'humidity', 'latitude', 'date', 'sun_altitude',             2, 0, 0,    0.1, 0.05, 0.001],  # 6. T H DTLOC
    ['temperature', 'pressure', 'sun_direction', 'sun_altitude', 'sun_direction', 0, 0, 1, 0.1, 0.05, 0.0],
]

mod_list = [
    lambda x: x,                    # 0 positive
    lambda x: 1 - x,                # 1 negative
    lambda x: 1 - abs(2 * x - 1),   # 2 cyclical
    lambda x: abs(2 * x - 1),       # 3 reverse cyclical
    lambda x: 0.5 * (0.5 + x),      # 4 muted
    lambda x: 0,                    # 5 zero
    lambda x: 1,                    # 6 one
    lambda x: 0.5                   # 7 half
]

x_data = preset_metadata[preset][0]
y_data = preset_metadata[preset][1]
r_data = preset_metadata[preset][2]
g_data = preset_metadata[preset][3]
b_data = preset_metadata[preset][4]

r_mod = preset_metadata[preset][5]
g_mod = preset_metadata[preset][6]
b_mod = preset_metadata[preset][7]

point_size = preset_metadata[preset][8]
point_opacity = preset_metadata[preset][9]
shift_magnitude = preset_metadata[preset][10]

# Path containing the labels
directory = LABEL_SAVE_PATH

x_column = DATA_FILE_FIELDS.index(x_data)
y_column = DATA_FILE_FIELDS.index(y_data)
r_column = DATA_FILE_FIELDS.index(r_data)
g_column = DATA_FILE_FIELDS.index(g_data)
b_column = DATA_FILE_FIELDS.index(b_data)

# Initialize lists to store x and y values
x_values = []
y_values = []
colors = []
x_max, x_min = None, None
y_max, y_min = None, None
r_max, r_min = None, None
g_max, g_min = None, None
b_max, b_min = None, None


def is_valid_value(value):
    return value != 'None' and value.replace('.', '', 1).replace('-', '', 1).isdigit()


# Iterate over all txt files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        with open(os.path.join(directory, filename), 'r') as file:
            for line in file:
                # Split the line into a list
                columns = line.strip().split(';')

                # Check if the selected columns are not None and are numeric
                if (is_valid_value(columns[x_column]) and is_valid_value(columns[y_column]) and
                        is_valid_value(columns[r_column]) and is_valid_value(columns[g_column]) and
                        is_valid_value(columns[b_column])):

                    # Convert values to floats
                    x_value = float(columns[x_column])
                    y_value = float(columns[y_column])
                    r_value = float(columns[r_column]) / 255.0
                    g_value = float(columns[g_column]) / 255.0
                    b_value = float(columns[b_column]) / 255.0

                    x_values.append(x_value)
                    y_values.append(y_value)
                    colors.append((r_value, g_value, b_value))

                    # Update max and min values for the rgb channels
                    x_max = x_value if x_max is None or x_value > x_max else x_max
                    x_min = x_value if x_min is None or x_value < x_min else x_min
                    y_max = y_value if y_max is None or y_value > y_max else y_max
                    y_min = y_value if y_min is None or y_value < y_min else y_min
                    r_max = r_value if r_max is None or r_value > r_max else r_max
                    r_min = r_value if r_min is None or r_value < r_min else r_min
                    g_max = g_value if g_max is None or g_value > g_max else g_max
                    g_min = g_value if g_min is None or g_value < g_min else g_min
                    b_max = b_value if b_max is None or b_value > b_max else b_max
                    b_min = b_value if b_min is None or b_value < b_min else b_min


# Adjust the color values to be within 0 to 1
for index in range(len(colors)):
    colors[index] = (
        colors[index][0] if r_max - r_min == 0 else (colors[index][0] - r_min) / (r_max - r_min),
        colors[index][1] if g_max - g_min == 0 else (colors[index][1] - g_min) / (g_max - g_min),
        colors[index][2] if b_max - b_min == 0 else (colors[index][2] - b_min) / (b_max - b_min)
    )

    # Set the median to be the brightest if required (rather than maximum value)
    colors[index] = (
        mod_list[r_mod](colors[index][0]),
        mod_list[g_mod](colors[index][1]),
        mod_list[b_mod](colors[index][2]),
    )

# Shift points randomly to reduce overlaying
x_mag = (x_max - x_min) * shift_magnitude
y_mag = (y_max - y_min) * shift_magnitude
x_shifted = x_values + np.random.uniform(-x_mag, x_mag, size=len(x_values))
y_shifted = y_values + np.random.uniform(-y_mag, y_mag, size=len(y_values))

# Create the scatter plot
plt.figure(facecolor='#222222')
plt.gca().set_facecolor('#1a1a1a')
plt.scatter(x_shifted, y_shifted, c=colors, s=point_size, alpha=point_opacity)

# Add labels and title
plt.xlabel(f'{x_data}')
plt.ylabel(f'{y_data}')
plt.title(f'{x_data} (x-axis) against {y_data} (y-axis)\n(red: {r_data}, green {g_data}, blue {b_data})')

# Show the plot
plt.show()
