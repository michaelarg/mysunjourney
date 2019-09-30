
from math import radians, degrees, cos, sin, asin, atan2, atan

def points_from_bearing(lat,lon,bearing, distance, coord):
    radius = 6378.1
    bearing = radians(bearing)
    distance = distance
    lat1 = radians(lat)
    lon1 = radians(lon)

    lat2 = asin( sin(lat1)*cos(distance/radius) +
    cos(lat1)*sin(distance/radius)*cos(bearing))

    lon2 = lon1 + atan2(sin(bearing)*sin(distance/radius)*cos(lat1), cos(distance/radius)-sin(lat1)*sin(lat2))


    lat2 = degrees(lat2)
    lon2 = degrees(lon2)

    if coord == "lat":
        return(lat2)
    else:
        return(lon2)

def bearing_between_two_points(lat1,lon1,lat2,lon2):
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    
    delta_lon = lon2 - lon1
    delta_lat = lat2 - lat1

    y= sin(delta_lon) * cos(lat2)
    x = cos(lat1) * sin(lat2) - (sin(lat1) * cos(lat2) * cos(delta_lon))

    bearing = atan2(y,x)
    bearing = (degrees(bearing) + 360) % 360

    return bearing

if __name__ == "__main__":
    print(bearing_between_two_points(-33.81730 , 151.00523,-33.81739  , 151.00541))
    print(points_from_bearing(-33.81730 , 151.00523,90,1))