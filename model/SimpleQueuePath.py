from model.Path import Path
from model.PathType import PathType
import queue, math, logging
import numpy as np

class SimpleQueuePath(Path):

    def __init__(
                    self, 
                    maxDataInPipe=10000,
                    maxQsize = 10000, 
                    avgTTL=20, noiseMax=20,
                    debug=True
                ):
        super().__init__(PathType.SimpleQueue, maxDataInPipe=maxDataInPipe, avgTTL=avgTTL, noiseMax=noiseMax, debug=debug)
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
    
    def onTimeStepStart(self, timeStep):
        self.ackPackets = self.getPacketsByTimeStep(timeStep)
        self.tryFlushQueue(timeStep)

    def onTimeStepEnd(self, timeStep):
        """To be called at the end of a timeStep

        Args:
            timeStep ([type]): [description]
        """
        pass

    def tryFlushQueue(self, timeStep):
        if self.isPipeFull() is False:
            counter = 0
            sizeQBeforeFlushing = self.getQueueSize()
            while self.queue.empty() is False:
                counter += 1
                packet = self.getFromQueue()
                self.updateTTL(packet)
                # adjust for waiting time
                packet.ackAt = timeStep + packet.ttl
                packet.ttl = packet.ackAt - packet.sentAt 
                self.addToPipe(packet)
                if self.isPipeFull() is True:
                    break
            if self.debug and counter > 0:
                logging.info(f"SimpleQueuePath: #{counter} of {sizeQBeforeFlushing} packets were flushed to pipe from the queue")



    def getACKs(self):
        return self.ackPackets

    
    def getNumPacketInflight(self):
        return self.getNumPacketInPipe() + self.getQueueSize()
        

    def updateTTL(self, packet):
        packet.ttlNoise = np.random.randint(0, self.noiseMax)
        packet.ttl = math.floor( self.avgTTL + self.avgTTL * (self.getQueueSize() / self.maxQsize) + packet.ttlNoise )
        packet.ackAt = packet.sentAt + packet.ttl
        pass


    def getDataInFlightInKB(self):
        return self.getDataInPipeInKB() + self.getDataInQueueInKB()
    
    
    def getDataInQueueInKB(self):
        s = 0
        for packet in self.queue.queue: # accessing underlying deque, so, items are not consumed
            s += packet.size / 1000
        return round(s, 2)


    
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

    
    def getQueueSize(self):
        """[summary]

        Returns:
            [type]: approximate queue size
        """
        return self.queue.qsize()

    
    def isOverflowed(self):
        return self.getQueueSize() >= self.maxQsize
