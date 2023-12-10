class Producer:
    def __init__(self, id_ = 1, party = "red"):
        self.id_ = id_
        self.party = party
        self.consumers = set()


    def __eq__(self, other):
        if isinstance(other, Producer):
            return self.id_ == other.id_
        return False

    
    def __str__(self):
        return f"""
        PRODUCER
        _______________________

        ID : {self.id_}
        Party : {self.party}
        """
