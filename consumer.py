import numpy as np

# probs correspond to [many, some, few, none] friends of opposing party (Pew)
RED_FRIEND_PROBS = [.07, .46, .31, .14]
BLUE_FRIEND_PROBS = [.06, .31, .38, .25]

# proportion of friend group that is diverse given above classification
MANY = 0.3
SOME = 0.2
FEW = 0.1
NONE = 0.0
DIVERSE_FRIENDS = [MANY, SOME, FEW, NONE]

# number of close friends probability corresponds to 0, 1, 2, 3, 4, or 5 (Pew)
NUM_FRIENDS_PROBS = [.09, .08, .14, .18, .13, .38]

# probability that an agent consumes diverse mediadata (Pew, Media Bias Chart)
P_DIVERSE_RED = [.244, 1 - .244]
P_DIVERSE_BLUE = [.23, 1 - .23]

class Consumer:
    def __init__(self, id_ = 1, politics_score = 0):
        self.id_ = id_
        self.politics_score = politics_score

        self.n_friends = 0
        self.n_friends_diverse = 0
        self.n_producers = 0
        self.friends = []
        self.producers = []

        if politics_score > 0:
            self.party = "red"
        elif politics_score < 0:
            self.party = "blue"
        elif politics_score == 0:
            self.party = np.random.choice(["red", "blue"])

        self.n_friends_ideal = np.random.choice([0, 1, 2, 3, 4, 5],
                                                p = NUM_FRIENDS_PROBS)

        # how many politically diverse friends a consumer has
        friend_diversity = np.random.choice(DIVERSE_FRIENDS)
        self.n_friends_diverse_ideal = int(self.n_friends * friend_diversity)
        p_div = P_DIVERSE_RED if self.party == "red" else P_DIVERSE_BLUE
        self.consumes_diverse = np.random.choice([True, False], p = p_div)


    def add_friend(self, friend):
        if friend in self.friends:
            print(f"Consumers {self.id_} and {friend.id_} are already friends")
            return
        self.friends.append(friend)
        self.n_friends = len(self.friends) 
        if friend.party != self.party:
            self.n_friends_diverse += 1


    def remove_friend(self, friend):
        try:
            self.friends.remove(f)
        except ValueError:
            print(f"Consumer {friend.id_} is not a friend of consumer {self.id}")
            return
        self.n_friends = len(self.friends)
        if f.party != self.party:
            self.n_diverse_friends -=1


    def add_producer(self, producer):
        if producer in self.producers:
            print(f"Producer {producer.id_} is already producing for {self.id_}")
            return
        self.producers.append(producer)
        self.n_producers += 1


    def remove_producer(self, producer):
        try:
            self.friends.remove(f)
        except ValueError:
            print(f"Producer {producer.id_} is not a producer for {self.id}")
            return
        self.n_producers = len(self.producers)


    def is_friend(self, friend) -> bool:
        for f in self.friends:
            if f.id_ == friend.id_:
                return True
        return False

    
    def needs_friends(self) -> bool:
        return self.n_friends < self.n_friends_ideal

    
    def needs_friends_diverse(self) -> bool:
        return self.n_friends_diverse < self.n_friends_diverse_ideal


    def __eq__(self, other):
        if isinstance(other, Consumer):
            return self.id_ == other.id_
        return False


    def __str__(self):
        return f"""
        CONSUMER
        ______________________

        ID : {self.id_}
        Number of friends : {self.n_friends}
        Politics score : {self.politics_score}
        """
