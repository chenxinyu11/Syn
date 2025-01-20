import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
import matplotlib.patches as mpatches
import os

data = pd.read_csv("shannon.csv")

lat = np.array(data['lat'])
lon = np.array(data['lon'])
change = np.array(data['shannon'])
plt.style.use('ggplot')
plt.figure(figsize=(10, 6))

map1 = Basemap(projection='robin', lat_0=90, lon_0=0,
               resolution='l', area_thresh=1000.0)

map1.drawmeridians(np.arange(0, 360, 60))
map1.drawparallels(np.arange(-90, 90, 30))

map1.drawcoastlines(linewidth=0.2)
map1.drawmapboundary(fill_color='white')
map1.fillcontinents(color='lightgrey', alpha=0.8)

#colors = np.where(change > 3, 'red',
#                 np.where(change < -3, 'blue', 'grey'))


#map1.scatter(lon, lat, latlon=True, alpha=1, s=10, c=colors,
#             linewidths=0, marker='s', zorder=1)

#counts = [np.sum(change > 3), np.sum(change < -3), np.sum((change >= -3) & (change <= 3))]
#labels = ['>3%', '<-3%', '-3% to 3%']
#colors_pie = ['red', 'blue', 'grey']


#ax = plt.gca()
#inset = ax.inset_axes([1.05, 0.75, 0.1, 0.1]) 
#inset.pie(counts, labels=labels, colors=colors_pie, autopct='%1.1f%%', textprops={'fontsize': 8})


sc = map1.scatter(lon, lat, latlon=True, alpha=1, s=10, c=change,
                  cmap='coolwarm', linewidths=0, marker='s', zorder=1)

cbar = map1.colorbar(sc, location='right', pad="5%")
cbar.set_label('abundance (RPM)')

plt.show()
plt.close()