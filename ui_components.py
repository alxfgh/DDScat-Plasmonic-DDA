import tkinter as tk
from tkinter import ttk, messagebox


class UIComponents:
    def __init__(
        self,
        root,
        add_layer_callback,
        remove_layer_callback,
        plot_callback,
        save_callback,
        save_simulation_parameter,
    ):
        self.root = root
        self.root.title("Core-Shell Nanoparticle Builder")

        # Callbacks for button actions
        self.add_layer_callback = add_layer_callback
        self.remove_layer_callback = remove_layer_callback
        self.plot_callback = plot_callback
        self.save_callback = save_callback
        self.save_simulation_parameter = save_simulation_parameter

        self.layers = []  # Store layers as (radius, comp)

        # UI for adding layers
        self.layer_frame = ttk.Frame(root)
        self.layer_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(self.layer_frame, text="Shell Radius (nm)").grid(
            row=0, column=0, padx=5
        )
        ttk.Label(self.layer_frame, text="Composition").grid(row=0, column=1, padx=5)

        self.radius_var = tk.DoubleVar()
        self.comp_var = tk.IntVar()

        self.radius_entry = ttk.Entry(
            self.layer_frame, textvariable=self.radius_var, width=10
        )
        self.radius_entry.grid(row=1, column=0, padx=5)
        self.comp_entry = ttk.Entry(
            self.layer_frame, textvariable=self.comp_var, width=10
        )
        self.comp_entry.grid(row=1, column=1, padx=5)

        ttk.Button(self.layer_frame, text="+ Add Layer", command=self.add_layer).grid(
            row=1, column=2, padx=5
        )
        ttk.Button(
            self.layer_frame,
            text="- Remove Last Layer",
            command=self.remove_layer,
        ).grid(row=1, column=3, padx=5)

        # Display layers
        self.layer_list = tk.Listbox(root, height=8)
        self.layer_list.pack(padx=10, pady=5, fill="x")

        # Buttons for Saving
        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(pady=10)

        ttk.Button(
            self.button_frame, text="Save Shape", command=self.save_callback
        ).pack(side="right", padx=5)

        ttk.Button(
            self.button_frame,
            text="Save Simulation Parameter",
            command=self.save_simulation_parameter,
        ).pack(side="right", padx=5)

    def add_layer(self):
        self.add_layer_callback()
        self.plot_callback()

    def remove_layer(self):
        self.remove_layer_callback()
        self.plot_callback()
