import pygame
import neat

from food import Food
from snake import Snake, Direction
from fitness_function import make_attributes


bounds = (300, 300)
block_size = 30


def fitness(genomes, config):
    networks, ge, snakes, foods, game_states, best_score, dead_road = [], [], [], [], [], [], []

    pygame.init()
    window = pygame.display.set_mode(bounds)
    pygame.display.set_caption("Snake")

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
        pygame.time.delay(10)  # Adjust game speed, decrease to test your model quickly

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for idx, snake in enumerate(snakes):
            game_states[idx] = {"food": (foods[idx].x, foods[idx].y),
                                "snake_body": snake.body,  # The last element is snake's head
                                "snake_direction": snake.direction}

            output = networks[idx].activate(make_attributes(game_states[idx], bounds, block_size))
            act = max(output)
            if act == output[0]:
                snake.turn(Direction.UP)
            elif act == output[1]:
                snake.turn(Direction.RIGHT)
            elif act == output[2]:
                snake.turn(Direction.DOWN)
            elif act == output[3]:
                snake.turn(Direction.LEFT)

            snake.move()
            if snake.check_for_food(foods[idx], game_states[idx]):
                dead_road[idx] = bounds[0]*bounds[1]/block_size**2
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
                ge[idx].fitness += 0.01

        window.fill((0, 0, 0))

        for idx, snake in enumerate(snakes):
            if snake.alive:
                snake.draw(pygame, window)
                foods[idx].draw(pygame, window)
        pygame.display.update()

    pygame.quit()
    print(max(best_score))


def main():
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         "config_file.txt")

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(fitness, 1000)
    print(winner)


if __name__ == "__main__":
    main()
