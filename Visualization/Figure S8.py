import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

df = pd.read_csv("extrapolation_map_2023.csv")
df["lon_360"] = df["lon"] % 360
lon = df["lon_360"]
lat = df["lat"]
extrap = df["final_extrapolation"]

fig = plt.figure(figsize=(12,6))
ax = plt.axes(projection=ccrs.Robinson(central_longitude=180))  # 中心经线 180°

ax.set_global()
ax.coastlines(linewidth=0.5)
ax.add_feature(cfeature.LAND, facecolor="lightgrey")
ax.add_feature(cfeature.OCEAN, facecolor="white")

sc = ax.scatter(
    lon,
    lat,
    c=extrap,
    cmap="inferno",
    s=5,
    transform=ccrs.PlateCarree()
)

cb = plt.colorbar(sc, orientation="horizontal", pad=0.05, shrink=0.7)
cb.set_label("Extrapolation")

plt.title("2023 model extrapolation")
plt.show()
