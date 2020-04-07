from LinkInfo import LinkInfo
import csv

# This class extracts all the Link data.
class MapInfo(object):
    def __init__(self, fname):
        self.file = fname
        self.links = {}

    def extractAll_Links(self):
        with open(self.file, 'r') as rd:
            read_info = csv.reader(rd)
            for info in read_info:
                linkPVID = int(info[0])
                refNodeID = int(info[1])
                nrefNodeID = int(info[2])
                length = float(info[3])
                directionOfTravel = info[5]
                shapeInfo = info[14]
                slopeInfo = info[16]
                self.links[linkPVID] = LinkInfo(linkPVID, refNodeID, nrefNodeID, length, directionOfTravel, shapeInfo, slopeInfo)
        return self.links