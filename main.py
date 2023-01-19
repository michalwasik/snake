import random

import termcolor
import os
from random import randint, choice


def get_random_cord(height: int, width: int) -> tuple[int, int]:
    return randint(0, height-1), randint(0, width-1)


class Game:
    WIDTH = 30
    HEIGHT = 30

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
        return snake_map

    @property
    def snakes_fields(self):
        field = []
        if self.snakes:
            for snake in self.snakes:
                field += snake.body
        return field

    def _create_fruit(self):
        while True:
            rand_cord = self._get_random_cord()
            if rand_cord not in self.snakes_fields:
                return rand_cord

    def _get_random_cord(self):
        _x, _y = get_random_cord(self.HEIGHT, self.WIDTH)
        return _x , _y

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
                point = x, y = self._get_random_cord()
                if 'snakes' in self.__dict__:
                    if point not in self.snakes_fields:
                        body.append((x, y))
                        break
                body.append(point)
                break
            for _ in range(length - 1):
                choices = self.available_neigh(body[0])
                choices = [point for point in choices if point not in body]
                if choices:
                    body = [choice(choices)] + body
            if len(body) == length:
                return Snake(self, body)

    @staticmethod
    def distance(point1: tuple[int, int], point2: tuple[int, int]) -> int:
        height = abs(point1[0]-point2[0])
        width = abs(point1[1] - point2[1])
        return height + width

    def step(self):
        self.snake_map = self.create_map()
        for snake in self.snakes:
            if snake.move():
                snake.body.append(self.fruit)
                self.fruit = self._create_fruit()
            else:
                direction = snake.set_direction()
                if not direction:
                    self.del_snake(snake)
                else:
                    snake.body = snake.body[1:]
                    snake.body.append(direction)
            snake.snake_on_map()
        self.snake_map[self.fruit[0]][self.fruit[1]] = '*'
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
        current_snakes = self.game.snakes
        taken_fields = []
        for snake in current_snakes:
            taken_fields += snake.body
        head = self.body[-1]
        ways = self.game.available_neigh(head)
        if not ways:
            return None
        can_move = [x for x in ways if x not in taken_fields]
        if not can_move:
            return None
        if not self.game.fruit:
            destination = random.choice(can_move)
            return destination
        else:
            can_move.sort(key=lambda x: self.game.distance(x, self.game.fruit))
            return can_move[0]

    def move(self, grow: bool = False):
        if not self.game.fruit:
            return False
        head = self.body[-1]
        distance = self.game.distance(head, self.game.fruit)
        if distance == 1:
            grow = True
        return grow


while True:
    game = Game(8)
    while True:
        game.step()
