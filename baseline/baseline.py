import robotic_warehouse.robotic_warehouse as rw
import time
import numpy
import queue

timestamp = time.time()
gym = rw.RoboticWarehouse(
    robots=10,
    capacity=1,
    spawn=10,
    spawn_rate=0.1,
    shelve_length=8,
    shelve_height=4,
    shelve_width=4,
    shelve_throughput=1,
    cross_throughput=5)
print("Setup Time: {}".format(time.time() - timestamp))


def permute(position: np.array) -> list:
    return [
        position + rw.RoboticWarehouse.UP, position + rw.RoboticWarehouse.DOWN,
        position + rw.RoboticWarehouse.LEFT, position + RoboticWarehouse.RIGHT
    ]


def pickup(position: np.array) -> np.array:
    for pos in permute_positions(position):
        y, x = pos
        if gym.__within_map(y, x) and (gym.map[y][x] == gym.FREE or
                                       (type(gym.map[y][x]) == tuple
                                        and gym.map[y][x][0] == 3)):
            return pos


def a_way(game_map: list, start: np.array, package: np.array,
          end: np.array) -> list:

    current_position = start
    bfs = queue.Queue()
    bfs.put(start)

    pickup_position = pickup(position)
    while bfs and current_position != pickup_position:
        pass
