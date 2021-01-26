# netmad - Minimalistic network simulator


# stream loop:
Each loop is considered one time-step which is equal to 1 ms. Starting time step is 1 (not 0)

## delivery mechanism:
In each loop, a sender will send delivery_rate number of packets. we need to track total time passed. number of packets to send in current loop is actually - 
   floor(currentTimeStepNo * delivery rate)  - floor(lastTimeStepNo * delivery rate)


# Simulator

        self.stats['dataInFlight'] = []
        self.stats['dataInQueue'] = []
        self.stats['packetsInFlight'] = []
        self.stats['packetsInQueue'] = []
        self.stats['packetsSent'] = []
        self.stats['packetsAcked'] = []
        self.stats['totalPacketsSent'] = []
        self.stats['totalPacketsAcked'] = []
## Stats
Simulator stats are gathered for every timeStep of the simulation. The data is collected in a dictionary called **stats** keyed by categories. The categories of the data are

1. **dataInFlight**: amount of data in flight 
2. **dataInQueue**: amount of data in path's queue
3. **packetsInFlight**: 
4. **packetsInQueue**:
5. **packetsSent**:
6. **packetsAcked**:
7. **totalPacketsSent**:
8. **totalPacketsAcked**:

## Loop Simulator life cycle:

In general, a loop based simulator will run for some timeSteps. Each time step has some life cycle events:

1. timeStepStart: at the beginning of the step
2. receiveACKs: the packets that should be acknowledged in this step are gathered (and removed) from the path and sent to the senders
3. sendPackets: senders are allowed to send packets
4. gather timeStep stats: stats are gathered 
5. network overflowed: terminate simulation
6. timeStepEnd: end of a timeStep. 


# Sender (Abstract)
The base class for Senders. Only the **public API** is documented here.

## Properties:
1. **ackedPackets**: acknowledged packets per timeStep, keyed by timeSteps of the simulation. *Not* all the timeSteps has a key in this dictionary as it is only populated if an ack arrives at the sender
2. **deliveryRate**: delivery rate of the sender in packets. It may change over time.
3. **nextPacketNumber**: next packet number, used to generate id for the next packet
4. **lock**: used to generate next packet id. 

## API methods to be implemented by concrete senders.

### Lifecycle methods:
1. **onTimeStepStart**: To be called at the start of each time step. All the state variables should be changed here or at onTimeStepEnd
2. **onTimeStepEnd**: To be called at the start of each time step. All the state variables should be changed here or at onTimeStepStart
3. **onFinish**: To be called after the simulation is done.

### Packet methods:
1. **onACK**: called when an ACK received. **Must called the super method when implemented.**
2. **getNumberOfPacketsToCreateForTimeStep**: given a timeStep, this function decides number of packets to be created.


## Overridable methods, but not required:
1. **createAndSendPacketsForTimeStep**: create new packets and send to a given path in a given timeStep


# Path (Abstract)

Path calculates the ttl for packets and releases the packets at (sentAt + ttl) timeStep.

## SimpleQueuePath:

Whenever a packet comes, it either adds a ttl value to the packet or keeps it in the queue depending on data in pipe. This path does not reflect TCP protocol.

### Assumptions:
1. delivery rate is indirectly clamped by the length of the pipe (amount of data travelling)

1. Does not ensure packet order in sending acknowledgements. 
2. Does not check for packet order when receiving. 

# AnalyzerTools

## 
