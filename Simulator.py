from model.Sender import Sender
from model.Path import Path
from model.SimpleQueuePath import SimpleQueuePath
from model.NoobSender import NoobSender
import pprint
import logging
logging.basicConfig(level=logging.DEBUG)

class Simulator:

    def __init__(self, path: Path):
        self.senders = {}
        self.path = path
        self.nextSenderId = 1
        self.pp = pprint.PrettyPrinter()

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
            print(f"\n************Time step: {timeStep}*********")

            # 0. onTimeStep # any prep work
            self.path.onTimeStep(timeStep)

            # 1. receiveACKs
            ackPackets = self.path.getACKs()
            for packet in ackPackets:
                packet.sender.onACK(packet)

            # 2. sendPackets
            for sender in self.senders.values():
                sender.createAndSendPacketsForTimeStep(timeStep, self.path)

            # 3. print stats
            print(f"Packets in-flight: {self.path.getNumPacketInflight()}")
            self.pp.pprint(self.path.getPipeStats())
            print(f"Path queue size: {self.path.getQSize()}")

            

if __name__ == "__main__":
    simulator = Simulator(SimpleQueuePath(avgTTL=20, noiseMax=10))
    deliveryRate = 5
    sender = NoobSender(simulator.createSenderId(), deliveryRate)
    simulator.senders[sender.id] = sender
    simulator.run(100)