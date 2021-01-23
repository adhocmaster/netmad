# TTLObserverSender

When packets arrive, they bear a TTL information in them. TTLObserver will observe the TTL values irrespective of the packet sequence or sentAt time. 

delivery rate is updated based on recent TTL information, avgTTL over lifetime.