from model.Path import Path
from model.PathType import PathType
import queue, math, logging
import numpy as np

class SimpleQueuePath(Path):

    def __init__(
                    self, 
                    maxDataInflight=10000,
                    maxQsize = 10000, 
                    avgTTL=20, noiseMax=20,
                    debug=True
                ):
        super().__init__(PathType.SimpleQueue, maxDataInflight=maxDataInflight, avgTTL=avgTTL, noiseMax=noiseMax, debug=debug)
        self.maxQsize = maxQsize
        self.queue = queue.Queue(maxsize=maxQsize)
        self.timeStep = 0
        self.ackPackets = []
        
    
    def onIncomingPackets(self, packets):
        if self.debug:
            logging.info(f"SimpleQueuePath: {len(packets)} incoming packets")
        for packet in packets:

            if self.isPipeFull():
                # add to queue if pipe is full
                self.addToQueue(packet)
            else:
                # else, update ttl and add to pipe
                self.updateTTL(packet)
                self.addToPipe(packet)
        pass
    
    def onTimeStep(self, timeStep):
        self.ackPackets = self.getPacketsByTimeStep(timeStep)

        # TODO get some from queue

        self.tryFlushQueue(timeStep)


    def tryFlushQueue(self, timeStep):
        if self.isPipeFull() is False:
            while self.queue.empty() is False:
                packet = self.getFromQueue()
                self.updateTTL(packet)
                # adjust for waiting time
                packet.ackAt = timeStep + packet.ttl
                packet.ttl = packet.ackAt - packet.sentAt 
                self.addToPipe(packet)
                if self.isPipeFull() is True:
                    break



    def getACKs(self):
        return self.ackPackets

    
    def getNumPacketInflight(self):
        s = 0
        for packets in self.pipe.values():
            s += len(packets)
        return s

        

    def updateTTL(self, packet):
        packet.ttlNoise = np.random.randint(0, self.noiseMax)
        packet.ttl = math.floor( self.avgTTL + self.avgTTL * (self.getQSize() / self.maxQsize) + packet.ttlNoise )
        packet.ackAt = packet.sentAt + packet.ttl
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
            return None

    
    def getQSize(self):
        """[summary]

        Returns:
            [type]: approximate queue size
        """
        return self.queue.qsize()

    
    def isOverflowed(self):
        return self.getQSize() >= self.maxQsize