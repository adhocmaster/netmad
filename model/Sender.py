from abc import ABC, abstractmethod
import time
import threading
from model.Packet import Packet
from model.SenderType import SenderType
from model.Path import Path
import math
import numpy as np
import logging

class Sender(ABC):

    def __init__(self, id, senderType: SenderType, deliveryRate = 0.1, debug=True):
        self.lock = threading.RLock()
        self.id = id
        self.nextPacketNumber = 1
        self.type = senderType
        self.deliveryRate = deliveryRate # per ms
        self.debug = debug
    
    def __str__(self):

        return (
        f" \n\tid: {self.id} \n"
        f"\ttype: {self.type} \n"
        f"\tdeliveryRate: {self.deliveryRate} \n"
        f"\tnextPacketNumber: {self.nextPacketNumber} \n"

        f"\tdebug: {self.debug} \n"
        )
        
    def getName(self):
        return self.type.name + " #" + str(self.id)


    def createPacketIdFromNumber(self, packetNumber):
        return str(self.id) + "-" + str(packetNumber)

    def getNewPacketId(self):

        with self.lock:
            packetNumber = self.nextPacketNumber
            self.nextPacketNumber += 1
        
        return self.createPacketIdFromNumber(packetNumber)


    def getNewPacketIds(self, numberOfPackets):

        ids = []
        with self.lock:
            nextPacketNumber = self.nextPacketNumber
            self.nextPacketNumber += numberOfPackets
        
        for _ in range(numberOfPackets):
            ids.append(self.createPacketIdFromNumber(nextPacketNumber))
            nextPacketNumber += 1
        
        return ids


    
    def createPacket(self, size, sentAt=0):
        
        packetId = self.getNewPacketId()
        return Packet(packetId, self, size=size, sentAt=0)
    
    def createPackets(self, numberOfPackets, sizeMin=20, sizeMax=40, sentAt=0):

        size = sizeMin
        if sizeMin < sizeMax:
            size = np.random.randint(sizeMin, sizeMax)
        
        ids = self.getNewPacketIds(numberOfPackets)
        packets = []
        for id in ids:
            packets.append(Packet(id, self, size=size, sentAt=sentAt))
        return packets


    def createPacketsForTimeStep(self, timeStep):
        
        numberOfPackets = math.floor(timeStep * self.deliveryRate)  - math.floor((timeStep - 1) * self.deliveryRate)
        return self.createPackets(numberOfPackets, sizeMin=20, sizeMax=20, sentAt=timeStep)


    def createAndSendPacketsForTimeStep(self, timeStep, path: Path):
        packets = self.createPacketsForTimeStep(timeStep)

        if len(packets) == 0:
            return

        if self.debug:
            logging.debug(f"Sender #{self.id} created and sent {len(packets)} packets at {timeStep}")

        if packets[-1].sentAt != timeStep:
            raise Exception(f"sentAt is not the same as current timeStep")

        self.sendTo(packets, path)
        pass


    def sendTo(self, packets, path: Path):
        path.onIncomingPackets(packets)
        pass

    
    @abstractmethod
    def onACK(self, packet):
        pass



    

