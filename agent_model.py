# Import necessary libraries
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import numpy as np

class CustomAgent(Agent):
    def __init__(self, unique_id, model, preferred_location):
        super().__init__(unique_id, model)
        self.preferred_location = preferred_location

    def move(self):
        # Include randomness in the agent's movement
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        move_randomly = self.random.random() < 0.2  # 20% chance to move randomly
        if not move_randomly:
            preferred_steps = [step for step in possible_steps if step == self.preferred_location]
            if preferred_steps:
                new_position = self.random.choice(preferred_steps)
            else:
                new_position = self.random.choice(possible_steps)
        else:
            new_position = self.random.choice(possible_steps)
        
        self.model.grid.move_agent(self, new_position)

    def step(self):
        self.move()

class CustomModel(Model):
    def __init__(self, width, height, num_agents, agent_preferences):
        super().__init__()
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.num_agents = num_agents
        # Initialize agent positions for visualization
        self.all_positions = []

        # Create agents with user-defined preferences
        for i in range(num_agents):
            preferred_location = agent_preferences[i]
            a = CustomAgent(i, self, preferred_location)
            x, y = preferred_location  # Place agent at preferred location initially
            self.grid.place_agent(a, (x, y))
            self.schedule.add(a)

    def step(self):
        self.schedule.step()
        # Collect positions for all agents at this step
        positions = [(agent.pos[0], agent.pos[1]) for agent in self.schedule.agents]
        self.all_positions.append(positions)
