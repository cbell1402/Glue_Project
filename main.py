import os.path
import sys
import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd
import datetime as dt
from sys import platform as sys_pf
from matplotlib.widgets import Button
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")


def my_function(t):
    # Define your function here
    return 11.0 + 0.0745 * t


def run():
    while True:
        for m in markers:
            # Get time delta from creation till now
            right_now = dt.datetime.now()
            delta = right_now - m.start_time

            # Update the marker's position
            x_pos = delta.total_seconds() / 60
            y_pos = my_function(delta.total_seconds() / 60)
            m.set_xdata(x_pos)
            m.set_ydata(y_pos)
            # m.pressure = np.float_(m.get_ydata())
            m.pressure = y_pos

            # Annotate marker with pressure
            text = "PSI: " + str(round(m.pressure, 3))
            m.anno.set_text(text)
            #m.anno.set_x(x_pos)
            #m.anno.set_y(y_pos)

        # Update the plot
        fig.canvas.draw()
        fig.canvas.flush_events()

        # Save the data
        save_data()


def add_marker(event):
    # Plot a marker
    marker, = ax.plot(0, my_function(0), 'o')
    setattr(marker, 'anno', ax.annotate('', (121, 14.1), xycoords='data'))
    setattr(marker, 'start_time', dt.datetime.now())
    setattr(marker, 'update_time', dt.datetime.now())
    setattr(marker, 'run', df['Run'].max() + 1)
    setattr(marker, 'end_time', 0)
    setattr(marker, 'pressure', 0)
    df.loc[marker.run, "Run"] = marker.run
    df.loc[marker.run, "Start Time"] = marker.start_time
    markers.append(marker)


def save_data():
    # Get the end time value
    end_time = dt.datetime.now()
    for m in markers:
        m.end_time = end_time
        df.loc[m.run, "Run"] = m.run
        df.loc[m.run, "Start Time"] = m.start_time
        df.loc[m.run, "End Time"] = m.end_time
        df.loc[m.run, "Pressure"] = m.pressure
    df.to_csv("glue_data.csv", index=False)
    # print("I have saved!")


def my_exit(event):
    save_data()
    #window.destroy()
    plt.close()


# Read in data file
if os.path.isfile("glue_data.csv"):
    data_file = pd.read_csv("glue_data.csv")
    df = pd.DataFrame(data_file)
else:
    data = {
        "Run": [0],
        "Start Time": [0],
        "End Time": [0],
        "Pressure": [0],
    }
    df = pd.DataFrame(data)


# Create a time array from 0 to 240 minutes with a step of 0.01
t = np.arange(0, 240, 1)

# Create an empty list to store the markers
markers = []

# Create a figure and axis objects
fig, ax = plt.subplots()

# Plot the function
line, = ax.plot(t, my_function(t))

# Set the axis labels and title
ax.set_xlabel('Time (min)')
ax.set_ylabel('Pressure (PSI)')
ax.set_title('Glue - Pressure vs Time')

# Set up the initial plot
plt.yticks(np.arange(10, 30, 1))
plt.xticks(np.arange(0, 241, 20))
plt.grid()

# Create a button to add markers
axadd = fig.add_axes([0.5, 0.15, 0.15, 0.075])
add_button = Button(axadd, "Add Marker")
add_button.on_clicked(add_marker)

# Create a button to close and save
axexit = fig.add_axes([0.66, 0.15, 0.15, 0.075])
exit_button = Button(axexit, "Save & Exit")
exit_button.on_clicked(my_exit)

# Show the plot
plt.show(block=False)

# Test block
#temp_anno = ax.annotate('', (120, 14))

#print(df)

running = True

while running:
    running = run()

# Close the plot window
my_exit()

