import matplotlib.pyplot as plt
from scripts.scraping.labels.collect_labels import *
from scripts.constants import *

# Get count of records
num_records = count_text_lines_in_directory(LABEL_SAVE_PATH)

x_field = 'temperature'
y_field = 'pressure'
r_field = 'sun_altitude'
g_field = 'sun_altitude'
b_field = 'sun_altitude'

filter_condition = lambda x: True or x[0] in {'K5ZEJWCTSzQ'}

r_mod = lambda r, g, b: min(max(1.50 * (r - 0.80) + 0.75, 0), 1)
g_mod = lambda r, g, b: min(max(2.20 * (g - 0.7) + 0.75, 0), 0.85)
b_mod = lambda r, g, b: min(max(0.2 * (b - 0.30) + 0.5, 0), 1)

point_size = 0.05
point_opacity = 0.5
shift_magnitude = 0.00

# Path containing the labels
x_index = LABEL_FILE_FIELDS.index(x_field)
y_index = LABEL_FILE_FIELDS.index(y_field)
r_index = LABEL_FILE_FIELDS.index(r_field)
g_index = LABEL_FILE_FIELDS.index(g_field)
b_index = LABEL_FILE_FIELDS.index(b_field)

# Initialize lists to store x and y values
x_values = np.zeros(num_records)
y_values = np.zeros(num_records)
t_values = np.zeros(num_records)
colors = np.zeros((num_records, 3))

x_max, x_min = None, None
y_max, y_min = None, None
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
                            is_valid_value(columns[b_index]) and filter_condition(columns)):

                        # Convert values to floats
                        x_value = float(columns[x_index])
                        y_value = float(columns[y_index])
                        t_value = float(columns[7]) + float(columns[1])
                        r_value = float(columns[r_index]) / 255.0
                        g_value = float(columns[g_index]) / 255.0
                        b_value = float(columns[b_index]) / 255.0

                        x_values[counted_records] = x_value
                        y_values[counted_records] = y_value
                        t_values[counted_records] = t_value
                        colors[counted_records] = np.array((r_value, g_value, b_value))

                        # Update max and min values for the rgb channels
                        x_max = x_value if x_max is None or x_value > x_max else x_max
                        x_min = x_value if x_min is None or x_value < x_min else x_min
                        y_max = y_value if y_max is None or y_value > y_max else y_max
                        y_min = y_value if y_min is None or y_value < y_min else y_min
                        t_max = t_value if t_max is None or t_value > t_max else t_max
                        t_min = t_value if t_min is None or t_value < t_min else t_min

                        r_max = r_value if r_max is None or r_value > r_max else r_max
                        r_min = r_value if r_min is None or r_value < r_min else r_min
                        g_max = g_value if g_max is None or g_value > g_max else g_max
                        g_min = g_value if g_min is None or g_value < g_min else g_min
                        b_max = b_value if b_max is None or b_value > b_max else b_max
                        b_min = b_value if b_min is None or b_value < b_min else b_min

                        counted_records += 1

x_values = x_values[:counted_records]
y_values = y_values[:counted_records]
t_values = t_values[:counted_records]
colors = colors[:counted_records]

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

print(t_max, t_min)

max_range = t_max - t_min
set_range = max_range
r1, r2 = 0, set_range
x_slice = x_values
y_slice = y_values

# Create the scatter plot
fig, ax = plt.subplots(facecolor='#222222')
ax.set_facecolor('#000000')
sc = ax.scatter(x_slice, y_slice, c=colors, s=point_size, alpha=point_opacity)


def on_key(event):
    global r1, r2, set_range, t_max, t_min

    if event.key == 'right':
        r1 = min(max_range - set_range, r1 + 1)
        r2 = min(max_range, r2 + 1)
    elif event.key == 'left':
        r1 = max(0, r1 - 1)
        r2 = max(set_range, r2 - 1)

    plt.draw()


fig.canvas.mpl_connect('key_press_event', on_key)


# Add labels and title
plt.xlabel(f'{x_field}')
plt.ylabel(f'{y_field}')
plt.title(f'{x_field} (x-axis) against {y_field} (y-axis)\n(red: {r_field}, green {g_field}, blue {b_field})')

# Show the plot
plt.show()
