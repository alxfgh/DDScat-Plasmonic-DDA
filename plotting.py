import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Plotter:
    def __init__(self, root):
        self.figure = Figure(figsize=(5, 4))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(padx=10, pady=5)

    def plot_structure(self, layers):
        if not layers:
            raise ValueError("No layers to plot.")

        # Clear and recreate plot
        self.ax.clear()
        # Clear and recreate the figure and axes to ensure a clean plot
        self.figure.clf()  # Clear the entire figure
        self.ax = self.figure.add_subplot(111)  # Recreate the axes

        N = 256
        L = 0.160  # microns
        d = L / N

        x = np.linspace(-L / 2, L / 2, N)
        y = np.linspace(-L / 2, L / 2, N)
        X, Y = np.meshgrid(x, y)
        r = np.sqrt(X**2 + Y**2) * 1e3  # Convert to nm

        composition_grid = np.zeros_like(r, dtype=int)
        for layer_radius, comp in layers:
            composition_grid[(r <= layer_radius) & (composition_grid == 0)] = comp

        cax = self.ax.imshow(
            composition_grid,
            cmap="viridis",
            origin="lower",
            extent=[-L / 2 * 1e3, L / 2 * 1e3, -L / 2 * 1e3, L / 2 * 1e3],
        )
        self.ax.set_title("2D Cross-Section of Nanoparticle")
        self.ax.set_xlabel("X (nm)")
        self.ax.set_ylabel("Y (nm)")

        self.figure.colorbar(cax, ax=self.ax, label="Composition")
        self.canvas.draw()
