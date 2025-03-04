import tkinter as tk
from tkinter import ttk
import subprocess, threading, csv, os
from concurrent.futures import ThreadPoolExecutor


# Define a Task object.
class Task:
    def __init__(self, path):
        self.path = path
        self.status = "Queued"


def run_task(task):
    task.status = "Running"
    # Launch the ddscat process in its folder
    proc = subprocess.Popen("sudo ./ddscat ddscat.par", cwd=task.path, shell=True)
    proc.wait()
    task.status = "Completed"


def start_tasks():
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(run_task, task) for task in tasks]
        for future in futures:
            future.result()  # wait for each task to finish


def update_gui():
    for i, task in enumerate(tasks):
        tree.set(task_ids[i], column="Status", value=task.status)
    root.after(1000, update_gui)


# Load tasks from CSV
tasks = []
with open("all_shells/config_paths.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        tasks.append(Task(row["path"]))

# Build the GUI
root = tk.Tk()
root.title("DDscat Task Runner")

tree = ttk.Treeview(root, columns=("Path", "Status"), show="headings")
tree.heading("Path", text="Path")
tree.heading("Status", text="Status")
tree.pack(fill=tk.BOTH, expand=True)

# Keep track of tree item IDs for easy updating.
task_ids = []
for task in tasks:
    task_ids.append(tree.insert("", tk.END, values=(task.path, task.status)))

start_btn = tk.Button(
    root,
    text="Start",
    command=lambda: threading.Thread(target=start_tasks, daemon=True).start(),
)
start_btn.pack(pady=10)

root.after(1000, update_gui)
root.mainloop()
