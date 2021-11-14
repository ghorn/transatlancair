#!/usr/bin/env python3

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import argparse

from transatlancair.load_flights import load_flights

STOPS = {
  'KLAX':None,
  'KSQL':(37.5151, -122.2504),
  'KGTF':(47.4825, 111.3566),
}

def plotmap(flights):
  fig = plt.figure(figsize=(8, 8))
  #m = Basemap(projection='lcc', resolution='l',
  #            width=10E6, height=4E6,
  #            lat_0=58, lon_0=-65,
  #)
  m = Basemap(projection='gnom', resolution='l',
              width=13E6, height=5E6,
              lat_0=55, lon_0=-65,
  )



  m.etopo()#scale=0.5, alpha=0.5)

  #m.drawcoastlines()
  lats = range(0, 90, 10)
  lons = range(-170, 170, 10)
  # labels [left, right, top, bottom]
  m.drawparallels(lats, labels=[1,0,1,0])
  m.drawmeridians(lons, labels=[0,1,0,1])

  # draw a great circle for reference
  #m.drawgreatcircle(-122.251250, 37.513420, -3.234017, 50.860516,linewidth=2,color='b')

  # draw tracks
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
  flights = load_flights(args.logfiles)
  plotmap(flights)

if __name__=='__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('logfiles', nargs='*')
  args = parser.parse_args()
  main(args)
