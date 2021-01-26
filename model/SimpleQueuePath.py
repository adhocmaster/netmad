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
        """ It assumes infinite arrival and delivery rate. This method is called every time step for every sender seperately."""
        if self.debug:
            logging.info(f"SimpleQueuePath: {len(packets)} incoming packets from sender {packets[0].sender.id}")
        for packet in packets:
            self.deliverOrEnqueuePacket(packet)
        pass
    
    def deliverOrEnqueuePacket(self, packet):
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
        self.tryDeliveringFromQueue(timeStep) # assumes infinite delivery rate.

    def onTimeStepEnd(self, timeStep):
        """To be called at the end of a timeStep

        Args:
            timeStep ([type]): [description]
        """
        pass

    def tryDeliveringFromQueue(self, timeStep, limit=None):
        numDelivered = 0
        if self.isPipeFull() is False:
            sizeQBeforeFlushing = self.getQueueSize()
            while self.queue.empty() is False:
                packet = self.getFromQueue()
                self.updateTTL(packet)
                # adjust for waiting time
                packet.ackAt = timeStep + packet.ttl
                packet.ttl = packet.ackAt - packet.sentAt 
                self.addToPipe(packet)
                numDelivered += 1
                if self.isPipeFull() is True:
                    break
                if limit is not None:
                    if numDelivered >= limit:
                        break

            if self.debug and numDelivered > 0:
                logging.info(f"SimpleQueuePath: #{numDelivered} of {sizeQBeforeFlushing} packets were flushed to pipe from the queue")

        return numDelivered



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
