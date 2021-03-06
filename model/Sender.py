from abc import ABC, abstractmethod
import time, collections
import threading
from model.Packet import Packet
from model.SenderType import SenderType
from model.Path import Path
import math
import numpy as np
import logging
import pandas as pd

class Sender(ABC):

    def __init__(self, id, senderType: SenderType, deliveryRate = 0.1, debug=True):
        self.lock = threading.RLock()
        self.id = id
        self.nextPacketNumber = 1
        self.type = senderType
        self.deliveryRate = deliveryRate # per ms
        self.debug = debug
        self.ackedPackets = {}
    
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
        
        numberOfPackets = self.getNumberOfPacketsToCreateForTimeStep(timeStep)
        # if self.debug:
        #     logging.info(f"Sender #{self.id} creating {numberOfPackets} packets at {timeStep}")
        return self.createPackets(numberOfPackets, sizeMin=20, sizeMax=20, sentAt=timeStep)


    def createAndSendPacketsForTimeStep(self, timeStep, path: Path):
        packets = self.createPacketsForTimeStep(timeStep)

        if len(packets) == 0:
            return 0

        if self.debug:
            logging.info(f"Sender #{self.id} created and sent {len(packets)} packets at {timeStep}")

        if packets[-1].sentAt != timeStep:
            raise Exception(f"sentAt is not the same as current timeStep")

        self.sendTo(packets, path)
        
        return len(packets)


    def sendTo(self, packets, path: Path):
        path.onIncomingPackets(packets)
        pass

    
    def finalizeStats(self):
        self.ackedPackets = collections.OrderedDict(sorted(self.ackedPackets.items()))

    
    @abstractmethod
    def onTimeStepStart(self, timeStep):
        """To be called at the beginning of a timeStep

        Args:
            timeStep ([type]): [description]
        """
        pass

    @abstractmethod
    def onTimeStepEnd(self, timeStep):
        """To be called at the end of a timeStep

        Args:
            timeStep ([type]): [description]
        """
        pass

    
    def onFinish(self):
        """To be called after simulation is finished
        """
        self.finalizeStats()
    
    @abstractmethod
    def getNumberOfPacketsToCreateForTimeStep(self, timeStep):
        pass


    @abstractmethod
    def onACK(self, packet):
        self.ackedPackets[packet.getPacketNumber()] = packet
        pass



    

