# photogrammetry_gui.py

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import numpy as np

from QA_checker.analysis import (
    elevation_summary,
    slope_analysis,
    point_density,
    dem_resolution
)

def select_dem():
    path = filedialog.askopenfilename(title="Select DEM File", filetypes=[("GeoTIFF files", "*.tif")])
    if path:
        dem_entry.delete(0, tk.END)
        dem_entry.insert(0, path)

def select_pointcloud():
    path = filedialog.askopenfilename(title="Select Point Cloud File", filetypes=[("LAS files", "*.las"), ("LAZ files", "*.laz")])
    if path:
        pc_entry.delete(0, tk.END)
        pc_entry.insert(0, path)

def run_analysis():
    results_box.delete("1.0", tk.END)
    dem_path = dem_entry.get()
    pc_path = pc_entry.get()

    if not os.path.isfile(dem_path):
        messagebox.showerror("Error", "DEM file not found.")
        return

    try:
        stats = elevation_summary(dem_path)
        res = dem_resolution(dem_path)
        slope_map = slope_analysis(dem_path)

        results_box.insert(tk.END, "--- Elevation Summary ---\n")
        for k, v in stats.items():
            results_box.insert(tk.END, f"{k}: {v:.2f}\n")

        results_box.insert(tk.END, f"\n--- DEM Resolution ---\nPixel size: {res[0]:.2f}m x {res[1]:.2f}m\n")

        results_box.insert(tk.END, "\n--- Slope Analysis ---\n")
        results_box.insert(tk.END, f"Slope (deg) - min: {np.min(slope_map):.2f}, max: {np.max(slope_map):.2f}, mean: {np.mean(slope_map):.2f}\n")
    except Exception as e:
        results_box.insert(tk.END, f"Error processing DEM: {str(e)}\n")

    if os.path.isfile(pc_path):
        try:
            density_info = point_density(pc_path)
            results_box.insert(tk.END, "\n--- Point Cloud Density ---\n")
            for k, v in density_info.items():
                results_box.insert(tk.END, f"{k}: {v:.2f}\n")
        except Exception as e:
            results_box.insert(tk.END, f"Error processing point cloud: {str(e)}\n")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Drone Photogrammetry QA Tool")

    frm = ttk.Frame(root, padding=10)
    frm.grid(row=0, column=0, sticky="nsew")

    ttk.Label(frm, text="DEM File:").grid(row=0, column=0, sticky="w")
    dem_entry = ttk.Entry(frm, width=50)
    dem_entry.grid(row=0, column=1, padx=5)
    ttk.Button(frm, text="Browse", command=select_dem).grid(row=0, column=2)

    ttk.Label(frm, text="Point Cloud File:").grid(row=1, column=0, sticky="w")
    pc_entry = ttk.Entry(frm, width=50)
    pc_entry.grid(row=1, column=1, padx=5)
    ttk.Button(frm, text="Browse", command=select_pointcloud).grid(row=1, column=2)

    ttk.Button(frm, text="Run QA Analysis", command=run_analysis).grid(row=2, column=0, columnspan=3, pady=10)

    results_box = tk.Text(frm, width=80, height=25)
    results_box.grid(row=3, column=0, columnspan=3, pady=5)

    root.mainloop()
