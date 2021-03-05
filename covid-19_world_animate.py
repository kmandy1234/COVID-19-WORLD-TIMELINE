import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.patches import Polygon
from matplotlib.colors import BoundaryNorm
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.animation import FuncAnimation 
from matplotlib.animation import FFMpegWriter
from matplotlib.colorbar import ColorbarBase  

#read the data
c19_data = pd.read_csv('covid_world.csv')

#set iso codes of countries as index
c19_data = c19_data.set_index('codes')

#get the iso_codes and dates as list
iso_codes = list(c19_data.index)
dates = list(c19_data.columns)

fig = plt.figure(num=None ,figsize=(13,9), dpi=100 ,facecolor='w', edgecolor='k')
ax= fig.add_subplot(111)
ax.set_title("COVID-19 INFECTIONS WORLDWIDE", fontsize=18)
date_text = ax.text(0.4,0.1,'',transform=ax.transAxes,fontsize=20)

#draw world map using Basemap library
m = Basemap(projection='cyl',llcrnrlat=-70,urcrnrlat=90,llcrnrlon=-180,urcrnrlon=180,resolution='l')
m.drawlsmask(land_color='white',ocean_color='#87CEFA',resolution='l')

#read world shapefile  
world=m.readshapefile(r'world_map\world_borders','world_borders',default_encoding='latin-1')


colors=['#FFE5E5','#FFCCCC','#FFC1C1','#FF6A6A','#FF6666','#FF4040','#FF3333','#FF3030','#FF0000','#EE0000','#CD0000','#8B0000','#800000','#660000','#330000']
bounds=[1,20,100,500,1000,5000,10000,30000,50000,75000,100000,2500000,5000000,7500000,10000000,30000000]
tick_labels=[1,20,100,500,'1 K','5 K','10 K','30 K','50 K','75 K','1 L','2.5 M','5 M', '7.5 M', '10 M','30 M']

#Mapping data onto colors using a colormap involves two steps: 
# data is first mapped onto the range 0-1 using a BoundaryNorm, 
#then this number is mapped to a color using LinearSegmentedColormap.
cmap = LinearSegmentedColormap.from_list('newcolor',colors)
norm = BoundaryNorm(bounds,cmap.N)

#define the colorbar
cbaxes = inset_axes(ax, width="3%", height="50%", loc=3) 
cb = ColorbarBase(cbaxes, cmap=cmap, norm=norm, ticks=bounds, boundaries=bounds, format='%1i',spacing='uniform')
cb.set_ticklabels(tick_labels)
fig.tight_layout()

#animate function colors each region according to the no. of cases. 
#this function is called repeatedly by FuncAnimation with each dates as a argument 
def animate(i):
    date_text.set_text(i)
    for info, shape in zip(m.world_borders_info, m.world_borders):
        if info['ISO3'] in iso_codes:
            cases = c19_data.at[info['ISO3'],i]
            country_color = cmap(norm(cases))
            ax.add_patch(Polygon(shape, fc=country_color, ec='white', lw=0.5))
output = FuncAnimation(fig, animate, dates, interval=1000, repeat = False)

#save the file as mp4
writer = FFMpegWriter(fps=10, metadata=dict(artist='Me'), bitrate=4000)
output.save('covid_animation.mp4', writer=writer)