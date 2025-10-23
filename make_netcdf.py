
import numpy as np
from netCDF4 import Dataset
import os

# === Constants ===
syr, eyr = 1901, 2022
nlon, nlat = 720, 360
nland = 67420
pi = np.pi
larea_base = 1.0e6 * (40075.0 / 720.0) ** 2  # m^2
output_dir = 'data/dgvm/output'

# === Read input binary files ===
lonlat = np.fromfile('data/dgvm/lonslats.bin', dtype=np.float32)
lon = lonlat[:nlon]
lat = lonlat[nlon:]

coords = np.fromfile('data/dgvm/coords.bin', dtype=np.int32)
xk = coords[:nland]
yk = coords[nland:]

# === Prepare for writing MPP_ann.txt ===
output_file = os.path.join(output_dir, 'MPP_ann.txt')
with open(output_file, 'w') as f:
    for year in range(syr, eyr + 1):
        # Load annual file
        filename = f'MPP_mean_{year}.bin'
        filepath = os.path.join(output_dir, filename)
        if not os.path.exists(filepath):
            print(f"⚠️ Missing file: {filepath}")
            continue
        
        data = np.fromfile(filepath, dtype=np.float32)
        MPP_mean_ann = data[:nland]
        NEE_mean_ann = data[nland:]
        
        MPP_global_ann = 0.0
        NEE_global_ann = 0.0

        for k in range(nland):
            larea = np.cos(lat[yk[k]] * pi / 180.0) * larea_base
            MPP_global_ann += larea * MPP_mean_ann[k]
            NEE_global_ann += larea * NEE_mean_ann[k]

        # Convert to PgC/yr and write
        MPP_pg = MPP_global_ann / 1.0e15
        NEE_pg = NEE_global_ann / 1.0e15
        print(f"{year}: MPP = {MPP_pg:.3f}, NEE = {NEE_pg:.3f}")
        f.write(f"{year} {MPP_pg:.6f} {NEE_pg:.6f}\n")

print(f"\n✅ Finished writing: {output_file}")