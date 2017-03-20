import cmath,math
class Coord(object):
    
    @classmethod
    def getDistanceFromLatLonInKm(cls,lat1, lon1, lat2, lon2):
        R = 6371
        dLat = cls.deg2rad(lat2 - lat1)
        dLon = cls.deg2rad(lon2 - lon1)
        a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(cls.deg2rad(lat1)) * math.cos(cls.deg2rad(lat2)) * math.sin(dLon / 2) * math.sin(dLon / 2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a));
        d = R * c;
        return d

    @classmethod
    def deg2rad(cls,deg):
        return deg * (math.pi / 180)