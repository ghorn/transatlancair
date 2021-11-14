import numpy as np
import pandas

def load_flight(path):
  # open the CSV and load the dataframe
  with open(path, 'r') as f:
    df = pandas.read_csv(path, skiprows=15, encoding='iso-8859-1', warn_bad_lines=False, error_bad_lines=False)

  lats = df['GPS-LAT'].to_numpy()
  lons = df['GPS-LONG'].to_numpy()
  alts = df['GPS-ALT;F'].to_numpy()

  ret_lats = []
  ret_lons = []
  ret_alts = []

  for k in range(len(lats)):
    lat = lats[k]
    lon = lons[k]
    alt = alts[k]

    if '-' in lat or '-' in lon:
      continue

    # parse lat
    lat = lat.split(' ')
    if len(lat) != 3:
      continue

    if lat[0] not in ['N', 'S']:
      continue

    ret_lat = float(lat[1]) + float(lat[2])/6000.
    if lat[0] == 'S':
      ret_lat = -ret_lat

    # parse lon
    lon = lon.split(' ')
    if len(lon) != 3:
      continue

    if lon[0] not in ['E', 'W']:
      continue

    ret_lon = float(lon[1]) + float(lon[2])/6000.
    if lon[0] == 'W':
      ret_lon = -ret_lon

    # drop some bad GPS data
    if path == 'data/N77ZG_flight_logs/Flt1164_10-08-21f.csv':
      if ret_lat < 40 and ret_lon > -100:
        continue

    ret_lats.append(ret_lat)
    ret_lons.append(ret_lon)
    ret_alts.append(alt)

  return {
    'name': path,
    'lat': np.array(ret_lats),
    'lon': np.array(ret_lons),
    'alt': np.array(ret_alts),
  }

def path_distance(lat, lon):
  v0 = ll2ecef(lat[0], lon[0])
  v1 = ll2ecef(lat[-1], lon[-1])
  dv = v1 - v0
  return np.sqrt(np.sum(dv*dv))

def ll2ecef(lat, lon):
  wgs84_A = 6378137.0
  wgs84_F = 1. / 298.257223563
  wgs84_E = np.sqrt (2 * wgs84_F - wgs84_F * wgs84_F)
  pi = np.pi
  lat = pi / 180. * lat
  lon = pi / 180. * lon
  height = 0.

  d = wgs84_E * np.sin(lat)
  n = wgs84_A / np.sqrt(1 - d * d)

  ecef0 = (n + height) * np.cos(lat) * np.cos(lon)
  ecef1 = (n + height) * np.cos(lat) * np.sin(lon)
  ecef2 = ((1 - wgs84_E * wgs84_E) * n + height) * np.sin(lat)

  return np.array([ecef0, ecef1, ecef2])


def load_flights(logfiles):
  flights = []
  for path in logfiles:
    # only logs that end with 'f' are flights - discard the rest
    if not path.endswith('f.csv'):
      continue

    # load the flight
    flight = load_flight(path)

    # discard empty ones
    if flight['lat'].size == 0:
      continue

    # discard short ones (taxiing and the short england flights)
    dist_km = 1e-3*path_distance(flight['lat'], flight['lon'])
    if dist_km < 400:
      continue

    # print the result
    print(f'{path}: {dist_km:6.1f} km')

    flights.append(flight)

  return flights
