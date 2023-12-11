from consumer import Consumer
from producer import Producer
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
        for consumer in self.agents[n_producers:]:
            edges_per_node[consumer.id_] = consumer.n_friends

        self.G = nx.Graph()
        self.G.add_nodes_from([a.id_ for a in self.agents])
        self.setup_starting_edges(edges_per_node)
        node_colors = [node.party for node in self.agents]
        nx.draw(self.G, with_labels=True, font_weight='bold', node_size=700,
                node_color=node_colors, font_size=10, font_color='black',
                font_family='sans-serif')
        plt.show()


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
                    self.G.add_edge(consumer.id_, producer.id_)
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
                edges.append((idx, f.id_))

        self.G.add_edges_from(edges)
        

    # create relatinship between two consumers
    def make_friends(self, f1, f2) -> None:
        f1.add_friend(f2)
        f2.add_friend(f1)


    # control what occurs at each model iteration
    def step(self):
        return


    # this function changes what displays when running print(MediaModel)
    def __str__(self):
        return f"""
        MODEL
        _______________________

        Number of producers: {self.n_producers}
        Number of consumers: {self.n_consumers}
        """
