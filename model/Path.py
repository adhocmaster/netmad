from abc import ABC, abstractmethod
from model.PathType import PathType


class Path(ABC):

    def __init__(self, pathType: PathType=PathType.SimpleQueue, avgTTL=20, noiseMax=20, debug=True):
        self.pathType = pathType
        self.pipe = None
        self.queue = None
        self.noiseMax = noiseMax # ms
        self.avgTTL = avgTTL # ms
        self.debug = debug

    
    @abstractmethod
    def onIncomingPackets(self, packets):
        pass

    @abstractmethod
    def getACKs(self):
        pass
    

    @abstractmethod
    def onTimeStep(self, timeStep):
        pass

    @abstractmethod
    def getPacketsByTimeStep(self, timeStep):
        pass

    @abstractmethod
    def getQSize(self):
        pass

    @abstractmethod
    def getNumPacketInflight(self):
        pass