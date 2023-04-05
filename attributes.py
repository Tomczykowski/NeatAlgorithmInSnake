def distance_from_obstacle_up(x, y, snake_body, block_size):
    distance_to_obstacle = y // block_size + 1
    for body in snake_body:
        if x == body[0] and y > body[1]:
            distance = (y - body[1]) // block_size
            if distance < distance_to_obstacle:
                distance_to_obstacle = distance
    return distance_to_obstacle


def distance_from_obstacle_right(x, y, snake_body, block_size, bounds):
    distance_to_obstacle = (bounds - x) // block_size
    for body in snake_body:
        if y == body[1] and x < body[0]:
            distance = (body[0] - x) // block_size
            if distance < distance_to_obstacle:
                distance_to_obstacle = distance
    return distance_to_obstacle


def distance_from_obstacle_down(x, y, snake_body, block_size, bounds):
    distance_to_obstacle = (bounds - y) // block_size
    for body in snake_body:
        if x == body[0] and y < body[1]:
            distance = (body[1] - y) // block_size
            if distance < distance_to_obstacle:
                distance_to_obstacle = distance
    return distance_to_obstacle


def distance_from_obstacle_left(x, y, snake_body, block_size):
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


def make_attributes(game_state, bounds, block_size):
    attributes = []
    head_x = game_state['snake_body'][-1][0]
    head_y = game_state['snake_body'][-1][1]
    food_x = game_state['food'][0]
    food_y = game_state['food'][1]
    attributes.append(distance_from_obstacle_up(head_x, head_y, game_state['snake_body'], block_size))
    attributes.append(distance_from_obstacle_right(head_x, head_y, game_state['snake_body'], bounds[0], block_size))
    attributes.append(distance_from_obstacle_down(head_x, head_y, game_state['snake_body'], bounds[1], block_size))
    attributes.append(distance_from_obstacle_left(head_x, head_y, game_state['snake_body'], block_size))
    attributes.append(distance_to_food(head_y, food_y))
    attributes.append(distance_to_food(head_x, food_x))
    return attributes
