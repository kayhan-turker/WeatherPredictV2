import matplotlib.pyplot as plt
from core.scrapers.collect_labels import *
from common.constants import *

# Get count of records
num_records = count_text_lines_in_directory(LABEL_SAVE_PATH)

x_field = 'longitude'
y_field = 'latitude'
r_field = 'temperature'
g_field = 'pressure'
b_field = 'humidity'

filter_condition = lambda x: True or x[0] in {'K5ZEJWCTSzQ'}

r_mod = lambda r, g, b: r
g_mod = lambda r, g, b: g
b_mod = lambda r, g, b: b

point_size = 2

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

                        # Store values into np array
                        x_values[counted_records] = float(columns[x_index])
                        y_values[counted_records] = float(columns[y_index])
                        t_values[counted_records] = float(columns[7]) + float(columns[1])
                        colors[counted_records] = np.array((
                            float(columns[r_index]) / 255.0,
                            float(columns[g_index]) / 255.0,
                            float(columns[b_index]) / 255.0))

                        counted_records += 1

x_values = x_values[:counted_records]
y_values = y_values[:counted_records]
t_values = t_values[:counted_records]
colors = colors[:counted_records]

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

# Time range setup
max_range = t_max - t_min
set_range = max_range
range_step = max_range / 50
t1, t2 = t_min, t_min + set_range

# Adjust visibility
visible = np.where((t_values >= t1) & (t_values <= t2), 1.0, 0.0)


def on_key(event):
    global t1, t2, t_max, t_min, max_range, set_range, range_step, visible

    if event.key == 'right':
        t1 = min(t_max - set_range, t1 + range_step)
        t2 = min(t_max, t2 + range_step)
    elif event.key == 'left':
        t1 = max(t_min, t1 - range_step)
        t2 = max(t_min + set_range, t2 - range_step)

    if event.key == 'up':
        set_range = min(max_range, set_range + range_step)
        if t1 > t_min:
            t1 = t2 - set_range
        else:
            t2 = t1 + set_range
    elif event.key == 'down':
        set_range = max(range_step, set_range - range_step)
        t1 = t2 - set_range

    # Update visibility mask in place (no reallocation)
    np.putmask(visible, (t_values >= t1) & (t_values <= t2), 1.0)
    np.putmask(visible, ~((t_values >= t1) & (t_values <= t2)), 0.0)

    # Update scatter plot without re-drawing everything
    sc.set_alpha(0.5 * visible + 0.01)
    plt.draw()


# Create the scatter plot
fig, ax = plt.subplots(facecolor='#222222')
ax.set_facecolor('#000000')
sc = ax.scatter(x_values, y_values, c=colors, s=point_size, alpha=(0.5 * visible + 0.01).astype(float))
fig.canvas.mpl_connect('key_press_event', on_key)


# Add labels and title
plt.xlabel(f'{x_field}')
plt.ylabel(f'{y_field}')
plt.title(f'{x_field} (x-axis) against {y_field} (y-axis)\n(red: {r_field}, green {g_field}, blue {b_field})')

# Show the plot
plt.show()
