from information import Information
import numpy as np

class Producer:
    def __init__(self, id_ = 1, party = "red", misinfo_rate = 0.0):
        self.id_ = id_
        self.party = party
        self.consumers = set()
        self.misinfo_rate = misinfo_rate


    def gen_info(self) -> Information:
        is_misinformation = False
        if np.random.rand() < self.misinfo_rate:
            is_misinformation = True

        info = Information(self.party, is_misinformation)
        return info


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
