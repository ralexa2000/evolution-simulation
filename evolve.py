import matplotlib.pyplot as plt

from space import Space


SPACE_SIZE = 100
N_DAYS = 10000
PAUSE = 0.01

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
