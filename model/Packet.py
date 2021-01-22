class Packet:

    def __init__(self, id, sender, size=20, sentAt=0):
        self.id = id
        self.sender = sender
        self.size = size # in bytes

        self.receiver = None
        self.sentAt = sentAt # in ms
        self.receivedAt = 0 # in ms
        self.ttl = 0 # in ms
        self.ttl_noise = 0 # in ms
        self.isDropped = False

    
    def __str__(self):

        return (
        f" \nid: {self.id} \n"
        f"sender: {self.sender} \n"
        f"size: {self.size} \n"
        f"receiver: {self.receiver} \n"

        f"sentAt: {self.sentAt} \n"
        f"receivedAt: {self.receivedAt} \n"
        f"ttl: {self.ttl} \n"
        f"ttl_noise: {self.ttl_noise} \n"
        f"isDropped: {self.isDropped}"
        )
    
