import numpy as np
import pandas

def load_flight(path):
  # open the CSV and load the dataframe
  with open(path, 'r') as f:
    df = pandas.read_csv(path, skiprows=15, encoding='iso-8859-1', warn_bad_lines=False, error_bad_lines=False)

  lats = df['GPS-LAT'].to_numpy()
  lons = df['GPS-LONG'].to_numpy()
  alts = df['GPS-ALT;F'].to_numpy()
  gps_speeds = df['GPS-SPEED;KTS'].to_numpy()

  ret_lats = []
  ret_lons = []
  ret_alts = []
  ret_dist = []
  ret_gps_speed = []
  ret_dts = []

  # time since last sample
  dt = 0.
  for k in range(len(lats)):
    dt += 1.

    lat = lats[k]
    lon = lons[k]
    alt_ft = alts[k]
    gps_speed_kts = gps_speeds[k]

    if '-' in lat or '-' in lon:
      continue

    if isinstance(gps_speed_kts, str) and '-' in gps_speed_kts:
      continue

    if isinstance(alt_ft, str) and '-' in alt_ft:
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

    # altitude
    alt_ft = float(alt_ft)

    # convert gps speed from string
    gps_speed_kts = float(gps_speed_kts)

    # compute distances
    old_dist = 0. if len(ret_dist)==0 else ret_dist[-1]
    dist = old_dist + gps_speed_kts*dt/60./60.
    #dist = 0 if len(ret_dist) == 0 else ret_dist[-1]

    ret_lats.append(ret_lat)
    ret_lons.append(ret_lon)
    ret_alts.append(alt_ft)
    ret_dist.append(dist)
    ret_gps_speed.append(gps_speed_kts)
    ret_dts.append(dt)

    # zero delta time for next time
    dt = 0.


  ret = {
    'name': path,
    'lat': np.array(ret_lats),
    'lon': np.array(ret_lons),
    'alt_ft': np.array(ret_alts),
    'dist_nm': np.array(ret_dist),
    'gps_speed_kts': np.array(ret_gps_speed),
    'dt': np.array(ret_dts),
  }

  ret['alt_m'] = ret['alt_ft'] * 0.3048
  ret['ecef_position'] = llh2ecef(ret['lat'], ret['lon'], height=ret['alt_m'])
  ret['ned_position'] = ecef2ned(ret['ecef_position'][:,0], ret['ecef_position'])
  return ret


def path_distance(lat, lon):
  v0 = llh2ecef(lat[0], lon[0])
  v1 = llh2ecef(lat[-1], lon[-1])
  dv = v1 - v0
  return np.sqrt(np.sum(dv*dv))

def llh2ecef(lat, lon, height=0):
  wgs84_A = 6378137.0
  wgs84_F = 1. / 298.257223563
  wgs84_E = np.sqrt (2 * wgs84_F - wgs84_F * wgs84_F)
  pi = np.pi
  lat = pi / 180. * lat
  lon = pi / 180. * lon

  d = wgs84_E * np.sin(lat)
  n = wgs84_A / np.sqrt(1 - d * d)

  ecef0 = (n + height) * np.cos(lat) * np.cos(lon)
  ecef1 = (n + height) * np.cos(lat) * np.sin(lon)
  ecef2 = ((1 - wgs84_E * wgs84_E) * n + height) * np.sin(lat)

  return np.array([ecef0, ecef1, ecef2])

def dcmEcef2Ned(ref_ecef):
  ref_ecef_0 = ref_ecef[0]
  ref_ecef_1 = ref_ecef[1]
  ref_ecef_2 = ref_ecef[2]

  hyp_az = np.sqrt(ref_ecef_0 * ref_ecef_0 + ref_ecef_1 * ref_ecef_1)
  hyp_el = np.sqrt(hyp_az * hyp_az + ref_ecef_2 * ref_ecef_2)
  sin_el = ref_ecef_2 / hyp_el
  cos_el = hyp_az / hyp_el
  sin_az = ref_ecef_1 / hyp_az
  cos_az = ref_ecef_0 / hyp_az

  return np.array([
    [-sin_el * cos_az, -sin_el * sin_az, cos_el],
    [-sin_az, cos_az, 0],
    [-cos_el * cos_az, -cos_el * sin_az, -sin_el],
  ])

def ecef2ned(ecef_ref, ecef):
  dcmE2N = dcmEcef2Ned(ecef_ref)
  delta_ecef = np.subtract(ecef.T, ecef_ref).T
  return np.dot(dcmE2N, delta_ecef)

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

    dist_nm = dist_km / 1.852

    # print the result
    print(f'{path}: {dist_km:6.1f} km | {dist_nm:6.1f} nm')

    flights.append(flight)

  return flights
