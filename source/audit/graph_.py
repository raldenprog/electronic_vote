import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from random import randint

graph = {
    (datetime.now()).strftime('%H:%M'): 0,
}

delta = 0
for i in range(25):
    delta += 10
    graph[(datetime.now() + timedelta(minutes=delta)).strftime('%H:%M')] = randint(10, 40)

fig, ax = plt.subplots()

# plt.figure(figsize=(12, 7))

# plt.plot(graph.keys(), graph.values(), 'o-b')
# plt.legend()

ax.plot(graph.keys(), graph.values(), 'o-b')
ax.set_xlabel('Время',
              fontsize=15
              )
ax.set_ylabel('Количество принятых бюллетеней',
              fontsize=15)

plt.grid(True)
