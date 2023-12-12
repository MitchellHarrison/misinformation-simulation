from information import Information
import numpy as np
import csv
import os

PATH = "data/producer_parameters.csv"

class Producer:
    def __init__(self, id_ = 1, party = "red", misinfo_rate = 0.0):
        self.id_ = id_
        self.party = party
        self.consumers = set()
        self.misinfo_rate = misinfo_rate
        self.save_starting_state()


    def gen_info(self) -> Information:
        is_misinformation = False
        if np.random.rand() < self.misinfo_rate:
            is_misinformation = True

        info = Information(self.party, is_misinformation)
        return info

    
    def save_starting_state(self, path = PATH):
        data = {
                "id": self.id_,
                "party": self.party,
                "misinformation_rate": self.misinfo_rate
                }

        with open(path, "a", newline = "") as f:
            writer = csv.DictWriter(f, fieldnames = data.keys())
            if os.path.getsize(path) == 0:
                writer.writeheader()
            writer.writerow(data)


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
