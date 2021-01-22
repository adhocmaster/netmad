import unittest

from model.NoobSender import NoobSender

class test_NoobSender(unittest.TestCase):

    def setUp(self):
        
        deliveryRate = 0.1
        self.sender = NoobSender(1, deliveryRate)

    def test_getNewPacketId(self):

        deliveryRate = 0.1
        sender = NoobSender(1, deliveryRate)

        firstPacketId = sender.getNewPacketId()
        print(firstPacketId)
        assert firstPacketId == "1-1"
        assert sender.getNewPacketId() == "1-2"
        assert sender.getNewPacketId() == "1-3"

        sender2 = NoobSender(2, deliveryRate)
        
        assert sender.getNewPacketId() == "1-4"
        assert sender2.getNewPacketId() == "2-1"

        print(sender.getNewPacketIds(10))
        
        assert sender.getNewPacketId() == "1-15"

    
    def test_createPacket(self):

        packet = self.sender.createPacket(20)
        assert self.sender.nextPacketNumber == 2
        packet = self.sender.createPacket(20)
        assert packet.id == "1-2"

    
    def test_createPacketForTimeStep(self):


        # delivery rate is 0.1 
        packets = self.sender.createPacketsForTimeStep(timeStep = 1)
        assert len(packets) == 0
        packets = self.sender.createPacketsForTimeStep(timeStep = 9)
        assert len(packets) == 0
        packets = self.sender.createPacketsForTimeStep(timeStep = 10)
        assert len(packets) == 1
        packets = self.sender.createPacketsForTimeStep(timeStep = 11)
        assert len(packets) == 0
        packets = self.sender.createPacketsForTimeStep(timeStep = 20)
        assert len(packets) == 1
        packets = self.sender.createPacketsForTimeStep(timeStep = 199)
        assert len(packets) == 0
        packets = self.sender.createPacketsForTimeStep(timeStep = 200)
        assert len(packets) == 1

        assert self.sender.nextPacketNumber == 4

        # set delivery rate to 1
        self.sender.deliveryRate = 1
        packets = self.sender.createPacketsForTimeStep(timeStep = 1)
        assert len(packets) == 1
        packets = self.sender.createPacketsForTimeStep(timeStep = 9)
        assert len(packets) == 1
        packets = self.sender.createPacketsForTimeStep(timeStep = 10)
        assert len(packets) == 1
        packets = self.sender.createPacketsForTimeStep(timeStep = 11)
        assert len(packets) == 1
        packets = self.sender.createPacketsForTimeStep(timeStep = 20)
        assert len(packets) == 1
        packets = self.sender.createPacketsForTimeStep(timeStep = 199)
        assert len(packets) == 1
        packets = self.sender.createPacketsForTimeStep(timeStep = 200)
        assert len(packets) == 1

        assert self.sender.nextPacketNumber == 4 + 7

        # set delivery rate to 10
        self.sender.deliveryRate = 10
        packets = self.sender.createPacketsForTimeStep(timeStep = 1)
        assert len(packets) == 10
        packets = self.sender.createPacketsForTimeStep(timeStep = 9)
        assert len(packets) == 10
        packets = self.sender.createPacketsForTimeStep(timeStep = 10)
        assert len(packets) == 10
        packets = self.sender.createPacketsForTimeStep(timeStep = 11)
        assert len(packets) == 10
        packets = self.sender.createPacketsForTimeStep(timeStep = 20)
        assert len(packets) == 10
        packets = self.sender.createPacketsForTimeStep(timeStep = 199)
        assert len(packets) == 10
        packets = self.sender.createPacketsForTimeStep(timeStep = 200)
        assert len(packets) == 10

        assert self.sender.nextPacketNumber == 4 + 7 + 70

        # set delivery rate to 10.1
        self.sender.deliveryRate = 10.1
        packets = self.sender.createPacketsForTimeStep(timeStep = 1)
        assert len(packets) == 10
        packets = self.sender.createPacketsForTimeStep(timeStep = 9)
        assert len(packets) == 10
        packets = self.sender.createPacketsForTimeStep(timeStep = 10)
        assert len(packets) == 11
        packets = self.sender.createPacketsForTimeStep(timeStep = 11)
        assert len(packets) == 10
        packets = self.sender.createPacketsForTimeStep(timeStep = 20)
        assert len(packets) == 11
        packets = self.sender.createPacketsForTimeStep(timeStep = 199)
        assert len(packets) == 10
        packets = self.sender.createPacketsForTimeStep(timeStep = 200)
        assert len(packets) == 11

        print( self.sender.nextPacketNumber )
        assert self.sender.nextPacketNumber == 4 + 7 + 70 + 73 

        # print(packets)

        pass
        