import random


class Food:
    def __init__(self, block_size, bounds, lifetime=1e8):
        self.color = (150, 0, 0)
        self.block_size = block_size
        self.bounds = bounds
        self.x = random.randint(0, (self.bounds[0]) / self.block_size - 1) * self.block_size
        self.y = random.randint(0, (self.bounds[1]) / self.block_size - 1) * self.block_size
        self.lifetime = lifetime
        self.time_left = lifetime

    def draw(self, game, window):
        game.draw.rect(window, self.color, (self.x, self.y, self.block_size, self.block_size))

    def respawn(self, game_state):
        self.time_left = self.lifetime
        blocks_in_x = (self.bounds[0]) / self.block_size
        blocks_in_y = (self.bounds[1]) / self.block_size
        self.x = random.randint(0, blocks_in_x - 1) * self.block_size
        self.y = random.randint(0, blocks_in_y - 1) * self.block_size
        while (self.x, self.y) in game_state['snake_body']:
            self.x = random.randint(0, blocks_in_x - 1) * self.block_size
            self.y = random.randint(0, blocks_in_y - 1) * self.block_size
