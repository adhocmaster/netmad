import pandas as pd
from model.Packet import Packet

class AnalyzerTools:

    def createDfFromPackets(self, packets):
        
        packNums = []
        ttls = []
        ttlNoises = []
        sentAt = []
        ackAt = []
        isDropped = []

        for packNum in packets:
            packNums.append(packNum)
            packet = packets[packNum]
            ttls.append(packet.ttl)
            ttlNoises.append(packet.ttlNoise)
            sentAt.append(packet.sentAt)
            ackAt.append(packet.ackAt)
            isDropped.append(packet.isDropped)

        
        data = {
            'packNum': packNums,
            'ttl': ttls,
            'ttlNoise': ttlNoises,
            'sentAt': sentAt,
            'ackAt': ackAt,
            'isDropped': isDropped
        }
        
        return pd.DataFrame(data)

    
    def getAvgTTLPerTimeStep(self, dfPackets:pd.DataFrame):
        return dfPackets.groupby(['sentAt']).mean()

    
    def getStatsPerTimeStep(self, dfPackets:pd.DataFrame):
        return dfPackets.groupby(['sentAt']).agg(
            avgTTL = pd.NamedAgg(column = "ttl", aggfunc="mean"),
            minTTL = pd.NamedAgg(column = "ttl", aggfunc="min"),
            maxTTL = pd.NamedAgg(column = "ttl", aggfunc="max"),
        )


