import math

MIN_LAT = -math.pi / 2
MAX_LAT = math.pi / 2
MIN_LON = -math.pi * 2
MAX_LON = math.pi * 2

EARTH_MEAN_RADIUS_MI = 3958.761
EARTH_MEAN_RADIUS_KM = 6371.009

def get_bounding_box(lat, lon, distance, radians=True):
    """
    Returns coordinates in degrees of bounding box (latmin, latmax, lonmin, lonmax)
    for given point(lat, lon) in degrees, distance in miles.
    """
    earth_radius = EARTH_MEAN_RADIUS_MI
    if distance < 0:
        raise AttributeError()

    # angular distance in radians on a great circle
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)

    rad_dist = distance / earth_radius
    min_lat = lat_rad - rad_dist
    max_lat = lat_rad + rad_dist

    if min_lat > MIN_LAT and max_lat < MAX_LAT:
        delta_lon = math.asin(math.sin(rad_dist) / math.cos(lat_rad))
        min_lon = lon_rad - delta_lon
        if min_lon < MIN_LON:
            min_lon = min_lon + 2 * math.pi
        max_lon = lon_rad + delta_lon
        if max_lon > MAX_LON:
            max_lon = max_lon - 2 * math.pi
    else:
        # a pole is within the distance
        min_lat = max((min_lat, MIN_LAT))
        max_lat = min((max_lat, MAX_LAT))
        min_lon = MIN_LON
        max_lon = MAX_LON
    if radians is False:
        return map(math.degrees, (min_lat, max_lat, min_lon, max_lon))
    else:
        return (min_lat, max_lat, min_lon, max_lon)


def get_distance(origin_lat, origin_lon, dest_lat, dest_lon, units='mi'):
    """
    Calculates the distance between two geo points using Heavisine formula.
    Result is in miles by default.
    """
    radius = EARTH_MEAN_RADIUS_MI
    mi_per_km = 0.62317

    dlat = math.radians(dest_lat - origin_lat)
    dlon = math.radians(dest_lon - origin_lon)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(origin_lat)) \
        * math.cos(math.radians(dest_lat)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    # convert result from mi to km if required
    if units == 'km':
        d = d / mi_per_km
    return d
