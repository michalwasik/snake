import random

import termcolor
import os
from random import randint, choice
# width = 40
# height = 20
# area = [[] for _ in range(height)]
# for _ in range(width):
#     area[0].append('+')
# for x in range(1, height - 1):
#     area[x].append('+')
#     for _ in range(width - 2):
#         area[x].append(' ')
#     area[x].append('+')
# for _ in range(width):
#     area[-1].append('+')
#
#
# def show_game():
#     os.system('cls')
#     for i in area:
#         a = ''.join(i)
#         termcolor.cprint(a, 'yellow')
#
#
# def show_head(direction):
#     if direction == [1, 0]:
#         return '^'
#     elif direction == [-1, 0]:
#         return 'v'
#     elif direction == [0, -1]:
#         return '>'
#     else:
#         return '<'
#
#
# def show_snake(show=True):
#     for idx, (x, y) in enumerate(snake):
#         if idx == 0:
#             head = show_head(get_head_dir(snake))
#             area[x][y] = head
#         else:
#             area[x][y] = '0'
#     if trace:
#         area[trace[0]][trace[1]] = ' '
#     if show:
#         show_game()
#
#
# def get_head_dir(snake):
#     head_dir = [
#         snake[1][0] - snake[0][0],
#         snake[1][1] - snake[0][1]
#     ]
#     return head_dir
#
#
# def diff_a_b(point1, point2):
#     return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])
#
#
# def possible_moves(snake):
#     head = snake[0]
#     all_points = [
#         (head[0] + 1, head[1]),
#         (head[0] - 1, head[1]),
#         (head[0], head[1] + 1),
#         (head[0], head[1] - 1)
#     ]
#     possible_points = [point for point in all_points if area[point[0]][point[1]] not in ['+', '0']]
#     return possible_points
#
#
# def closest_point(goal, points):
#     closest = []
#     distance = None
#     if tuple(goal) in points:
#         return goal
#     for point in points:
#         if not distance:
#             distance = diff_a_b(goal, point)
#             closest = list(point)
#         else:
#             curr_dist = diff_a_b(goal, point)
#             if curr_dist < distance:
#                 distance = curr_dist
#                 closest = list(point)
#     return tuple(closest)
#
#
# def place_fruit():
#     while True:
#         apple = [randint(1, height - 1), randint(1, width - 1)]
#         if area[apple[0]][apple[1]] == ' ':
#             area[apple[0]][apple[1]] = '*'
#             return apple
#
#
# snake = [tuple([randint(1, height - 1), randint(1, width - 1)])]
# init_tail = choice(possible_moves(snake))
# snake.append(init_tail)
# fruit = place_fruit()


# while True:
#     if list(snake[0]) == fruit:
#         snake.append(tuple(trace))
#         show_snake()
#         trace = []
#         fruit = place_fruit()
#     else:
#         options = possible_moves(snake)
#         if not options:
#             print(f"Sorry, you lost \n Your score:{len(snake)}")
#             break
#         move = closest_point(fruit, options)
#         snake.insert(0, move)
#         trace = snake[-1]
#         snake = snake[:-1]
#         show_snake()


#
# width = 40
# height = 20
# area = [[] for _ in range(height)]
# for _ in range(width):
#     area[0].append('+')
# for x in range(1, height - 1):
#     area[x].append('+')
#     for _ in range(width - 2):
#         area[x].append(' ')
#     area[x].append('+')
# for _ in range(width):
#     area[-1].append('+')

from random import choice


def get_random_cord(height: int, width: int) -> tuple[int, int]:
    return randint(0, height), randint(0, width)


class Game:
    WIDTH = 50
    HEIGHT = 50

    def __init__(self, n_snakes: int, snake_map: list[list[str]] = None):
        if not snake_map:
            self.snake_map = self.create_map()
        else:
            self.snake_map = snake_map
        self.n_snakes = n_snakes
        self.snakes = [self.create_snake(4) for _ in range(n_snakes)]
        self.fruit = self._create_fruit()


    @classmethod
    def create_map(cls):
        snake_map: list[list[str]] = [[' ' for _ in range(cls.WIDTH)] for _ in range(cls.HEIGHT)]
        for idx, row in enumerate(snake_map):
            snake_map[idx] = ['+'] + row + ['+']
        snake_map = ['+' * (cls.WIDTH + 2)] + snake_map + ['+' * (cls.WIDTH + 2)]
        return snake_map

    def _create_fruit(self):
        while True:
            rand_cort = self._get_random_cord()
            if self.snake_map[rand_cort[0]][rand_cort[1]] == ' ':
                self.snake_map[rand_cort[0]][rand_cort[1]] = '*'
                return rand_cort

    def _get_random_cord(self):
        _y, _x = get_random_cord(self.HEIGHT, self.WIDTH)
        return _y + 1, _x + 1

    def available_neigh(self, point: tuple[int, int]):
        xs = [(point[0] - 1, point[1]), (point[0] + 1, point[1])]
        ys = [(point[0], point[1] - 1), (point[0], point[1] + 1)]
        for x in xs:
            if not 0 <= x[0] < len(self.snake_map):
                xs.remove(x)
            elif self.snake_map[x[0]][x[1]] != ' ':
                xs.remove(x)
        for y in ys:
            if not 0 <= y[1] < len(self.snake_map[0]):
                ys.remove(y)
            elif self.snake_map[y[0]][y[1]] != ' ':
                ys.remove(y)
        return xs + ys

    def create_snake(self, length: int = 3) -> 'Snake':
        while True:
            body = []
            while True:
                y, x = self._get_random_cord()
                # print(self.snake_map)
                # print(y, x)
                # print(len(self.snake_map[0]), len(self.snake_map))
                if self.snake_map[x][y] == ' ':
                    body.append((x, y))
                    break
            for _ in range(length - 1):
                choices = self.available_neigh(body[0])
                choices = [point for point in choices if point not in body]
                if choices:
                    body = [choice(choices)] + body
            if len(body) == length:
                return Snake(self, body)

    def step(self):
        print('make one step')
        for snake in self.snakes:
            if snake.move():
                self.snake_map[self.fruit[0]][self.fruit[1]] = snake.set_direction()
                snake.body.append(self.fruit)
                self.fruit = None
            else:
                direction = snake.set_direction()
                print(direction)
                if not direction:
                    for coord in snake.body:
                        self.snake_map[coord[0]][coord[1]] = ' '
                    self.snakes.remove(snake)
                else:
                    self.snake_map[snake.body[0][0]][snake.body[0][1]] = ' '
                    snake.body = snake.body[1:]
                    change = snake.DIR_TO_DELTA[direction]
                    new_point = (snake.body[-1][0] + change[0], snake.body[-1][1] + change[1])
                    self.snake_map[new_point[0]][new_point[1]] = snake.set_direction()
                    snake.body.append(new_point)
        if not self.fruit:
            self.fruit = self._create_fruit()
        self._print_map()

    def _print_map(self):
        os.system('cls')
        for i in self.snake_map:
            a = ''.join(i)
            termcolor.cprint(a, 'yellow')


class Snake:
    DIRECTIONS = ('<', '>', 'V', '^')
    DIR_TO_DELTA = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'V': (1, 0)}

    def __init__(self, game: 'Game', body):
        self.game = game
        self.body = body

    @property
    def direction(self) -> tuple[int, int]:
        head = self.body[-1]
        behind_head = self.body[-2]
        return head[0] - behind_head[0], head[1] - behind_head[1]

    def set_direction(self):
        head = self.body[-1]
        if head[0] != self.game.fruit[0]:
            if head[0] > self.game.fruit[0]:
                dream = '^'
            else:
                dream = 'V'
        else:
            if head[1] > self.game.fruit[1]:
                dream = '<'
            else:
                dream = '>'
        ways = self.game.available_neigh(head)
        if not ways:
            return None
        if dream in ways:
            return dream
        else:
            return random.choice(ways)

    def move(self, grow: bool = False):
        head = self.body[-1]
        distance = abs(sum(map(lambda x, y: x - y, head, self.game.fruit)))
        if distance == 1:
            grow = True
        return grow


while True:
    game = Game(4)
    print(game.fruit)
    for snake in game.snakes:
        print(snake.body)
    print(game.snake_map)
    while True:
        game.step()
