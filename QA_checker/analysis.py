import rasterio
import numpy as np
import os
from scipy.ndimage import generic_filter

def elevation_summary(dem_path):
    with rasterio.open(dem_path) as src:
        dem = src.read(1, masked=True)
        stats = {
            "min": float(np.min(dem)),
            "max": float(np.max(dem)),
            "mean": float(np.mean(dem)),
            "std": float(np.std(dem))
        }
    return stats

def slope_analysis(dem_path):
    with rasterio.open(dem_path) as src:
        dem = src.read(1, masked=True)
        transform = src.transform
        cellsize_x = transform.a
        cellsize_y = -transform.e

    dzdx = np.gradient(dem, axis=1) / cellsize_x
    dzdy = np.gradient(dem, axis=0) / cellsize_y

    slope = np.sqrt(dzdx**2 + dzdy**2)
    slope_degrees = np.degrees(np.arctan(slope))
    return slope_degrees

def point_density(point_cloud_path):
    try:
        import laspy
    except ImportError:
        raise ImportError("laspy is required for point cloud processing. Install with `pip install laspy`.")

    las = laspy.read(point_cloud_path)
    x, y = las.x, las.y
    area = (max(x) - min(x)) * (max(y) - min(y))
    num_points = len(x)
    density = num_points / area if area > 0 else 0
    return {
        "point_count": num_points,
        "area_m2": area,
        "avg_density_ppm2": density
    }

def dem_resolution(dem_path):
    with rasterio.open(dem_path) as src:
        transform = src.transform
        return abs(transform.a), abs(transform.e)
