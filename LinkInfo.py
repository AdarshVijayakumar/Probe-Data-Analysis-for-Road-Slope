from math import sin, cos, atan2, sqrt, degrees, radians, pi, asin
from geopy.distance import great_circle as distance
from geopy.point import Point
import csv
# This class collects extra information on shape and slope.
class LinkInfo(object):
    def __init__(self, linkPVID, refNodeID, nrefNodeID, length, directionOfTravel, shapeInfo, slopeInfo):
        self.linkPVID = linkPVID
        self.refNodeID = refNodeID
        self.nrefNodeID = nrefNodeID
        self.length = length
        self.directionOfTravel = directionOfTravel
        self.shapeInfo = shapeInfo
        self.slopeInfo = slopeInfo
        self.keep = []
        self.slope = []
        self.collect_shapeInfo()
        self.collect_slopeInfo()
        self.link = ''

    def collect_shapeInfo(self):
        for content in self.shapeInfo.split('|'):
            info = [0, 0]
            info[0], info[1], elevation = content.split('/')
            self.keep.append(info)
        self.ref_lat = float(self.keep[0][0])
        self.ref_lon = float(self.keep[0][1])
        l = len(self.keep)
        self.nonref_lat = float(self.keep[l - 1][0])
        self.nonref_lon = float(self.keep[l - 1][1])

    def collect_slopeInfo(self):
        if not self.slopeInfo:
            self.slopeInfo = None
            return
        for content in self.slopeInfo.split('|'):
            info = [0, 0]
            info[0], info[1] = content.split('/')
            self.slope.append(info)

    # this function defines haversine formula to calculate distance
    def haversine(self, probe):
        x_latitude = probe.latitude
        x_longitude = probe.longitude
        y_latitude = self.ref_lat
        y_longitude = self.ref_lon
        x_longitude, x_latitude, y_longitude, y_latitude = map(radians, [x_longitude, x_latitude, y_longitude, y_latitude])
        lon = y_longitude - x_longitude
        lat = y_latitude - x_latitude
        a = sin(lat / 2)**2 + cos(x_latitude) * cos(y_latitude) * sin(lon / 2)**2
        c = 2 * asin(sqrt(a))
        r = 6371 * 1000
        return c * r

    # this function defines mid point formula to calculate distance for ends.
    def middlePointLength_forEnds(self, probe, end1, end2):
        p = Point(probe.latitude, probe.longitude)
        latitude_x = radians(float(end1[0]))
        longitude_x = radians(float(end1[1]))
        latitude_y = radians(float(end2[0]))
        longitude_y = radians(float(end2[1]))
        x = cos(latitude_y) * cos(longitude_y - longitude_x)
        y = cos(latitude_y) * sin(longitude_y - longitude_x)
        lat = atan2(
            sin(latitude_x) + sin(latitude_y),
            sqrt(((cos(latitude_x) + x)**2 + y**2)))
        lon = longitude_x + atan2(y, cos(latitude_x) + x)
        lon = (lon + 3 * pi) % (2 * pi) - pi
        middle = Point(latitude=degrees(lat), longitude=degrees(lon))
        return distance(middle, p).km * 1000

    # this function defines mid point formula to calculate distance
    def middlePoint_length(self, probe):
        p = Point(probe.latitude, probe.longitude)
        X_lat = radians(self.ref_lat)
        X_lon = radians(self.ref_lon)
        Y_lat = radians(self.nonref_lat)
        Y_lon = radians(self.nonref_lon)
        x = cos(Y_lat) * cos(Y_lon - X_lon)
        y = cos(Y_lat) * sin(Y_lon - X_lon)
        lat = atan2(
            sin(X_lat) + sin(Y_lat),
            sqrt(((cos(X_lat) + x)**2 + y**2)))
        lon = X_lon + atan2(y, cos(X_lat) + x)
        lon = (lon + 3 * pi) % (2 * pi) - pi
        middle = Point(latitude=degrees(lat), longitude=degrees(lon))
        return distance(middle, p).km * 1000

    #this function is used to display matched points
    def __str__(self):
        return 'PVID ' + str(self.linkPVID) + ' Ref ID :' + str(self.refNodeID) + ' lat :' + str(self.ref_lat) + ' long :' + str(self.ref_lon) \
               + ' NRef ID :' + str(self.nrefNodeID) + ' lat :' + \
               str(self.nonref_lat) + ' long :' + str(self.nonref_lon)
