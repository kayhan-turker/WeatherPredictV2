import os
from datetime import datetime
from scripts.utils import *


def process_files(folder):
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            path = os.path.join(folder, file)
            with open(path, "r+") as f:
                lines = f.readlines()
                f.seek(0)
                for line in lines:
                    parts = line.strip().split(";")

                    dt = datetime(int(parts[1]), int(parts[2]), int(parts[3]),
                                  int(parts[4]), int(parts[5]), int(parts[6]))
                    parts[7] = str(round(get_decimal_year(dt) - dt.year, 4))
                    parts[8] = str(round(get_decimal_day(dt), 4))

                    f.write(";".join(parts) + "\n")
                f.truncate()


process_files("data/labels")