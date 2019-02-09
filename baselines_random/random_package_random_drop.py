import robotic_warehouse.robotic_warehouse as warehouse
import robotic_warehouse_utils.path_finder as path_finder
import robotic_warehouse_utils.data_collection as data_collection
import pandas as pd
import random
import time


class Robot():
    def __init__(self, capacity, pathfinder):
        self.capacity = capacity
        self.instructions = []
        self.instruction_pointer = 0
        self.pathfinder = pathfinder

    def __call__(self, gym, robot, free_packages) -> "instruction":
        """ IF there is something to do.. do it."""
        if len(self.instructions) > self.instruction_pointer:
            instruction = self.instructions[self.instruction_pointer]
            self.instruction_pointer += 1
            return instruction

        position = robot[0]
        drops = robot[1]
        """ If we are standing next to a package pick it up!"""
        if len(drops) != self.capacity:
            instruction = None
            for f, _ in free_packages:
                if path_finder.l1norm_dist(position, f) == 1:
                    instruction = gym.PICKUP_INSTRUCTION

            if instruction != None:
                return instruction
        """ If there is nothing to do and we have full capacity.. go drop shit."""
        if len(drops) == self.capacity:
            """ IF l1 norm to a drop off == 1 then we can drop of the packages. """
            instruction = None
            for drop in drops:
                if path_finder.l1norm_dist(position, drop) == 1:
                    instruction = gym.DROP_INSTRUCTION

            if instruction != None:
                return instruction

            self.instructions = self.pathfinder(
                position,
                self.pathfinder.available_pos_near(
                    random.choice(drops))).get_instructions()
            self.instruction_pointer = 1
            return self.instructions[0]
        elif free_packages:
            """ If there is nothing to do, we dont have full capacity and there are packages waiting.. get them. """
            target = random.choice(free_packages)[0]
            self.instructions = self.pathfinder(
                position,
                self.pathfinder.available_pos_near(target)).get_instructions()
            self.instruction_pointer = 1
            return self.instructions[0]
        else:
            """ If there is nothing to do, we dont have full capactiy and there are no packages waiting.. do some random shit. """
            return gym.PICKUP_INSTRUCTION


def evaluate(**kwargs):
    robots = 1
    if "robots" in kwargs:
        robots = kwargs["robots"]

    capacity = 1
    if "capacity" in kwargs:
        capacity = kwargs["capacity"]

    spawn = 10
    if "spawn" in kwargs:
        spawn = kwargs["spawn"]

    shelve_length = 2
    if "shelve_length" in kwargs:
        shelve_length = kwargs["shelve_length"]

    shelve_height = 2
    if "shelve_height" in kwargs:
        shelve_height = kwargs["shelve_height"]

    shelve_width = 2
    if "shelve_width" in kwargs:
        shelve_width = kwargs["shelve_width"]

    shelve_throughput = 1
    if "shelve_throughput" in kwargs:
        shelve_throughput = kwargs["shelve_throughput"]

    cross_throughput = 5
    if "cross_throughput" in kwargs:
        cross_throughput = kwargs["cross_throughput"]

    seed = 105
    if "seed" in kwargs:
        seed = kwargs["seed"]

    periodicity_lower = 20
    if "periodicity_lower" in kwargs:
        periodicity_lower = kwargs["periodicity_lower"]

    periodicity_upper = 100
    if "periodicity_upper" in kwargs:
        periodicity_upper = kwargs["periodicity_upper"]

    data = pd.DataFrame()
    if "data" in kwargs:
        data = kwargs["data"]

    output = "data/random_package_random_drop.csv"
    if "output" in kwargs:
        output = kwargs["output"]

    name = "random_package_random_drop"
    if "name" in kwargs:
        name = kwargs["name"]

    steps = 10000
    if "steps" in kwargs:
        steps = kwargs["steps"]

    collect = True
    if "collect" in kwargs:
        collect = kwargs["collect"]

    gym = warehouse.RoboticWarehouse(
        robots=robots,
        capacity=capacity,
        spawn=spawn,
        shelve_length=shelve_length,
        shelve_height=shelve_height,
        shelve_width=shelve_width,
        shelve_throughput=shelve_throughput,
        cross_throughput=cross_throughput,
        seed=seed,
        periodicity_lower=periodicity_lower,
        periodicity_upper=periodicity_upper)

    pf = path_finder.Astar(gym)

    gym = data_collection.GymCollect(
        gym=gym,
        data=data,
        output=output,
        name=name,
        steps=steps,
        collect=collect)

    R = [Robot(capacity, pf) for _ in range(robots)]

    render = False
    if "render" in kwargs:
        render = kwargs["render"]

    (robots, packages), _, _, _ = gym.reset()
    curr_step = 0
    print()
    while True:
        if render:
            gym.render()

        instructions = []
        for i, robot in enumerate(R):
            instructions.append(robot(gym, robots[i], packages))

        (robots, packages), _, _, _ = gym.step(instructions)

        if not (curr_step % 1000):
            print("{}/{}    ".format(curr_step, steps), end="\r")

        curr_step += 1


if __name__ == "__main__":
    evaluate(render=True)
