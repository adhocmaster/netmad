from model.Sender import Sender
from model.Path import Path
from model.SimpleQueuePath import SimpleQueuePath


class Simulator:

    def __init__(self, path: Path):
        self.senders = {}
        self.path = path
        self.nextSenderId = 1

    
    def createSenderId(self):
        senderId = self.nextSenderId
        self.nextSenderId += 1
        return senderId


    def validateEnv(self):
        if len(self.senders) is 0:
            raise Exception("No sender in the net")
        if self.path is None:
            raise Exception("No path in the net")

    def run(self, timeMS):

        self.validateEnv()

        for timeStep in range(1, timeMS + 1):
            # 1. receiveACKs
            ackPackets = self.path.getACKs()
            for packet in ackPackets:
                packet.sender.onACK(packet)

            # 2. sendPackets
            for sender in self.senders.values():
                sender.createAndSendPackets(timeStep, self.path)
        
            

if __name__ == "__main__":
   simulator = Simulator(SimpleQueuePath())