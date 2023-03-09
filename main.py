import copy
import os
import pickle
import pygame
import time
import neat

from model import SVM
from food import Food
from snake import Snake, Direction


class HumanAgent:
    def __init__(self, block_size, bounds):
        self.block_size = block_size
        self.bounds = bounds
        self.data = []

    def act(self, game_state) -> Direction:
        keys = pygame.key.get_pressed()
        action = game_state["snake_direction"]
        if keys[pygame.K_LEFT]:
            action = Direction.LEFT
        elif keys[pygame.K_RIGHT]:
            action = Direction.RIGHT
        elif keys[pygame.K_UP]:
            action = Direction.UP
        elif keys[pygame.K_DOWN]:
            action = Direction.DOWN

        self.data.append((copy.deepcopy(game_state), action))
        return action

    def dump_data(self):
        os.makedirs("data", exist_ok=True)
        current_time = time.strftime('%Y.%m.%d.%H.%M.%S')
        with open(f"data/{current_time}.pickle", 'wb') as f:
            pickle.dump({"block_size": self.block_size,
                         "bounds": self.bounds,
                         "data": self.data[:-10]}, f)  # Last 10 frames are when you press exit, so they are bad, skip


class BehavioralCloningAgent:
    def __init__(self, path):
        self.svm_player = SVM(path)
        self.svm_player.make_attributes()
        self.svm_player.fit()

    def act(self, game_state) -> Direction:
        attributes = self.svm_player.make_attributes_from_game_state(game_state)
        next_move = self.svm_player.game_state_to_data_sample(attributes)
        if next_move == 3:
            return Direction.LEFT
        elif next_move == 1:
            return Direction.RIGHT
        elif next_move == 0:
            return Direction.UP
        elif next_move == 2:
            return Direction.DOWN

    def dump_data(self):
        pass


def distance_from_obstacle_up(x, y, snake_body, block_size=30):
    distance_to_obstacle = y // block_size + 1
    for body in snake_body:
        if x == body[0] and y > body[1]:
            distance = (y - body[1]) // block_size
            if distance < distance_to_obstacle:
                distance_to_obstacle = distance
    return distance_to_obstacle


def distance_from_obstacle_right(x, y, snake_body, block_size=30, bound=300):
    distance_to_obstacle = (bound - x) // block_size
    for body in snake_body:
        if y == body[1] and x < body[0]:
            distance = (body[0] - x) // block_size
            if distance < distance_to_obstacle:
                distance_to_obstacle = distance
    return distance_to_obstacle


def distance_from_obstacle_down(x, y, snake_body, block_size=30, bound=300):
    distance_to_obstacle = (bound - y) // block_size
    for body in snake_body:
        if x == body[0] and y < body[1]:
            distance = (body[1] - y) // block_size
            if distance < distance_to_obstacle:
                distance_to_obstacle = distance
    return distance_to_obstacle


def distance_from_obstacle_left(x, y, snake_body, block_size=30):
    distance_to_obstacle = x // block_size + 1
    for body in snake_body:
        if y == body[1] and x > body[0]:
            distance = (x - body[0]) // block_size
            if distance < distance_to_obstacle:
                distance_to_obstacle = distance
    return distance_to_obstacle


def make_attributes(game_state):
    attributes = []
    head_x = game_state['snake_body'][-1][0]
    head_y = game_state['snake_body'][-1][1]
    attributes.append(head_x)
    attributes.append(head_y)
    attributes.append(game_state['food'][0])
    attributes.append(game_state['food'][1])
    attributes.append(distance_from_obstacle_up(head_x, head_y, game_state['snake_body']))
    attributes.append(distance_from_obstacle_right(head_x, head_y, game_state['snake_body']))
    attributes.append(distance_from_obstacle_down(head_x, head_y, game_state['snake_body']))
    attributes.append(distance_from_obstacle_left(head_x, head_y, game_state['snake_body']))
    return attributes


def fitness(genomes, config):
    networks = []
    ge = []
    snakes = []
    foods = []
    game_states = []

    pygame.init()
    bounds = (300, 300)
    window = pygame.display.set_mode(bounds)
    pygame.display.set_caption("Snake")

    block_size = 30

    for _, genome in genomes:
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(network)
        snakes.append(Snake(block_size, bounds))
        foods.append(Food(block_size, bounds))
        genome.fitness = 0
        ge.append(genome)
        game_states.append(0)

    snakes_alive = len(snakes)

    run = True
    pygame.time.delay(100)
    while snakes_alive != 0 and run:
        snakes_alive = len(snakes)
        pygame.time.delay(20)  # Adjust game speed, decrease to test your agent and model quickly

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for idx, snake in enumerate(snakes):
            game_states[idx] = {"food": (foods[idx].x, foods[idx].y),
                          "snake_body": snake.body,  # The last element is snake's head
                          "snake_direction": snake.direction}

            output = networks[idx].activate(make_attributes(game_states[idx]))
            act = max(output)
            if act == output[0]:
                snake.turn(Direction.UP)
            elif act == output[1]:
                snake.turn(Direction.RIGHT)
            elif act == output[2]:
                snake.turn(Direction.DOWN)
            elif act == output[3]:
                snake.turn(Direction.LEFT)

        for idx, snake in enumerate(snakes):
            snake.move()
            snake.check_for_food(foods[idx])

        for idx, snake in enumerate(snakes):
            if snake.is_wall_collision() or snake.is_tail_collision():
                #pygame.display.update()                 # ???????????????
                snake.alive = False
                snakes_alive -= 1
                ge[idx].fitness = snake.length - 3

        window.fill((0, 0, 0))
        for idx, snake in enumerate(snakes):
            if snake.alive:
                snake.draw(pygame, window)
                foods[idx].draw(pygame, window)
        pygame.display.update()

    pygame.quit()


def main():
    run()


def run():
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         "config_file.txt")

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(fitness, 400)


if __name__ == "__main__":
    main()
