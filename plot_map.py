#!/usr/bin/env python3

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import argparse

# supress decompression bomb warning
from PIL import Image
Image.MAX_IMAGE_PIXELS = 1000000000

from transatlancair.load_flights import load_flights

STOPS = {
  'KLAX':None,
  'KSQL':(37.5151, -122.2504),
  'KGTF':(47.4825, 111.3566),
}

def plot_map(args):
  fig = plt.figure(figsize=(8, 8))
  #m = Basemap(projection='lcc', resolution='l',
  #            width=10E6, height=4E6,
  #            lat_0=58, lon_0=-65,
  #)
  m = Basemap(projection='gnom', resolution='l',
              width=13E6, height=5E6,
              lat_0=55, lon_0=-65,
              #epsg=4269,
  )
#  service = 'World_Physical_Map'
#  epsg = 4269
#  xpixels = 5000
#  m = Basemap(projection='mill',llcrnrlon=-123. ,llcrnrlat=37,
#      urcrnrlon=-121 ,urcrnrlat=39, resolution = 'l', epsg = epsg)
  
  # xpixels controls the pixels in x direction, and if you leave ypixels
  # None, it will choose ypixels based on the aspect ratio
  #m.arcgisimage(service=service, xpixels = xpixels, verbose= False)
  #m.warpimage(args.gebco2021_path)


#  m = Basemap(llcrnrlon=-118.5,llcrnrlat=33.15,urcrnrlon=-117.15,urcrnrlat=34.5, epsg=4269)
#
#
#  m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 2000, verbose= True)
  m.etopo()#scale=0.5, alpha=0.5)

#  #m.drawcoastlines()
  lats = range(0, 90, 10)
  lons = range(-170, 170, 10)
  # labels [left, right, top, bottom]
  m.drawparallels(lats, labels=[1,0,1,0])
  m.drawmeridians(lons, labels=[0,1,0,1])

  # draw a great circle for reference
  m.drawgreatcircle(-122.251250, 37.513420, -3.234017, 50.860516,linewidth=2,color='b')

  # draw tracks
  flights = load_flights(args.logfiles)
  col = 'r'
  for flight in flights:
    lat = flight['lat']
    lon = flight['lon']

    #m.plot(lon, lat, latlon=True)
    m.plot(lon, lat, color=col, latlon=True)

    if col == 'r':
      col = 'orange'
    else:
      col = 'r'

  # draw airfields
  for flight in flights:
    lat = flight['lat']
    lon = flight['lon']

    # plot airfield
    m.scatter(lon[-1], lat[-1], c='k', s=50, latlon=True)

  plt.show()

def main(args):
  plot_map(args)

if __name__=='__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--gebco2021_path', required=True)
  parser.add_argument('logfiles', nargs='*')
  args = parser.parse_args()
  main(args)
