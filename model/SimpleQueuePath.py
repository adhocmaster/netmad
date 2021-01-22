from model.Path import Path
from model.PathType import PathType

class SimpleQueuePath(Path):

    def __init__(self):
        super().__init__(PathType.SimpleQueue)
        
        
    
    def onIncomingPackets(self, packets):
        pass

    def getACKs(self):
        return []