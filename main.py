import random

import termcolor
import os
from random import randint, choice


def get_random_cord(height: int, width: int) -> tuple[int, int]:
    return randint(0, height), randint(0, width)


class Game:
    WIDTH = 40
    HEIGHT = 40

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
        # print(self.snakes)
        for snake in self.snakes:
            # print(snake)
            if snake.move():
                self.snake_map[self.fruit[0]][self.fruit[1]] = snake.set_direction()
                self.snake_map[snake.body[-1][0]][snake.body[-1][1]] = '0'
                snake.body.append(self.fruit)
                self.fruit = None
            else:
                direction = snake.set_direction()
                if not direction:
                    self.del_snake(snake)
                else:
                    self.snake_map[snake.body[0][0]][snake.body[0][1]] = ' '
                    snake.body = snake.body[1:]
                    change = snake.DIR_TO_DELTA[direction]
                    new_point = (snake.body[-1][0] + change[0], snake.body[-1][1] + change[1])
                    if self.snake_map[new_point[0]][new_point[1]] != ' ':
                        self.del_snake(snake)
                    else:
                        self.snake_map[snake.body[-1][0]][snake.body[-1][1]] = '0'
                        # print(f'{new_point= }')
                        # print(f'{direction= }')
                        # print(f'{self.snake_map[new_point[0]][new_point[1]] = }')
                        self.snake_map[new_point[0]][new_point[1]] = direction
                        snake.body.append(new_point)
        if not self.fruit:
            self.fruit = self._create_fruit()
        self._print_map()
        if len(self.snakes) == 0:
            exit()

    def _print_map(self):
        os.system('cls')
        for i in self.snake_map:
            a = ''.join(i)
            termcolor.cprint(a, 'yellow')

    def del_snake(self, snake: 'Snake'):
        for coord in snake.body:
            self.snake_map[coord[0]][coord[1]] = ' '
        self.snakes.remove(snake)


class Snake:
    DIRECTIONS = ('<', '>', 'V', '^')
    DIR_TO_DELTA = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'V': (1, 0)}

    def __init__(self, game: 'Game', body):
        self.game = game
        self.body = body
        self.snake_on_map()

    @property
    def direction(self) -> tuple[int, int]:
        head = self.body[-1]
        behind_head = self.body[-2]
        return head[0] - behind_head[0], head[1] - behind_head[1]

    def snake_on_map(self):
        destination = self.direction
        head_shape = '>'
        for key, value in self.DIR_TO_DELTA.items():
            if value == destination:
                head_shape = key
        for cords in self.body[:-1]:
            self.game.snake_map[cords[0]][cords[1]] = '0'
        self.game.snake_map[self.body[-1][0]][self.body[-1][1]] = head_shape

    def set_direction(self):
        head = self.body[-1]
        ways = self.game.available_neigh(head)
        if not ways:
            return None
        poss_neigh = [(x-head[0], y-head[1]) for x, y in ways]
        if not self.game.fruit:
            # print(poss_neigh)
            destination = random.choice(poss_neigh)
            for key, value in self.DIR_TO_DELTA.items():
                if value == destination:
                    return key
        elif head[0] != self.game.fruit[0]:
            if head[0] > self.game.fruit[0]:
                dream = '^'
            else:
                dream = 'V'
        else:
            if head[1] > self.game.fruit[1]:
                dream = '<'
            else:
                dream = '>'
        shift = self.DIR_TO_DELTA[dream]
        # print(shift)
        if shift in poss_neigh:
            return dream
        else:
            destination = random.choice(poss_neigh)
            for key, value in self.DIR_TO_DELTA.items():
                if value == destination:
                    return key

    def move(self, grow: bool = False):
        if not self.game.fruit:
            return False
        head = self.body[-1]
        # print(f'{self.game.fruit =}')
        # print(f'{self.body =}')
        distance = abs(sum(map(lambda x, y: x - y, head, self.game.fruit)))
        if distance == 1:
            grow = True
        return grow


while True:
    game = Game(4)
    while True:
        game.step()
