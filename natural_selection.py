import random

class Agent:
    def __init__(self, x, y, environment):
        self.x = x
        self.y = y
        self.fitness = 0
        self.environment = environment
        self.death_rate = 0.01

    # Movement is completely random
    def move(self):
        self.x += random.randint(-1, 1)
        self.y += random.randint(-1, 1)

    def calculate_fitness(self):
        # Calculate fitness based on distance from center of environment
        center_x = self.environment.width / 2
        center_y = self.environment.height / 2
        distance = ((self.x - center_x) ** 2 + (self.y - center_y) ** 2) ** 0.5
        if distance == 0:
            self.fitness = 0
        else:
            self.fitness = 1 / distance

    # death is random, probability adjusted via death_rate
    def die(self):
        if random.random() < self.death_rate:
            self.environment.agents.remove(self)

class Environment:
    def __init__(self, width, height, num_agents):
        self.width = width
        self.height = height
        self.agents = [Agent(random.randint(0, width), random.randint(0, height), self) for _ in range(num_agents)] # 10 agents to start
        self.agent_counts = [len(self.agents)]
        self.avg_fitness = []
        self.agents_history = [self.agents]

    def step(self):
        for agent in self.agents:
            agent.move()
            agent.calculate_fitness()
            agent.die()

        # Select agents for reproduction based on fitness
        total_fitness = sum(agent.fitness for agent in self.agents)
        probabilities = [agent.fitness / total_fitness for agent in self.agents]
        new_agents = []
        for _ in range(len(self.agents)):
            parent1 = random.choices(self.agents, probabilities)[0]
            parent2 = random.choices(self.agents, probabilities)[0]
            child_x = (parent1.x + parent2.x) / 2
            child_y = (parent1.y + parent2.y) / 2
            new_agents.append(Agent(child_x, child_y, self))

        # Replace old agents with new ones
        self.agents = new_agents

        self.agents_history.append(self.agents)

        # Update average fitness as metric
        self.avg_fitness.append(total_fitness / len(self.agents)) if len(self.agents) else self.avg_fitness.append(0)

        # Add current number of agents to list
        self.agent_counts.append(len(self.agents))
    
    def plot(self):
        import matplotlib.pyplot as plt
        import matplotlib.animation as animation
        import os

        self.mypath = os.path.dirname(os.path.abspath(__file__)) + '/'
        # set parameters
        frames = 10
        # create data
        print(self.agents_history[0])
        x = [agent.x for agent in self.agents_history[0]]
        y = [agent.y for agent in self.agents_history[0]]

        # set how the graph will change each frame
        # sizes = itertools.cycle([10, 50, 150])
        # colors = np.random.rand(frames, points)
        # colormaps = itertools.cycle(['Purples', 'Blues', 'Greens', 'Oranges', 'Reds'])
        # markers = itertools.cycle(['o', 'v', '^', 's', 'p'])

        # init the figure
        fig, ax = plt.subplots(figsize=(5,5))

        def update(i):
            # clear the axis each frame
            ax.clear()
            # replot things
            ax.scatter(x, y,
                    s=1,
                    c='k',
                    # cmap=next(colormaps),
                    marker='.')

            # reformat things
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            # ax.set_xlim(min(x), max(x))
            # ax.set_ylim(min(y), max(y))
            ax.set_xlim(0, 100)
            ax.set_ylim(0, 100)

        ani = animation.FuncAnimation(fig, update, frames=frames, interval=1)
        ani.save(self.mypath + 'scatter.gif', writer='pillow')

def simulate(iterations, num_agents=10) :
    env = Environment(100, 100, num_agents)
    for i in range(iterations) :
        env.step()
        if i == iterations - 1 :
            return(env.agent_counts, env.avg_fitness, env.agents)
