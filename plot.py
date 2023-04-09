import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from natural_selection import simulate

agent_count, fitness, agents = simulate(100, 100)

fig, axs = plt.subplots(3)
fig.tight_layout()
fig.subplots_adjust(top=0.88)
# figure size
fig.set_size_inches(5, 10)
fig.suptitle("Agent Population and Fitness Over Time")
axs[0].plot(agent_count)
axs[0].set(ylabel="Number of Agents", xlabel="Generations")
axs[1].plot(fitness)
axs[1].set(ylabel="Average Fitness", xlabel="Generations")
# Plot agent locations
x = [agent.x for agent in agents]
y = [agent.y for agent in agents]
axs[2].set_title("Agent Locations")
axs[2].grid()
axs[2].scatter(x, y, s=1, c ='k', marker='.')
axs[2].set(ylabel="Y", xlabel="X")
axs[2].set_xlim(0, 100)
axs[2].set_ylim(0, 100)

plt.show()
