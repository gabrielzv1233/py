import tkinter as tk
import psutil
import GPUtil

def update_stats():
    cpu_percent = psutil.cpu_percent(interval=1)
    gpus = GPUtil.getGPUs()
    gpu_info = ""
    if gpus:
        for gpu in gpus:
            gpu_info += f" | GPU {gpu.id} Usage: {gpu.load * 100:.2f}% | GPU {gpu.id} Memory: {gpu.memoryUsed}/{gpu.memoryTotal}MB"
    else:
        gpu_info = " | No GPU detected"

    stats_label.config(text=f"CPU Usage: {cpu_percent}%{gpu_info}")
    root.after(1000, update_stats)  # Update every 1000 milliseconds (1 second)

# Create the main window
root = tk.Tk()
root.title("System Monitor")

# Create a Label widget to display CPU and GPU usage
stats_label = tk.Label(root, font=('Arial', 12))
stats_label.pack(padx=20, pady=20)

# Start updating stats
update_stats()

# Start the Tkinter main loop
root.mainloop()
