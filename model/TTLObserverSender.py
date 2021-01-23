from model.Sender import Sender
from model.SenderType import SenderType
import logging
import math
import numpy as np
from collections import deque

class TTLObserverSender(Sender):

    def __init__(self, id, deliveryRate, debug=True, TTLWindowSize=5):
        super().__init__(id, SenderType.Noob, deliveryRate=deliveryRate, debug=debug)
        self.TTLWindowSize = TTLWindowSize
        self.avgTTLLifeTime = None # a huge number in ms
        self.avgTTLWindowTime = 999999
        self.TTLWindow = deque(maxlen=self.TTLWindowSize)


    def getNumberOfPacketsToCreateForTimeStep(self, timeStep):
        num = math.floor(timeStep * self.deliveryRate)  - math.floor((timeStep - 1) * self.deliveryRate)
        # randomness
        return math.floor( num * np.random.uniform(0.5, 1.1))
        

    def onTimeStepStart(self, timeStep):
        """To be called at the beginning of a timeStep

        Args:
            timeStep ([type]): [description]
        """

        if len(self.TTLWindow) > 0:
            self.avgTTLWindowTime = np.mean(self.TTLWindow)
        
        if self.avgTTLLifeTime > self.avgTTLWindowTime:
            # we can increase
            self.stepUpDeliveryRate()
        elif self.avgTTLLifeTime < self.avgTTLWindowTime:
            self.stepDownDeliveryRate()

        pass


    def onTimeStepEnd(self, timeStep):
        """To be called at the end of a timeStep

        Args:
            timeStep ([type]): [description]
        """
        pass
    

    def onACK(self, packet):

        super().onACK(packet)
        # packet loss conditions:
        # 1. ACK out of order.
        # 2. 
        if self.debug:
            logging.info(f"{self.getName()}: got ack for packet {packet.getPacketNumber()}")

        if self.avgTTLLifeTime is None:
            self.avgTTLLifeTime = packet.ttl
        
        self.TTLWindow.append(packet.ttl)
        pass


    def stepUpDeliveryRate(self):
        self.deliveryRate *=  (self.avgTTLLifeTime / self.avgTTLWindowTime)
        self.avgTTLLifeTime = self.avgTTLWindowTime
        pass
        
    def stepDownDeliveryRate(self):
        self.deliveryRate *=  (self.avgTTLLifeTime / self.avgTTLWindowTime)
        self.avgTTLLifeTime = self.avgTTLWindowTime
        pass
        