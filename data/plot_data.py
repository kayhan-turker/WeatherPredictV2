import matplotlib.pyplot as plt
import numpy as np
from scripts.scraping.labels.collect_labels import *
from scripts.constants import *


x_data = 'temperature'
y_data = 'pressure'
r_data = 'sun_altitude'
g_data = 'sun_altitude'
b_data = 'sun_altitude'

r_mod = lambda r, g, b: min(max(2.0 * (r - 0.95) + 0.75, 0), 1)  # r * (1 - g)
g_mod = lambda r, g, b: min(max(1.0 * (g - 0.25) + 0.00, 0), 1)  # 0.5 * (r * (1 + g) + 0.5 * g * (1 - r))  # (1 - abs(2 * g - 1)) * b
b_mod = lambda r, g, b: min(max(0.2 * (b - 0.5) + 0.30, 0), 1)  # (1 - b) - (1 - 0.5 * g) * (1 - r) * 0.5

point_size = 0.05
point_opacity = 0.5
shift_magnitude = 0.003

# Path containing the labels
directory = LABEL_SAVE_PATH

x_column = LABEL_FILE_FIELDS.index(x_data)
y_column = LABEL_FILE_FIELDS.index(y_data)
r_column = LABEL_FILE_FIELDS.index(r_data)
g_column = LABEL_FILE_FIELDS.index(g_data)
b_column = LABEL_FILE_FIELDS.index(b_data)

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
        r_mod(colors[index][0], colors[index][1], colors[index][2]),
        g_mod(colors[index][0], colors[index][1], colors[index][2]),
        b_mod(colors[index][0], colors[index][1], colors[index][2]),
    )

# Shift points randomly to reduce overlaying
x_mag = (x_max - x_min) * shift_magnitude
y_mag = (y_max - y_min) * shift_magnitude
x_shifted = x_values + np.random.uniform(-x_mag, x_mag, size=len(x_values))
y_shifted = y_values + np.random.uniform(-y_mag, y_mag, size=len(y_values))

# Create the scatter plot
plt.figure(facecolor='#222222')
plt.gca().set_facecolor('#000000')
plt.scatter(x_shifted, y_shifted, c=colors, s=point_size, alpha=point_opacity)

# Add labels and title
plt.xlabel(f'{x_data}')
plt.ylabel(f'{y_data}')
plt.title(f'{x_data} (x-axis) against {y_data} (y-axis)\n(red: {r_data}, green {g_data}, blue {b_data})')

# Show the plot
plt.show()
