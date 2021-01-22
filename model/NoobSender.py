from model.Sender import Sender
from model.SenderType import SenderType
import logging

class NoobSender(Sender):

    def __init__(self, id, deliveryRate):
        super().__init__(id, SenderType.Noob, deliveryRate=deliveryRate)

        
    def onACK(self, packet):

        if self.debug:
            logging.debug(f"{self.getName()}: got ack for packet {packet}")
        pass