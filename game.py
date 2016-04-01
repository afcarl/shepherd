import time
import random
import math
import sys
import Tkinter

MAX_TIME = 10 * 60
SHEEP_SPEED = 0.33
SHEPHERD_H_SPEED = 2.5
SHEPHERD_UP_TIME = 1
SHEPHERD_DOWN_TIME = 1

GOAT_CIRCLE_RADIUS = 5

STAGE_TIME = 20

ARENA_WIDTH = 20
ARENA_HEIGHT = 20
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
        dx  = self.dx * math.cos(theta) - self.dy * math.sin(theta)
        dy = self.dx * math.sin(theta) + self.dy * math.cos(theta)
        norm = math.sqrt(dx * dx + dy * dy)
        self.dx, self.dy = dx / norm, dy / norm
        print math.sqrt(self.dx ** 2 + self.dy ** 2)
    def turn_random(self):
        vx, vy = random.random() - 0.5, random.random() - 0.5
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
        super(Shepherd, self).__init__(x, y, dx, dy, SHEPHERD_H_SPEED)
        self.radius = SHEPHERD_RADIUS
    def collision(self):
        pass

class Arena(object):
    def __init__(self):
        self.entries = []
        self.goats = []
        self.sheeps = []
        self.shepherd = None
        self.n_home_sheep = 0
        self.n_wild_sheep = 0
        self.groud_sheep = 0
        self.stage = 0
        self.time = 0

    def handle_collision(self):
        for i in xrange(len(self.entries)):
            for j in xrange(i + 1, len(self.entries)):
                if (self.entries[i].x - self.entries[j].x) ** 2 + (self.entries[i].y - self.entries[j].y) ** 2 <= (self.entries[i].radius + self.entries[j].radius) ** 2:
                    self.entries[i].collision()
                    self.entries[j].collision()
    def time_fly(self, seconds):
        self.time += seconds
        stage = int(self.time / STAGE_TIME)
        for entry in self.entries:
            entry.move(seconds)
        self.handle_collision()
        print seconds
        print SHEEP_SPEED / GOAT_CIRCLE_RADIUS * seconds
        for goat in self.goats:
            goat.turn_angle(SHEEP_SPEED / GOAT_CIRCLE_RADIUS * seconds)
        if stage > self.stage:
            self.stage = stage
            for sheep in self.sheeps:
                sheep.turn_180()

class Monitor(object):
    def __init__(self, scale=50):
        self.scale = scale
        self.root = Tkinter.Tk()
        scale = self.scale
        frame = Tkinter.Frame(self.root, width=ARENA_WIDTH * scale, height=ARENA_HEIGHT * scale)
        frame.pack()
        self.canvas = Tkinter.Canvas(frame, width=ARENA_WIDTH * scale, height=ARENA_HEIGHT * scale)
        self.canvas.pack()

    def update(self, arena):
        self.canvas.delete(Tkinter.ALL)
        s = self.scale
        d = ANIMAL_RADIUS * s 
        for goat in arena.goats:
            self.canvas.create_oval(s * goat.x - d, s * goat.y - d, s * goat.x + d, s * goat.y + d, fill='red')
        for sheep in arena.sheeps:
            self.canvas.create_oval(s * sheep.x - d, s * sheep.y - d, s * sheep.x + d, s * sheep.y + d, fill='green')
        shepherd = arena.shepherd
        self.canvas.create_oval(s * shepherd.x - d, s * shepherd.y - d, s * shepherd.x + d, s * shepherd.y + d, fill='black')

        self.root.update()

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

    start_time = time.time()
    now = start_time
    while True:
        previous = now
        now = time.time()
        time.sleep(0.0001)
        if now - start_time >= MAX_TIME:
            sys.exit(0)
        delta_time = now - previous
        arena.time_fly(delta_time * 10)
        monitor.update(arena)
