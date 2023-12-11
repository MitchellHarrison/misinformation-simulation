from model import MediaModel
import mesa

N_PRODUCERS = 2
N_CONSUMERS = 10
N_ITERATIONS = 2

model = MediaModel(N_PRODUCERS, N_CONSUMERS)

# iterate once
for i in range(N_ITERATIONS):
    model.step()
model.display()
