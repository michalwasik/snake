import termcolor
import os
from random import randint, choice
width = 40
height = 20
area = [[] for _ in range(height)]
for _ in range(width):
    area[0].append('+')
for x in range(1, height - 1):
    area[x].append('+')
    for _ in range(width - 2):
        area[x].append(' ')
    area[x].append('+')
for _ in range(width):
    area[-1].append('+')


def show_game():
    os.system('cls')
    for i in area:
        a = ''.join(i)
        termcolor.cprint(a, 'yellow')


def show_head(direction):
    if direction == [1, 0]:
        return '^'
    elif direction == [-1, 0]:
        return 'v'
    elif direction == [0, -1]:
        return '>'
    else:
        return '<'


def show_snake(show=True):
    for idx, (x, y) in enumerate(snake):
        if idx == 0:
            head = show_head(get_head_dir(snake))
            area[x][y] = head
        else:
            area[x][y] = '0'
    if trace:
        area[trace[0]][trace[1]] = ' '
    if show:
        show_game()


def get_head_dir(snake):
    head_dir = [
        snake[1][0] - snake[0][0],
        snake[1][1] - snake[0][1]
    ]
    return head_dir


def diff_a_b(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def possible_moves(snake):
    head = snake[0]
    all_points = [
        (head[0] + 1, head[1]),
        (head[0] - 1, head[1]),
        (head[0], head[1] + 1),
        (head[0], head[1] - 1)
    ]
    possible_points = [point for point in all_points if area[point[0]][point[1]] not in ['+', '0']]
    return possible_points


def closest_point(goal, points):
    closest = []
    distance = None
    if tuple(goal) in points:
        return goal
    for point in points:
        if not distance:
            distance = diff_a_b(goal, point)
            closest = list(point)
        else:
            curr_dist = diff_a_b(goal, point)
            if curr_dist < distance:
                distance = curr_dist
                closest = list(point)
    return tuple(closest)


def place_fruit():
    while True:
        apple = [randint(1, height - 1), randint(1, width - 1)]
        if area[apple[0]][apple[1]] == ' ':
            area[apple[0]][apple[1]] = '*'
            return apple


snake = [tuple([randint(1, height - 1), randint(1, width - 1)])]
init_tail = choice(possible_moves(snake))
snake.append(init_tail)
fruit = place_fruit()


while True:
    if list(snake[0]) == fruit:
        snake.append(tuple(trace))
        show_snake()
        trace = []
        fruit = place_fruit()
    else:
        options = possible_moves(snake)
        if not options:
            print(f"Sorry, you lost \n Your score:{len(snake)}")
            break
        move = closest_point(fruit, options)
        snake.insert(0, move)
        trace = snake[-1]
        snake = snake[:-1]
        show_snake()
