from model.Sender import Sender
from model.SenderType import SenderType
import logging
import math
import numpy as np
from collections import deque

class TTLObserverSender(Sender):

    def __init__(self, id, deliveryRate, debug=True, TTLWindowSize=5, goalTTL=40, minDeliveryRate=5):
        super().__init__(id, SenderType.Noob, deliveryRate=deliveryRate, debug=debug)
        self.TTLWindowSize = TTLWindowSize
        self.goalTTL = goalTTL # a huge number in ms
        self.minDeliveryRate = minDeliveryRate
        self.avgTTLWindowTime = 20
        self.TTLWindow = deque(maxlen=self.TTLWindowSize)

        self.previousTTL = 20


    def getNumberOfPacketsToCreateForTimeStep(self, timeStep):
        num = math.floor(timeStep * self.deliveryRate)  - math.floor((timeStep - 1) * self.deliveryRate)
        # randomness
        return math.floor( num * np.random.uniform(0.5, 1.1))
        

    def onTimeStepStart(self, timeStep):
        """To be called at the beginning of a timeStep

        Args:
            timeStep ([type]): [description]
        """

        self.adjustDeliveryRate(timeStep)

        pass

    def adjustDeliveryRate(self, timeStep):

        if timeStep % self.goalTTL != 0:
            return

        if len(self.TTLWindow) > 0:
            self.avgTTLWindowTime = np.mean(self.TTLWindow)
        
        if self.previousTTL < self.avgTTLWindowTime:
            # ttl is increasing
            self.deliveryRate *= (self.previousTTL / (self.avgTTLWindowTime * 2))

            if self.deliveryRate < self.minDeliveryRate:
                self.deliveryRate = self.minDeliveryRate
            

            if self.debug:
                logging.info(f"TTLObserverSender:increasing ttl avgTTLwindow {self.avgTTLWindowTime}")
                logging.info(f"TTLObserverSender:decreasing {self.deliveryRate}")
        else:

            if self.goalTTL > self.avgTTLWindowTime:
                # we can increase
                self.stepUpDeliveryRate()
            elif self.goalTTL < self.avgTTLWindowTime:
                self.stepDownDeliveryRate()

        self.previousTTL = self.avgTTLWindowTime
        



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
        # if self.debug:
        #     logging.info(f"{self.getName()}: got ack for packet {packet.getPacketNumber()}")

        if self.goalTTL is None:
            self.goalTTL = packet.ttl
        
        self.TTLWindow.append(packet.ttl)
        pass


    def stepUpDeliveryRate(self):
        if self.debug:
            logging.info(f"TTLObserverSender:stepUpDeliveryRate avgTTLwindow {self.avgTTLWindowTime}")
        self.deliveryRate *=  (self.goalTTL / self.avgTTLWindowTime)

        if self.deliveryRate < self.minDeliveryRate:
            self.deliveryRate = self.minDeliveryRate

        if self.debug:
            logging.info(f"TTLObserverSender:stepUpDeliveryRate {self.deliveryRate}")
        pass
        
    def stepDownDeliveryRate(self):
        if self.debug:
            logging.info(f"TTLObserverSender:stepDownDeliveryRate avgTTLwindow {self.avgTTLWindowTime}")
        self.deliveryRate *=  (self.goalTTL / self.avgTTLWindowTime)

        if self.deliveryRate < self.minDeliveryRate:
            self.deliveryRate = self.minDeliveryRate

        if self.debug:
            logging.info(f"TTLObserverSender:stepDownDeliveryRate {self.deliveryRate}")
        pass
        