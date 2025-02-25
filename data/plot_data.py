import matplotlib.pyplot as plt
from scripts.localConfig import *
from scripts.scraping.labels.collect_labels import *

DATA_FILE_FIELDS = ['video_id', 'year', 'month', 'day', 'hour', 'minute', 'second'] + LABEL_NAMES

print(DATA_FILE_FIELDS)

x_data = 'sun_direction'
y_data = 'sun_altitude'
r_data = 'temperature'
g_data = 'pressure'
b_data = 'humidity'

# Define the directory containing the txt files
directory = LABEL_SAVE_PATH

# Define which columns to use for x and y (0-based index)
x_column = DATA_FILE_FIELDS.index(x_data)  # Change this to the desired column for x
y_column = DATA_FILE_FIELDS.index(y_data)  # Change this to the desired column for y
r_column = DATA_FILE_FIELDS.index(r_data)  # Change this to the desired column for y
g_column = DATA_FILE_FIELDS.index(g_data)  # Change this to the desired column for y
b_column = DATA_FILE_FIELDS.index(b_data)  # Change this to the desired column for y

# Initialize lists to store x and y values
x_values = []
y_values = []
colors = []
r_max, r_min = None, None
g_max, g_min = None, None
b_max, b_min = None, None

point_size = 0.5
point_opacity = 0.4


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
                    x_values.append(float(columns[x_column]))
                    y_values.append(float(columns[y_column]))

                    r_value = float(columns[r_column]) / 255.0
                    g_value = float(columns[g_column]) / 255.0
                    b_value = float(columns[b_column]) / 255.0

                    # Update max and min values for the rgb channels
                    r_max = r_value if r_max is None or r_value > r_max else r_max
                    r_min = r_value if r_min is None or r_value < r_min else r_min
                    g_max = g_value if g_max is None or g_value > g_max else g_max
                    g_min = g_value if g_min is None or g_value < g_min else g_min
                    b_max = b_value if b_max is None or b_value > b_max else b_max
                    b_min = b_value if b_min is None or b_value < b_min else b_min

                    colors.append((r_value, g_value, b_value))


# Adjust the color values to be within 0 to 1
for index in range(len(colors)):
    colors[index] = (
        colors[index][0] if r_max - r_min == 0 else (colors[index][0] - r_min) / (r_max - r_min),
        colors[index][1] if g_max - g_min == 0 else (colors[index][1] - g_min) / (g_max - g_min),
        colors[index][2] if b_max - b_min == 0 else (colors[index][2] - b_min) / (b_max - b_min)
    )

# Create the scatter plot
plt.figure(facecolor='#222222')
plt.gca().set_facecolor('#1a1a1a')
plt.scatter(x_values, y_values, c=colors, s=point_size, alpha=point_opacity)

# Add labels and title
plt.xlabel(f'{x_data}')
plt.ylabel(f'{y_data}')
plt.title(f'{x_data} (x-axis) against {y_data} (y-axis)\n(red: {r_data}, green {g_data}, blue {b_data})')

# Show the plot
plt.show()
