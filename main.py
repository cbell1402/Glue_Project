import os.path
import sys
import numpy as np
import matplotlib.pyplot as plt
import time
import tkinter as tk
import pandas as pd
import datetime as dt
from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")


def my_function(t):
    # Define your function here
    # return np.sin(2 * np.pi * t)  # Example: Sine wave
    # return np.exp(t)
    return (11 + 0.0745 * t)


def run():
    while True:
        for m in markers:
            # Get time delta from creation till now

            # Update the marker's position
            m.set_xdata(m.get_xdata() + 0.01)
            m.set_ydata(my_function(m.get_xdata()))
            m.viscosity = np.float_(m.get_ydata())

        # Update the plot
        fig.canvas.draw()
        fig.canvas.flush_events()

        # Pause for one second
        # time.sleep(1)

        #if my_exit() is False:
            #break
    #return False


def add_marker():
    # Plot a marker
    marker, = ax.plot(0, my_function(0), 'o')
    setattr(marker, 'start_time', dt.datetime.now())
    setattr(marker, 'run', df['Run'].max() + 1)
    setattr(marker, 'end_time', 0)
    setattr(marker, 'viscosity', 0)
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
        df.loc[m.run, "Viscosity"] = m.viscosity
    df.to_csv("glue_data.csv", index=False)
    print("I have saved!")
    #window.after(5000, save_data())


def my_exit():
    save_data()
    window.destroy()
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
        "Viscosity": [0],
    }
    df = pd.DataFrame(data)


# Create a time array from 0 to 10 seconds with a step of 0.01
t = np.arange(0, 20, 0.01)

# Create an empty list to store the markers
markers = []

# Create a figure and axis objects
fig, ax = plt.subplots()

# Plot the function
line, = ax.plot(t, my_function(t))

# Create the tkinter window
window = tk.Tk()

# Create a button to add markers
add_button = tk.Button(window, text="Add Marker", command=add_marker)
add_button.pack()

# Create a button to close and save
exit_button = tk.Button(window, text="Save and Exit", command=my_exit)
exit_button.pack()

# Start the tkinter event loop
# window.mainloop()

# Set the axis labels and title
ax.set_xlabel('Time (s)')
ax.set_ylabel('Function')
ax.set_title('Plotting a Function with Moving Marker')

# Show the initial plot
plt.show(block=False)

# Test block
#print(df)

running = True

# Start the tkinter event loop
#window.mainloop()

#window.after(5000, save_data())

while running:
    running = run()

# Close the plot window
plt.close()

