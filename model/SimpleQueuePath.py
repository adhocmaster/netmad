from model.Path import Path
from model.PathType import PathType
import queue, math, logging
import numpy as np

class SimpleQueuePath(Path):

    def __init__(
                    self, 
                    maxQsize = 1000000, 
                    avgTTL=20, noiseMax=20,
                    debug = True
                ):
        super().__init__(PathType.SimpleQueue, avgTTL=avgTTL, noiseMax=noiseMax, debug=debug)
        self.maxQsize = maxQsize
        self.queue = queue.Queue(maxsize=maxQsize)
        self.pipe = {} # holds received packets with ttl
        self.timeStep = 0
        self.ackPackets = []
        
    
    def onIncomingPackets(self, packets):
        if self.debug:
            logging.debug(f"SimpleQueuePath: {len(packets)} incoming packets")
        for packet in packets:
            self.updateTTL(packet)
            self.addToPipe(packet)
        pass
    
    def onTimeStep(self, timeStep):
        self.ackPackets = self.getPacketsByTimeStep(timeStep)


    def getACKs(self):
        return self.ackPackets

    
    def getNumPacketInflight(self):
        s = 0
        for packets in self.pipe.values():
            s += len(packets)
        return s
        

    def getPacketsByTimeStep(self, timeStep):
        existingPackets = self.pipe.get(timeStep, [])
        self.pipe[timeStep] = [] # removing the packets

        if self.debug and len(existingPackets) > 0:
            logging.debug(f"SimpleQueuePath: receiving {len(existingPackets)} packets at {timeStep}")

        return existingPackets
        

    def updateTTL(self, packet):
        packet.ttlNoise = np.random.randint(0, self.noiseMax)
        packet.ttl = math.floor( self.avgTTL + self.avgTTL * (self.getQSize() / self.maxQsize) + packet.ttlNoise )
        packet.ackAt = packet.sentAt + packet.ttl
        pass

    
    def addToPipe(self, packet):
        existingPackets = self.pipe.get(packet.ackAt, [])
        existingPackets.append(packet)
        self.pipe[packet.ackAt] = existingPackets
        pass

    
    def addToQueue(self, packet):

        try:
            self.queue.put(packet, block=False)
        except queue.Full:
            # packet dropped
            pass
    
    def getFromQueue(self):
        try:
            return self.queue.get(block=False)
        except queue.Empty:
            pass # queue is empty

    
    def getQSize(self):
        """[summary]

        Returns:
            [type]: approximate queue size
        """
        return self.queue.qsize()

    
    def getPipeStats(self):
        stats = {}
        for timeStep in self.pipe:
            if len(self.pipe[timeStep]) > 0:
                stats[timeStep] = len(self.pipe[timeStep])
        return stats