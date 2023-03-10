import copy
import os
import pickle
import pygame
import time
import neat

from model import SVM
from food import Food
from snake import Snake, Direction


def distance_from_obstacle_up(x, y, snake_body, block_size=30):
    distance_to_obstacle = y // block_size + 1
    for body in snake_body:
        if x == body[0] and y > body[1]:
            distance = (y - body[1]) // block_size
            if distance < distance_to_obstacle:
                distance_to_obstacle = distance
    return distance_to_obstacle


def distance_from_obstacle_right(x, y, snake_body, block_size=30, bound=900):
    distance_to_obstacle = (bound - x) // block_size
    for body in snake_body:
        if y == body[1] and x < body[0]:
            distance = (body[0] - x) // block_size
            if distance < distance_to_obstacle:
                distance_to_obstacle = distance
    return distance_to_obstacle


def distance_from_obstacle_down(x, y, snake_body, block_size=30, bound=900):
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


def distance_to_food(head, food):
    distance = food - head
    return distance



def make_attributes(game_state):
    attributes = []
    head_x = game_state['snake_body'][-1][0]
    head_y = game_state['snake_body'][-1][1]
    food_x = game_state['food'][0]
    food_y = game_state['food'][1]
    attributes.append(distance_from_obstacle_up(head_x, head_y, game_state['snake_body']))
    attributes.append(distance_from_obstacle_right(head_x, head_y, game_state['snake_body']))
    attributes.append(distance_from_obstacle_down(head_x, head_y, game_state['snake_body']))
    attributes.append(distance_from_obstacle_left(head_x, head_y, game_state['snake_body']))
    attributes.append(distance_to_food(head_y, food_y))
    attributes.append(distance_to_food(head_x, food_x))
    return attributes


def fitness(genomes, config):
    networks = []
    ge = []
    snakes = []
    foods = []
    game_states = []
    best_score = []
    dead_road = []

    pygame.init()
    bounds = (600, 600)
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
        best_score.append(0)
        dead_road.append(bounds[0]**2/block_size**2)

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
            if snake.check_for_food(foods[idx], game_states[idx]) == 1.001:
                dead_road[idx] = bounds[0]**2/block_size**2
            dead_road[idx] -= 1
            if snake.is_wall_collision() or snake.is_tail_collision() or dead_road[idx] <= 0:
                if dead_road[idx] == 0:
                    ge[idx].fitness -= bounds[0]**2/block_size**2 * 0.001
                snake.alive = False
                snakes_alive -= 1
                ge[idx].fitness += snake.length - 3
                best_score[idx] = snake.length - 3
                snakes.pop(idx)
                foods.pop(idx)
                networks.pop(idx)
                ge.pop(idx)
                game_states.pop(idx)
                dead_road.pop(idx)
            else:
                ge[idx].fitness += 0.001

        window.fill((0, 0, 0))
        for idx, snake in enumerate(snakes):
            if snake.alive:
                snake.draw(pygame, window)
                foods[idx].draw(pygame, window)
        pygame.display.update()

    pygame.quit()
    print(max(best_score))


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

    winner = p.run(fitness, 1000)


if __name__ == "__main__":
    main()
