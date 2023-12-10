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
                agent = Consumer(i + 1)
                self.consumers.append(agent)
            print(agent)
            self.agents.append(agent)

        # represent model as NetworkX graph
        edges_per_node = dict()
        for consumer in self.agents[n_producers:]:
            edges_per_node[consumer.id_] = consumer.n_friends

        #self.G = nx.Graph()
        #self.G.add_nodes_from([agent.id_ for agent in self.agents])
        #self.setup_starting_edges(edges_per_node)
        #colors = ["red" if isinstance(agent, Producer) else "skyblue" for 
        #          agent in self.agents]
        #nx.draw(self.G, with_labels=True, font_weight='bold', node_size=700,
        #        node_color=colors, font_size=10, font_color='black',
        #        font_family='sans-serif')
        #plt.show()
        self.setup_starting_edges2()


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

        # Connect each consumer to at least one producer
        for consumer in consumers:
            producer = np.random.choice(producers)
            self.G.add_edge(consumer.id_, producer.id_)

        # Add additional edges to meet the specified number of friends
        for node, num_edges in edges_per_node.items():
            full_friends =  self.check_edge_count(edges_per_node)
            existing_edges = set(self.G.neighbors(node))

            if len(existing_edges) >= edges_per_node[node]:
                full_friends.union({node})
                continue

            potential_friends = set(consumer.id_ for consumer in consumers)
            potential_friends -= existing_edges
            potential_friends -= {node}
            potential_friends -= full_friends
            additional_edges = min(num_edges - 1, len(potential_friends))

            # Prioritize connections to producers
            producers_friends = set(producer.id_ for producer in producers)
            selected_producer_friends = list(producers_friends &
                                             potential_friends)
            additional_producer_edges = min(additional_edges,
                                            len(selected_producer_friends))
            selected_nodes = selected_producer_friends[:additional_producer_edges]

            # Randomly select additional friends from the remaining consumers
            remaining_friends = list(potential_friends - set(selected_nodes))

            remaining_additional_edges = additional_edges
            remaining_additional_edges -= additional_producer_edges

            selected_nodes.extend(random.sample(remaining_friends,
                                                remaining_additional_edges))

            self.G.add_edges_from([(node, friend) for friend in selected_nodes])
        

    def setup_starting_edges2(self) -> None:
        red_producers = []
        blue_producers = []
        for producer in self.agents[:self.n_producers]:
            if producer.party == "red":
                red_producers.append(producer)
            elif producer.party == "blue":
                blue_producers.append(producer)

        consumers = self.agents[self.n_producers:]
        for consumer in consumers:

            # add producers for each consumer
            if consumer.party == "red":
                consumer.producers.append(np.random.choice(red_producers))

                if consumer.consumes_diverse:
                    new_blue = np.random.choice(blue_producers)
                    consumer.producers.append(new_blue)

            elif consumer.party == "blue":
                consumer.producers.append(np.random.choice(blue_producers))

                if consumer.consumes_diverse:
                    new_red = np.random.choice(red_producers)
                    consumer.producers.append(new_red)


            # add friends for each consumer, checking for nodes that need them
            options = random.sample(self.consumers, len(self.consumers))
            for o in options:
                if consumer.id_ == o.id_ or consumer.is_friend(o):
                    continue
                
                if o.n_friends < o.n_friends_ideal:
                    if o.party == consumer.party:
                        self.make_friends(consumer, o)
                        if consumer.n_friends >= consumer.n_friends_ideal:
                            break
                    else:
                        o_needs = o.needs_friends_diverse()
                        c_needs = consumer.needs_friends_diverse()
                        if o_needs and c_needs:
                            self.make_friends(consumer, o)
                            if consumer.n_friends >= consumer.n_friends_ideal:
                                break

            missing = True
            while missing:
                if consumer.n_friends < consumer.n_friends_ideal:
                    others = {
                        "blue": [o for o in options if o.party == "red" and
                                 not consumer.is_friends(o)],
                        "red": [o for o in options if o.party == "blue" and
                                not consumer.is_friends(o)]
                    }

                    same = {
                        "red": others["blue"],
                        "blue": others["red"]
                    }

                    # if more diverse friends are needed
                    if consumer.n_friends_diverse<consumer.n_friends_diverse_ideal:
                        new_friend = np.random.choice(others[consumer.party])
                    else:
                        new_friend = np.random.choice(same[consumer.party])

                    self.make_friends(consumer, new_friend)

                    if consumer.n_friends >= consumer.n_friends.ideal and \
                    consumer.n_friends.diverse >= consumer.n_friends_diverse_ideal:
                        missing = False


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
