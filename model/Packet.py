class Packet:

    def __init__(self, id, sender, size:int=20, sentAt=0):
        self.id = id
        self.sender = sender
        self.size = size # in bytes

        self.receiver = None
        self.sentAt = sentAt # in ms
        self.ackAt = 0 # in ms
        self.ttl = 0 # in ms
        self.ttlNoise = 0 # in ms
        self.isDropped = False

    
    def __str__(self):

        return (
        f" \nid: {self.id} \n"
        f"sender: {self.sender.getName()} \n"
        f"size: {self.size} \n"
        f"receiver: {self.receiver} \n"

        f"sentAt: {self.sentAt} \n"
        f"ackAt: {self.ackAt} \n"
        f"ttl: {self.ttl} \n"
        f"ttlNoise: {self.ttlNoise} \n"
        f"isDropped: {self.isDropped}"
        )
    
