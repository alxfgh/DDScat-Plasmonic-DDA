import tkinter as tk
from tkinter import messagebox
from ui_components import UIComponents
from plotting import Plotter
from data_handling import DataHandler


class NanoparticleBuilder:
    def __init__(self, root):
        self.layers = []
        self.plotter = Plotter(root)
        self.ui = UIComponents(
            root,
            add_layer_callback=self.add_layer,
            remove_layer_callback=self.remove_layer,
            plot_callback=self.plot_structure,
            save_callback=self.save_shape,
            save_simulation_parameter=self.save_simulation_parameter,
        )

    def add_layer(self):
        try:
            radius = self.ui.radius_var.get()
            comp = self.ui.comp_var.get()

            if radius <= 0 or comp <= 0:
                raise ValueError("Radius and Composition must be positive values.")

            if self.layers and radius <= self.layers[-1][0]:
                raise ValueError("Radius must be larger than the previous layer.")

            self.layers.append((radius, comp))
            self.ui.layer_list.insert(
                tk.END, f"Radius: {radius} nm, Composition: {comp}"
            )
            self.ui.radius_var.set(0)
            self.ui.comp_var.set(0)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def remove_layer(self):
        if self.layers:
            self.layers.pop()
            self.ui.layer_list.delete(tk.END)
            self.plot_structure()

    def plot_structure(self):
        try:
            self.plotter.plot_structure(self.layers)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def save_shape(self):
        try:
            DataHandler.save_shape(self.layers)
            messagebox.showinfo("Success", "Shape saved to shape.dat!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def save_simulation_parameter(self):
        try:
            DataHandler.save_simulation_parameter(self.layers)
            messagebox.showinfo("Success", "Simulation parameter saved to ddscat.par!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = NanoparticleBuilder(root)
    root.mainloop()
