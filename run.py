from model import MediaModel
import numpy as np
import os
np.random.seed(427)

N_PRODUCERS = 2
N_CONSUMERS = 10
N_ITERATIONS = 20

PATH_PROD_PARAMS = "data/producer_parameters.csv"
PATH_PROD = "data/producers.csv"
PATH_CON = "data/consumers.csv"

if os.path.exists(PATH_PROD_PARAMS):
    os.remove(PATH_PROD_PARAMS)

if os.path.exists(PATH_PROD):
    os.remove(PATH_PROD)

if os.path.exists(PATH_CON):
    os.remove(PATH_CON)

model = MediaModel(N_PRODUCERS, N_CONSUMERS)

# iterate once
for i in range(N_ITERATIONS):
    model.step()
model.save_graph_img(title = "Final graph configuration")
model.display()
