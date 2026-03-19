import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

df = pd.read_csv("species abundance_uncertainty.csv")

lon = df["Longitude"]
lat = df["Latitude"]
cv = df["CV_Uncertainty"]

fig = plt.figure(figsize=(12,6))
ax = plt.axes(projection=ccrs.Robinson())

ax.set_global()

ax.coastlines(linewidth=0.5)
ax.add_feature(cfeature.LAND, facecolor="lightgrey")

sc = ax.scatter(
    lon,
    lat,
    c=cv,
    cmap="viridis",
    s=5,
    transform=ccrs.PlateCarree()
)

cb = plt.colorbar(sc, orientation="horizontal", pad=0.05)
cb.set_label("Coefficient of variation")

plt.title("Species abundance model bootstrapped variance")
plt.show()
