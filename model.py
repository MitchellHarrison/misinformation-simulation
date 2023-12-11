from consumer import Consumer
from producer import Producer
from information import Information
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random

class MediaModel:
    def __init__(self, n_producers = 3, n_consumers = 50):
        self.n_producers = n_producers
        self.n_consumers = n_consumers
        self.n_agents = n_producers + n_consumers

        # create list of agents
        self.agents = []
        self.consumers = []
        self.producers = []
        for i in range(self.n_agents):
            # create produce}s
            if i < n_producers:
                if i % 2 == 0:
                    color = "red"
                else:
                    color = "blue"
                agent = Producer(i + 1, color)
                self.producers.append(agent)

            # create consumers
            else:
                agent = Consumer(i + 1, np.random.uniform(-1,1))
                self.consumers.append(agent)
            #print(agent)
            self.agents.append(agent)

        # represent model as NetworkX graph
        edges_per_node = dict()
        for consumer in self.consumers:
            edges_per_node[consumer.id_] = consumer.n_friends

        self.G = nx.Graph()
        self.G.add_nodes_from([a.id_ for a in self.agents])
        self.setup_starting_edges(edges_per_node)


    # return ID of consumers that have enough friends already
    def check_edge_count(self, edges_per_node) -> set:
        output = set()
        for node, max_friends in edges_per_node.items():
            current_neighbors = set(self.G.neighbors(node))
            friend_edges = len(current_neighbors) - 1
            if friend_edges < max_friends:
                continue
            else:
                output.add(node)
        return output


    # setup edges between relevant consumers and producers
    def setup_starting_edges(self, edges_per_node) -> None:
        producers = [agent for agent in self.agents if 
                     isinstance(agent, Producer)]
        consumers = [agent for agent in self.agents if 
                     isinstance(agent, Consumer)]
        edges = [] 

        # Connect each consumer to at least one producer
        for consumer in consumers:
            right_color = False
            while not right_color:
                producer = np.random.choice(producers)
                if producer.party == consumer.party:
                    self.G.add_edge(consumer.id_, producer.id_, weight = 1)
                    right_color = True

        # Add friends at random using friend diversity data
        reds = [a for a in self.agents[self.n_producers:] if a.party == "red"]
        blues = [a for a in self.agents[self.n_producers:] if a.party == "blue"]
        for c in self.agents[self.n_producers:]:
            # divide friends by 2 to correct over-adding of non-diverse friends
            n_friends_same = (c.n_friends_ideal - c.n_friends_diverse_ideal) / 2
            if c.party == "red":
                sames = reds
                diffs = blues
            else:
                sames = blues
                diffs = reds

            new_friends_same = random.sample(sames, int(n_friends_same))
            new_friends_diff = random.sample(diffs, int(c.n_friends_diverse_ideal))
            new_friends = new_friends_same + new_friends_diff
            for f in new_friends:
                if f.id_ == c.id_:
                    continue
                self.make_friends(c, f)

        # add edges
        for c in self.agents[self.n_producers:]:
            idx = c.id_
            connects = c.friends + c.producers
            for f in connects:
                edges.append((idx, f.id_, {"weight": 1}))

        self.G.add_edges_from(edges)
        

    # create relatinship between two consumers
    def make_friends(self, f1, f2) -> None:
        f1.add_friend(f2)
        f2.add_friend(f1)


    def remove_friends(self, f1, f2) -> None:
        f2.remove_friend(f1)
        f1.remove_friend(f2)


    # control what occurs at each model iteration
    def step(self, wdelta_same = 0.1, wdelta_diff = 0.05, miswdelta_same = 0.0, 
            miswdelta_diff = -0.4, miswdelta_trusted = 0.4, poldelta_mono = 0.1,
            poldelta_mis = 0.2, poldelta_diverse = 0.1, new_weight = 0.5, 
            frienddelta_pol = -0.1, friendsame_pol = 0.1, breakup_thresh = 0.3):

        for p in self.producers:
            # generate info from producer
            info = p.gen_info()

            # let connected consumers consume info
            consumer_ids = self.G.neighbors(p.id_)
            consumers = [c for c in self.consumers if c.id_ in consumer_ids]
            for c in consumers:

                # if information not misinformation, do the following
                if not info.is_misinformation:
                    # if producer party and consumer party are the same,
                    # build trust between consumer and producer
                    if p.party == c.party:
                        self.adjust_weight(c.id_, p.id_, wdelta_same)
                    else:
                        self.adjust_weight(c.id_, p.id_, wdelta_diff)

                # if information is misinformation
                else:
                    most_trusted = self.most_trusted_source(c.id_)
                    # trust more if most trusted source
                    if p.id_ == most_trusted:
                        self.adjust_weight(c_id, p_id, wmisdelta_trusted)

                    # no change in trust if party is same but not most trusted
                    elif p.party == c.party:
                        self.adjust_weight(c_id, p_id, wmisdelta_same)

                    # lower trust if party is different from consumer
                    else:
                        self.adjust_weight(c_id, p_id, wmisdelta_diff)
                
            # adjust consumer political scores
            for c in self.consumers:
                # if a consumer consumes only the misinformation source, they
                # become political much faster
                pn = -1 * (c.party == "blue")
                if c.consumes_misinfo_only():
                    c.politics_score += pn * poldelta_mis

                # if multiple media sources of varying politics
                elif c.consumes_diverse_media():
                    c.politics_score += pn * poldelta_div

                # if consumes one-party media, but not misinformation
                elif c.consumes_mono_media():
                    c.politics_score += pn * poldelta_mono
                     
                # possibly make new friends 
                bad_pick = True
                while bad_pick:
                    f = np.random.choice(self.consumers)
                    if f.id_ != c.id_ and not c.is_friend(f):
                        bad_pick = False
                
                p_friendship = 1 - np.abs(c.politics_score - f.politics_score)
                if np.random.rand() < p_friendship:
                    self.make_friends(c, f)
                    self.G.add_edge(c.id_, f.id_, weight = new_weight)

                for f in c.friends:
                    if np.abs(c.politics_score - f.politics_score) > 0.5:
                        self.adjust_weight(c.id_, f.id_, frienddelta_pol)
                    else:
                        self.adjust_weight(c.id_, f.id_, friendsame_pol)

                # end friendships
                for f in c.friends:
                    if self.get_edge_weight(c.id_, f.id_) < breakup_thresh:
                        try:
                            self.G.remove_edge(c.id_, f.id_)
                            self.remove_friends(c, f)
                        except nx.exception.NetworkXError:
                            pass


    def display(self):
        node_colors = [node.party for node in self.agents]
        nx.draw(self.G, with_labels=True, font_weight='bold', node_size=700,
                node_color=node_colors, font_size=10, font_color='black',
                font_family='sans-serif')
        plt.show()

    
    def get_media_sources(self, c_id):
        consumer_ids = self.G.neighbors(p.id_)
        consumers = [c for c in self.consumers if c.id_ in consumer_ids]


    def get_edge_weight(self, node1_id, node2_id):
        try:
            return self.G.get_edge_data(node1_id, node2_id)["weight"]
        except TypeError:
            return 0


    def most_trusted_source(self, node_id):
        neighbors = list(self.G.neighbors(node_id))
        highest = max(neighbors, key = lambda x : self.G[node_id][x]["weight"])
        return hightest


    def adjust_weight(self, node1, node2, delta):
        try:
            self.G[node1][node2]["weight"] += delta
        except KeyError:
            return


    # this function changes what displays when running print(MediaModel)
    def __str__(self):
        return f"""
        MODEL
        _______________________

        Number of producers: {self.n_producers}
        Number of consumers: {self.n_consumers}
        """
