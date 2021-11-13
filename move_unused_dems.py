#!/usr/bin/env python3

from os import listdir
from os.path import isfile, join
import shutil

def main():
  mypath = 'data/dem/COP90_hh'
  good = 0
  bad = 0
  for f in listdir(mypath):
    example = 'Copernicus_DSM_COG_30_N55_00_W162_00_DEM.tif'
    if example.endswith('DEM.tif') and len(f) == len(example):
      lat = f[22:25]
      lat = int(lat[1:]) if lat[0] == 'N' else -int(lat[1:])
      lon = f[29:33]
      lon = int(lon[1:]) if lon[0] == 'E' else -int(lon[1:])

      isgood = lon >= -135 and lon <=39 and lat >= 24 and lat <= 72
      #print(f'lat {lat:3d}, lon {lon:4d}, good {isgood}')
      if isgood:
        good += 1
      else:
        bad += 1
        shutil.move(f'{mypath}/{f}', f'{mypath}/../unused/{f}')
  print(f'num good: {good}')
  print(f'num bad: {bad}')
  

if __name__=='__main__':
  main()
