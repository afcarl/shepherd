import time
import random
import math
import sys
import Tkinter

MAX_TIME = 10 * 60
SHEEP_SPEED = 0.33
SHEPHERD_H_SPEED = 1.5
SHEPHERD_UP_TIME = 1
SHEPHERD_DOWN_TIME = 1

ARENA_WIDTH = 200
ARENA_HEIGHT = 200
half_sqrt_2 = 0.5 * math.sqrt(2)

ANIMAL_RADIUS = 0.3
SHEPHERD_RADIUS = 0.5

NUM_SHEEP = 10
NUM_GOAT = 4
class Entry(object):
    half_sqrt_2 = 0.5 * math.sqrt(2)
    def __init__(self, x, y, dx, dy, speed):
        self.x, self.y = x, y
        norm = math.sqrt(dx * dx + dy * dy)
        self.dx, self.dy = dx / norm, dy / norm
        self.speed = speed
    def turn_45(self):
        self.dx = self.dx * half_sqrt_2 - self.dy * half_sqrt_2
        self.vy = self.dx * half_sqrt_2 + self.dy * half_sqrt_2
    def turn_180(self):
        self.dx, self.dy = -self.dx, -self.dy
    def turn_angle(self, theta):
        self.dx  = self.dx * math.cos(theta) - self.dy * math.sin(theta)
        self.dy = self.dx * math.sin(theta) + self.dy * math.cos(theta)
    def turn_random(self):
        vx, vy = random.rand() - 0.5, random.rand() - 0.5
        norm = math.sqrt(vx * vx + vy * vy)
        self.dx, self.dy = vx / norm, vy / norm

    def move(self, time):
        self.x, self.y = self.x + self.dx * self.speed * time, self.y + self.dy * self.speed * time

    def collision(self):
        raise Exception('Not Implement')

class Sheep(Entry):
    def __init__(self, x, y, dx, dy):
        super(Sheep, self).__init__(x, y, dx, dy, SHEEP_SPEED)
        self.radius = ANIMAL_RADIUS
    def collision(self):
        self.turn_180()

class Goat(Entry):
    def __init__(self, x, y, dx, dy):
        super(Goat, self).__init__(x, y, dx, dy, SHEEP_SPEED)
        self.radius = ANIMAL_RADIUS
    def collision(self):
        pass

class Shepherd(Entry):
    def __init__(self, x, y, dx, dy):
        super(Entry, self).__init__(x, y, dx, dy, SHEPHERD_H_SPEED)
        self.radius = SHEPHERD_RADIUS
    def collision(self):
        pass

class Arena(object):
    def __init__(self):
        self.entries = []
        self.goats = []
        self.sheep = []
        self.shepherd = None
        self.n_home_sheep = 0
        self.n_wild_sheep = 0
        self.groud_sheep = 0

    def handle_collision(self):
        for i in xrange(len(self.entries)):
            for j in xrange(i + 1, len(self.entries)):
                if (self.entries[i].x - self.entries[j]) ** 2 + (self.entries[i].y - self.entries[j].y) ** 2 <= (self.entries[i].radius + self.entries[j].radius) ** 2:
                    self.entries[i].collision()
                    self.entries[j].collision()
    def time_fly(self, seconds):
        for entry in self.entries:
            entry.move(seconds)
        self.handle_collision()

class Monitor(object):
    def __init__(self, scale=5):
        self.root = Tkinter.Tk()
        self.scale = scale
        self.canvas = Tkinter.Canvas(self.root, width=ARENA_WIDTH * scale, height=ARENA_HEIGHT * scale)
        self.root.mainloop()

    def update(self, arena):
        self.canvas.delete(Tkinter.ALL)
        for goat in self.arena.goats:
            self.canvas.create_oval(goat.x - ANIMAL_RADIUS, goat.y - ANIMAL_RADIUS, goat.x + ANIMAL_RADIUS, goat.y + ANIMAL_RADIUS)
        for sheep in self.arena.sheeps:
            self.canvas.create_oval(sheep.x - ANIMAL_RADIUS, sheep.y - ANIMAL_RADIUS, sheep.x + ANIMAL_RADIUS, sheep.y + ANIMAL_RADIUS)
        shepherd = self.arena.shepherd
        self.canvas.create_oval(shepherd.x - SHEPHERD_RADIUS, shepherd.y - SHEPHERD_RADIUS, shepherd.x + SHEPHERD_RADIUS, shepherd.y + SHEPHERD_RADIUS)


if __name__ == '__main__':
    arena = Arena()
    for i in xrange(NUM_SHEEP):
        sheep = Sheep(random.random() * ARENA_WIDTH, random.random() * ARENA_HEIGHT, 1, 1)
        sheep.turn_random()
        arena.entries.append(sheep)
        arena.sheeps.append(sheep)
    for i in xrange(NUM_GOAT):
        goat = Goat(random.random() * ARENA_WIDTH, random.random() * ARENA_HEIGHT, 1, 1)
        goat.turn_random()
        arena.entries.append(goat)
        arena.goats.append(goat)
    shepherd = Shepherd(random.random() * ARENA_WIDTH, random.random() * ARENA_HEIGHT, 1, 1)
    shepherd.turn_random()
    arena.entries.append(shepherd)
    arena.shepherd = shepherd
    monitor = Monitor()
    monitor.update(arena)
    start_time = time.clock()
    now = start_time
    while True:
        previous = now
        time.sleep(1.0)
        now = time.clock()
        if now - start_time >= MAX_TIME:
            sys.exit(0)
        arena.time_fly(now - previous)
        monitor.update(arena)