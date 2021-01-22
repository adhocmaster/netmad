from model.Sender import Sender
from model.Path import Path
from model.SimpleQueuePath import SimpleQueuePath
from model.NoobSender import NoobSender
import pprint
import matplotlib.pyplot as plt
import logging
logging.basicConfig(level=logging.INFO)

class Simulator:

    def __init__(self, path: Path):
        self.senders = {}
        self.path = path
        self.nextSenderId = 1
        self.pp = pprint.PrettyPrinter()
        self.stats = {}

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

        self.stats['packetsInFlight'] = []
        self.stats['dataInFlight'] = []
        self.stats['queueSize'] = []
        self.stats['packetsSent'] = []
        self.stats['packetsAcked'] = []
        self.stats['totalPacketsSent'] = []
        self.stats['totalPacketsAcked'] = []
        totalPacketsSent = 0
        totalPacketsAcked = 0

        for timeStep in range(1, timeMS + 1):
            print(f"\n************Time step: {timeStep}*********")

            # 0. onTimeStep # any prep work
            self.path.onTimeStep(timeStep)

            # 1. receiveACKs
            ackPackets = self.path.getACKs()
            self.stats['packetsAcked'].append(len(ackPackets))
            totalPacketsAcked += len(ackPackets)
            self.stats['totalPacketsAcked'].append(totalPacketsAcked)
            
            for packet in ackPackets:
                packet.sender.onACK(packet)

            # 2. sendPackets
            for sender in self.senders.values():
                numPackets = sender.createAndSendPacketsForTimeStep(timeStep, self.path)
                self.stats['packetsSent'].append(numPackets)
                totalPacketsSent += numPackets
                self.stats['totalPacketsSent'].append(totalPacketsSent)

            # 3. print stats
            self.stats['packetsInFlight'].append(self.path.getNumPacketInflight())
            self.stats['dataInFlight'].append(self.path.getDataInFlightInKB())
            self.stats['queueSize'].append(self.path.getQSize())
            print(f"Packets in-flight: {self.path.getNumPacketInflight()}")
            print(f"Data in-flight: {self.path.getDataInFlightInKB()}KB")
            self.pp.pprint(self.path.getPipeStats())
            print(f"Path queue size: {self.path.getQSize()}")

            # 4. terminate early if path overflowed
            if self.path.isOverflowed():
                print("Path overflowed. Terminating....")
                break

            

if __name__ == "__main__":
    simulator = Simulator(SimpleQueuePath(avgTTL=20, noiseMax=20, maxDataInflight=10, maxQsize=100))
    deliveryRate = 25
    sender = NoobSender(simulator.createSenderId(), deliveryRate)
    simulator.senders[sender.id] = sender
    simulator.run(100)

    plt.plot(simulator.stats['dataInFlight'], label="Data in flight")
    plt.plot(simulator.stats['packetsInFlight'], label="Packet in flight")
    plt.plot(simulator.stats['queueSize'], label="Queue size")
    plt.plot(simulator.stats['packetsSent'], label="Packets Sent")
    plt.plot(simulator.stats['packetsAcked'], label="Packet Acked")
    plt.plot(simulator.stats['totalPacketsSent'], label="Total packets Sent")
    plt.plot(simulator.stats['totalPacketsAcked'], label="Total packet Acked")
    plt.title("Simulation stats")
    plt.legend()
    plt.show()