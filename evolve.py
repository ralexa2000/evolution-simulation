from collections import defaultdict
import matplotlib.pyplot as plt
import random


SPACE_SIZE = 100
N_DAYS = 10000
PAUSE = 0.01
ALL_DIRECTIONS = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

POSSIBLE_OBJECTS = {
    'creature': {
        'color': '#A52A2A'
    },
    'food': {
        'color': '#ADFF2F'
    }
}


class Object:
    def __init__(self, object_type):
        if object_type not in POSSIBLE_OBJECTS:
            raise TypeError('Object type {} is not implemented'.format(object_type))
        
        self.type = object_type
        self.color = POSSIBLE_OBJECTS[object_type]['color']
        self.moved_in_current_round = False


class Space:
    def __init__(self, size):
        self.size = size
        self.objects = [[None]*size for _ in range(size)]
        self.cnt_objects = defaultdict(int)

    def add_object(self, x, y, object_type):
        self.objects[x][y] = Object(object_type)
        self.cnt_objects[object_type] += 1

    def plot_objects(self):
        x_coordinates = []
        y_coordinates = []
        colors = []
        for x in range(self.size):
            for y in range(self.size):
                if self.objects[x][y]:
                    x_coordinates.append(x)
                    y_coordinates.append(y)
                    colors.append(self.objects[x][y].color)
        plt.scatter(x_coordinates, y_coordinates, c=colors)

    def move_creatures(self):
        self.clean_moved_in_current_round()
        for x in range(self.size):
            for y in range(self.size):
                if self.objects[x][y] and self.objects[x][y].type == 'creature' and \
                        not self.objects[x][y].moved_in_current_round:
                    for x_direction, y_direction in ALL_DIRECTIONS:
                        if self.is_possible_coordinates(x + x_direction, y + y_direction) and \
                                self.objects[x + x_direction][y + y_direction] and \
                                self.objects[x + x_direction][y + y_direction].type == 'food':
                            self.objects[x + x_direction][y + y_direction] = self.objects[x][y]
                            self.objects[x + x_direction][y + y_direction].moved_in_current_round = True
                            self.objects[x][y] = None
                            self.cnt_objects['food'] -= 1
                            break
                    else:
                        x_direction, y_direction = random.choice(self.get_possible_directions(x, y))
                        if x_direction != 0 or y_direction != 0:
                            self.objects[x + x_direction][y + y_direction] = self.objects[x][y]
                            self.objects[x + x_direction][y + y_direction].moved_in_current_round = True
                            self.objects[x][y] = None

    def clean_moved_in_current_round(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.objects[x][y]:
                    self.objects[x][y].moved_in_current_round = False

    def get_possible_directions(self, x, y):
        possible_directions = []
        for x_direction, y_direction in ALL_DIRECTIONS:
            if self.is_possible_coordinates(x + x_direction, y + y_direction) and \
                    (x_direction == 0 and y_direction == 0 or not self.objects[x + x_direction][y + y_direction]):
                possible_directions.append((x_direction, y_direction))
        return possible_directions

    def is_possible_coordinates(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

    def get_vacant_position(self):
        x, y = None, None
        while x is None or y is None or self.objects[x][y]:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
        return x, y


plt.ion()
plt.figure(figsize=(10, 10))

space = Space(SPACE_SIZE)

# fill food
for i in range(SPACE_SIZE * 3):
    x, y = space.get_vacant_position()
    space.add_object(x, y, 'food')

# fill creatures
for i in range(SPACE_SIZE // 10):
    x, y = space.get_vacant_position()
    space.add_object(x, y, 'creature')

for day in range(N_DAYS):
    if day // 5 == 0:
        x, y = space.get_vacant_position()
        space.add_object(x, y, 'food')

    space.move_creatures()
    space.plot_objects()

    print(space.cnt_objects)

    plt.xlim(0, SPACE_SIZE)
    plt.ylim(0, SPACE_SIZE)
    plt.pause(PAUSE)
    plt.clf()
