from math import sin, cos, sqrt, atan2, radians

R = 6373.0  # Earth constant


class GeospatialUtils():
    """ Class that implements some distance calculus methods """

    def calculate_distance(self, point1: dict, point2: dict) -> float:
        """ Calculate distance between two points (in Km)

        :param point1: **first (latitude, longitude) point**.
            dict with lat and lng keys

        :param point2: **second (latitude, longitude) point**.
            dict with lat and lng keys

        :return: distance in kilometers
        """

        lat1 = radians(point1['lat'])
        lon1 = radians(point1['lng'])
        lat2 = radians(point2['lat'])
        lon2 = radians(point2['lng'])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = (sin(dlat/2)) ** 2 + cos(lat1) * cos(lat2) * (sin(dlon/2)) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c

        return distance
