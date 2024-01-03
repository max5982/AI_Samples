import sys
import subprocess
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


app = QApplication(sys.argv)

# Function to get the current GPU memory usage
def get_gpu_memory():
    result = subprocess.run(
        ['nvidia-smi', '--query-gpu=memory.used', '--format=csv,nounits,noheader'],
        encoding='utf-8',
        stdout=subprocess.PIPE)
    return int(result.stdout.strip())

# Function to update the graph
def update_graph(usage_data):
    plt.cla()
    plt.plot(usage_data)
    plt.title('GPU Memory Usage Over Time')
    plt.xlabel('Time')
    plt.ylabel('Memory Used (MB)')
    plt.tight_layout()


# Setup the figure and canvas
fig = plt.figure()
fig.canvas.manager.set_window_title('GPU RAM Usage Monitor')
canvas = FigureCanvasQTAgg(fig)

# Function to be called when the window is closed
def on_close(event):
    sys.exit(0)  # Exit the program with status 0

# Connect the close event to the on_close function
fig.canvas.mpl_connect('close_event', on_close)

# Main loop to update the graph
usage_data = []
plt.ion()

for _ in range(1000):  # Run for 1000 seconds
    usage = get_gpu_memory()
    usage_data.append(usage)
    update_graph(usage_data)
    plt.pause(0.5)
    app.processEvents()  # Process any GUI events

plt.ioff()  # Turn interactive mode off
plt.show()

