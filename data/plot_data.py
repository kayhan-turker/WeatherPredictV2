import matplotlib.pyplot as plt
import os

# Define the directory containing the txt files
directory = 'path/to/your/txt/files'

# Define which columns to use for x and y (0-based index)
x_column = 0  # Change this to the desired column for x
y_column = 2  # Change this to the desired column for y

# Initialize lists to store x and y values
x_values = []
y_values = []

# Iterate over all txt files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        with open(os.path.join(directory, filename), 'r') as file:
            for line in file:
                # Split the line into columns
                columns = line.strip().split(';')

                # Check if the selected columns are not None and are numeric
                if (columns[x_column] != 'None' and columns[y_column] != 'None' and
                        columns[x_column].replace('.', '', 1).isdigit() and
                        columns[y_column].replace('.', '', 1).isdigit()):
                    # Append the values to the lists
                    x_values.append(float(columns[x_column]))
                    y_values.append(float(columns[y_column]))

# Create the scatter plot
plt.scatter(x_values, y_values)

# Add labels and title
plt.xlabel(f'Column {x_column}')
plt.ylabel(f'Column {y_column}')
plt.title('Scatter Plot of Data')

# Show the plot
plt.show()