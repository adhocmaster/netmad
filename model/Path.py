from abc import ABC, abstractmethod
from model.PathType import PathType


class Path(ABC):

    def __init__(self, pathType: PathType=PathType.SimpleQueue):
        self.pathType = pathType
        self.pipe = [] # max size of the pipe?
        self.queue = []

    
    @abstractmethod
    def onIncomingPackets(self, packets):
        pass

    @abstractmethod
    def getACKs(self):
        pass

