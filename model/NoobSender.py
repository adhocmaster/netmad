from model.Sender import Sender
from model.SenderType import SenderType
import logging
import math
import numpy as np

class NoobSender(Sender):

    def __init__(self, id, deliveryRate):
        super().__init__(id, SenderType.Noob, deliveryRate=deliveryRate)

    def getNumberOfPacketsToCreateForTimeStep(self, timeStep):
        num = math.floor(timeStep * self.deliveryRate)  - math.floor((timeStep - 1) * self.deliveryRate)
        # randomness
        return math.floor( num * np.random.uniform(0.5, 1.1))
        
    def onACK(self, packet):

        # packet loss conditions:
        # 1. ACK out of order.
        # 2. 
        if self.debug:
            logging.info(f"{self.getName()}: got ack for packet {packet}")
        pass