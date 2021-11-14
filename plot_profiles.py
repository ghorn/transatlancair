#!/usr/bin/env python3

import matplotlib.pyplot as plt
import argparse
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

from transatlancair.load_flights import load_flights

def main(args):
  flights = load_flights(args.logfiles)
  plot_profiles(flights)

  plot_3d_flights(flights)

  # plot the nasty takeoff
  for flight in flights:
    if flight['name'].endswith('Flt1184_10-20-21f.csv'):
      plot_3d_flight(flight)
      break

  plt.show()

def set_axes_equal(ax):
    '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().
    '''

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

def plot_3d_flight(flight):
  n = flight['ned_position'].shape[1]
  n = int(n/6)

  #fig = plt.figure()
  #ax = fig.add_subplot(111, projection='3d')
  #ax.plot(1e-3*flight['ned_position'][1,:n],
  #        1e-3*flight['ned_position'][0,:n],
  #        -1e-3*flight['ned_position'][2,:n])
  #set_axes_equal(ax)
  #ax.set_xlabel('east [km]')
  #ax.set_ylabel('north [km]')
  #ax.set_zlabel('down [km]')

  fig = plt.figure()
  ax1 = fig.add_subplot(1, 2, 1)
  ax2 = fig.add_subplot(1, 2, 2, aspect='equal')
  
  ax1.plot(flight['dist_nm'][:n], 1e-3*flight['alt_ft'][:n])
  ax1.set_xlabel('distance [nm]')
  ax1.set_ylabel('altitude [ft * 1000]')
  ax1.set_title('flight profile')

  ax2.plot(1e-3*flight['ned_position'][1,:n],
           1e-3*flight['ned_position'][0,:n])

  ax2.set_xlabel('position east [km]')
  ax2.set_ylabel('position north [km]')
  ax2.set_title('top view')
  

def plot_3d_flights(flights):
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  for flight in flights:
    ax.plot(flight['ecef_position'][0,:],
            flight['ecef_position'][1,:],
            flight['ecef_position'][2,:])
  ax.set_xlabel('ecef X')
  ax.set_ylabel('ecef Y')
  ax.set_zlabel('ecef Z')
  set_axes_equal(ax)
  plt.title("flights in ECEF")

def plot_profiles(flights):
  plt.figure()
  for flight in flights:
    plt.plot(flight['dist_nm'], 1e-3*flight['alt_ft'])
    #plt.plot(flight['dt'])
  plt.xlabel('distance [nm]')
  plt.ylabel('altitude [ft * 1000]')
  plt.title('all flight profiles')

if __name__=='__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('logfiles', nargs='*')
  args = parser.parse_args()
  main(args)
