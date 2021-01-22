# netmad - Minimalistic network simulator


# stream loop:
Each loop is considered one time-step which is equal to 1 ms. Starting time step is 1 (not 0)

## delivery mechanism:
In each loop, a sender will send delivery_rate number of packets. we need to track total time passed. number of packets to send in current loop is actually - 
   floor(currentTimeStepNo * delivery rate)  - floor(lastTimeStepNo * delivery rate)