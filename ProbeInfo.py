import csv

# This class fetches all the probe points and a display function to print them.
class ProbeInfo(object):

    def __init__(self, sampleID, dateTime, sourceCode, latitude, longitude, altitude, speed, heading):
        self.sampleID = sampleID
        self.dateTime = dateTime
        self.sourceCode = sourceCode
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.speed = speed
        self.heading = heading

    def __str__(self):
        return str(self.sampleID) + ',' + str(self.dateTime) + ',' + str(self.sourceCode) + ',' \
            + str(self.latitude) + ',' + str(self.longitude) + ',' + str(self.altitude) + ',' \
            + str(self.speed) + ',' + str(self.heading)
