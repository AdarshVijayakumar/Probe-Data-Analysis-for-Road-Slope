from math import sin, cos, sqrt, degrees, radians, asin
from ProbeInfo import ProbeInfo
from MapInfo import MapInfo
import csv


# This class defines methods to match probe points with link data.
class ProbMatching(object):

    # In this method Link data is extracted
    def start(self):
        self.connections = MapInfo('Partition6467LinkData.csv').extractAll_Links()
        self.probe_document = 'Partition6467ProbePoints.csv'
        self.probe_info = []
        self.obtain_probeInfo()

    # this method performs map matching.
    def obtain_probeInfo(self):
        print ("Map Matching Started.... Wait for the result! \n")

        # start reading probe data file
        with open(self.probe_document, 'r') as probe:
            k = 0
            read_info = csv.reader(probe)
            matched_probePoints = open("Partition6467MatchedPoints.csv", 'a+')

            content = 'sampleID,  dateTime, sourceCode, latitude, longitude, altitude, speed, heading, linkPVID, direction, distFromRef, distFromLink'
            print(content+"\n")
            matched_probePoints.write(content + "\n")
            for content in read_info:
                probeInfo = ProbeInfo(int(content[0]), str(content[1]), int(content[2]), float(content[3]), float(content[4]), float(content[5]), float(content[6]), float(content[7]))

                # appending probe points which are similar and resetting
                if k == 0:
                    self.probe_info.append(probeInfo)
                    k = k + 1
                elif self.probe_info[k - 1].sampleID == probeInfo.sampleID:
                    self.probe_info.append(probeInfo)
                    k = k + 1
                else:
                    self.probe_info = []
                    self.probe_info.append(probeInfo)
                    k = 1

                closest_res = self.fetchClosest_connection(probeInfo)

                linkPVID = closest_res[0].linkPVID
                distFromLink = closest_res[1]
                distFromRef = closest_res[2]

                # calculating the slope .
                slope = self.slope(closest_res[0], probeInfo)
                direction = closest_res[0].directionOfTravel

                if direction == 'B':
                    direction = 'X'
                # mMatched points are written to csv file
                content = "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (
                    probeInfo.sampleID, probeInfo.dateTime, probeInfo.sourceCode, probeInfo.latitude, probeInfo.longitude, probeInfo.altitude, probeInfo.speed, probeInfo.heading, linkPVID, direction, distFromRef, distFromLink)
                matched_probePoints.write(content + "\n")

                # displaying the result on console
                print (str(probeInfo) + ' Link ID ' + str(linkPVID) + ',' + str(direction) + ',' + \
                    str(distFromRef) + ',' + str(distFromLink) + \
                    ',' + '\n' + slope + '\n')

            matched_probePoints.close()

    # In this function closest matching points are fetched.
    def fetchClosest_connection(self, pdata):
        min_connection = self.connections.keys()[0]
        min_length = self.connections[min_connection].middlePoint_length(pdata)
        for link in self.connections:
            p_len = self.connections[link].middlePoint_length(pdata)
            if min_length > p_len:
                min_connection = link
                min_length = p_len
        hs= self.connections[min_connection].haversine(pdata)
        return [self.connections[min_connection], min_length, hs]

    # using mid point formula slope is calculated
    def slope(self, link, pdata):
        temp = open("Partition6467SlopeValues.csv", 'a+')
        if len(self.probe_info) == 1:
            return 'X'

        k = len(self.probe_info) - 2

        alt = pdata.altitude - self.probe_info[k].altitude
        dist = self.haversine(pdata, self.probe_info[k])
        slope = alt / dist

        # avoid lower value of slope to find slope in radian
        if slope > 1 or slope < -1:
            return 'Distance is small: ' + str(dist) + 'm'


        derivedslope = degrees(asin(slope))

        if link.slopeInfo is None:
            linkPVID = link.linkPVID
            content = "%s, %s, %s" % (
                linkPVID, derivedslope, ' Surveyed slope : N/A ')
            temp.write(content + "\n")
            temp.close()
            return 'Derived slope : ' + str(derivedslope) + ' Surveyed slope : N/A '
        linki = 0
        min_length = link.middlePointLength_forEnds(pdata, link.keep[0], link.keep[1])
        for k in range(1, len(link.slope)):
            slope_len = link.middlePointLength_forEnds(
                pdata, link.keep[k - 1], link.keep[k])
            if slope_len < min_length:
                linki = k
                min_length = slope_len
        error = float(link.slope[linki][1]) - derivedslope
        linkPVID = link.linkPVID
        content = "%s, %s, %s" % (linkPVID, derivedslope, link.slope[linki][1])
        temp.write(content + "\n")
        temp.close()
        return 'Derived slope : ' + str(derivedslope) + ' Surveyed slope : ' + str(link.slope[linki][1]) +\
            ' error : ' + str(abs(error))

    # haversine formula is used to calculate distance.
    def haversine(self, pEnd1, pEnd2):

        pEnd1.longitude, pEnd1.latitude, pEnd2.longitude, pEnd2.latitude = map(
            radians, [pEnd1.longitude, pEnd1.latitude, pEnd2.longitude, pEnd2.latitude])

        long1 = pEnd2.longitude - pEnd1.longitude
        lat1 = pEnd2.latitude - pEnd1.latitude
        a = sin(lat1 / 2) ** 2 + cos(pEnd1.latitude) * \
            cos(pEnd2.latitude) * sin(long1 / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371 * 1000
        return c * r

if __name__ == '__main__':
    ProbMatching().start()
