#import matplotlib
import tkinter
#matplotlib.use("TkAgg")
import os.path
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
from sys import platform as sys_pf
from matplotlib.widgets import Button, TextBox
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")


def my_function(t):
    # Define your function here
    return 11.0 + 0.0745 * t


def run():
    while True:
        time.sleep(0.2)
        for m in markers:
            # Get time delta from creation till now
            right_now = dt.datetime.now()
            delta = right_now - m.start_time

            # Check if greater than four hours
            if delta.total_seconds() > (4 * 60 * 60):
                axend = fig.add_axes([0.35, 0.4, 0.3, 0.15])
                end_button = Button(axend, "FOUR HOURS - MIX NEW BATCH \n Press To Continue", color="red")
                end_button.on_clicked(end_press)
                status.set_x(0.105)
                status.set_text("Status: Stopped...")
                plt.waitforbuttonpress()


            # Update the marker's position
            x_pos = delta.total_seconds() / 60
            y_pos = my_function(delta.total_seconds() / 60)
            m.set_xdata(x_pos)
            m.set_ydata(y_pos)
            m.pressure = y_pos

            # Annotate marker with pressure
            if round(m.pressure, 2) % 0.5 == 0:
                text = str(round(m.pressure, 2)) + " PSI"
                text_box.set_val(text)
                text_box.stop_typing()

        # Update the plot
        fig.canvas.draw()
        fig.canvas.flush_events()

        # Save the data
        save_data()


def add_marker(event):
    # Plot a marker
    marker, = ax.plot(0, my_function(0), 'o')
    setattr(marker, 'start_time', dt.datetime.now())
    setattr(marker, 'update_time', dt.datetime.now())
    setattr(marker, 'run', df['Run'].max() + 1)
    setattr(marker, 'end_time', 0)
    setattr(marker, 'pressure', 0)
    df.loc[marker.run, "Run"] = marker.run
    df.loc[marker.run, "Start Time"] = marker.start_time
    markers.append(marker)
    print(markers)
    print(len(markers))
    status.set_x(0.115)
    status.set_text("Status: Running")
    add_button.active = False


def check_markers():
    # Check for previous markers with time < 4 hours
    right_now = dt.datetime.now()
    time_list = df['Start Time'].to_list()
    for m in time_list[1:]:
        m_dt = dt.datetime.strptime(m, "%Y-%m-%d %H:%M:%S.%f")
        delta = right_now - m_dt
        run = df.loc[df['Start Time'] == m].iat[0, 0]

        # Add those markers if < 4 hours
        if delta.total_seconds() < (4 * 60 * 60):
            marker, = ax.plot(delta.total_seconds() / 60, my_function(delta.total_seconds() / 60), 'o')
            setattr(marker, 'anno', ax.annotate('', (200, 24.1 - len(markers)), xycoords='data'))
            setattr(marker, 'start_time', m_dt)
            setattr(marker, 'update_time', dt.datetime.now())
            setattr(marker, 'run', run)
            setattr(marker, 'end_time', dt.datetime.now())
            setattr(marker, 'pressure', my_function(delta.total_seconds() / 60))
            df.loc[marker.run, "Run"] = marker.run
            df.loc[marker.run, "Start Time"] = marker.start_time
            markers.append(marker)
            # Change Status
            status.set_x(0.115)
            status.set_text("Status: Running")
            add_button.active = False
            # Update pressure
            psi_value = round(marker.pressure * 2) / 2
            text = str(psi_value) + " PSI"
            text_box.set_val(text)
            text_box.stop_typing()


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


def remove_data(event):
    os.remove("glue_data.csv")
    os.execv(sys.executable, ['python'] + sys.argv)


def end_press(event):
    os.execv(sys.executable, ['python'] + sys.argv)


def my_exit():
    save_data()
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
fig, ax = plt.subplots(figsize=(9,5), facecolor="cornflowerblue")
fig.subplots_adjust(left=0.5, bottom=0.2)

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
axadd = fig.add_axes([0.1, 0.3, 0.2, 0.075])
add_button = Button(axadd, "Start", color="limegreen")
add_button.on_clicked(add_marker)

# Create a button to close and save
axexit = fig.add_axes([0.1, 0.2, 0.2, 0.075])
exit_button = Button(axexit, "Clear", color="red")
exit_button.on_clicked(remove_data)

# Create PSI text box
axtext = fig.add_axes([0.1, 0.5, 0.2, 0.075])
text_box = TextBox(axtext, "", textalignment="center")

# Create text for pressure and status
pressure = plt.text(0.155, 0.59, "Pressure", fontsize=14, transform=plt.gcf().transFigure)
status = plt.text(0.14, 0.4, "Status: Off", fontsize=14, transform=plt.gcf().transFigure)
title = plt.text(0.092, 0.8, "Glue Tracker", fontsize=24, transform=plt.gcf().transFigure)

# Show the plot
plt.show(block=False)

running = True

check_markers()
while running:
    running = run()

# Close the plot window
my_exit()
