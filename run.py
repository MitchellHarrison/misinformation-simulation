from model import MediaModel
import mesa

N_PRODUCERS = 2
N_CONSUMERS = 10

model = MediaModel(N_PRODUCERS, N_CONSUMERS)
print(model)
for agent in model.agents:
    print(agent)

# iterate once
model.step()
