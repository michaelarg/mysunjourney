import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, get_sun
from datetime import date, datetime

def sun_position(lat,lon,time):
    t = Time(time)
    syd = EarthLocation(lat=lat, lon=lon, height=100)
    s=get_sun(t)
    sal = s.transform_to(AltAz(obstime = t , location = syd))
    sun_details = {'azimuth' : sal.az.value, 'elevation' : sal.alt.value}
    return sun_details['azimuth']

if __name__ == "__main__":
    print(Time(str(datetime.utcnow())))
    #2019-10-01T02:05:00Z
    print(sun_position(-34.44,151.22,'2019-10-01T02:05:02Z'))