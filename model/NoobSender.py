from model.Sender import Sender
from model.SenderType import SenderType

class NoobSender(Sender):

    def __init__(self, id, deliveryRate):
        super().__init__(id, SenderType.Noob, deliveryRate=deliveryRate)

        
    def onACK(self, packet):
        pass