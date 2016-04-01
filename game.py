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
SHEEP_START_CIRCLE_RADIUS = 1
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
    def __init__(self, x, y, dx, dy, speed):
        self.x, self.y = x, y
        norm = math.sqrt(dx * dx + dy * dy)
        self.dx, self.dy = dx / norm, dy / norm
        self.speed = speed
    def turn_45(self):
        self.dx = self.dx * half_sqrt_2 - self.dy * half_sqrt_2
        self.vy = self.dx * half_sqrt_2 + self.dy * half_sqrt_2
        self.turn_angle(math.pi / 4)
    def turn_180(self):
        self.turn_angle(math.pi)
    def turn_angle(self, theta, sigma=0.00001):
        theta += random.gauss(0, sigma)
        dx = self.dx * math.cos(theta) - self.dy * math.sin(theta)
        dy = self.dx * math.sin(theta) + self.dy * math.cos(theta)
        norm = math.sqrt(dx * dx + dy * dy)
        self.dx, self.dy = dx / norm, dy / norm
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
    def action(self, arena):
        self.turn_random()
        self.x += 0.00005

class Arena(object):
    IN_ARENA = 0
    OUT_HOME = 1
    OUT_OTHER = 2
    IN_HOME = 3
    OUT_WILD = 4
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
    def out_of_arena(self, entry):
        if entry.y > ARENA_HEIGHT:
            return Arena.OUT_WILD
        if entry.y < 0:
            return Arena.IN_HOME
        if entry.x > ARENA_WIDTH or entry.x < 0:
            return Arena.OUT_OTHER
        return Arena.IN_ARENA

    def handle_out(self):
        no_out = True
        for i, e in enumerate(self.entries):
            if self.out_of_arena(e) != Arena.IN_ARENA:
                self.entries.pop(i)
                no_out = False
        if no_out:
            return
        for i, e in enumerate(self.sheeps):
            status = self.out_of_arena(e)
            if status != Arena.IN_ARENA:
                self.sheeps.pop(i)
                if status == Arena.OUT_WILD:
                    self.n_wild_sheep += 1
                elif status == Arena.IN_HOME:
                    self.n_home_sheep += 1
    def handle_collision(self):
        for i in xrange(len(self.entries)):
            for j in xrange(i + 1, len(self.entries)):
                if (self.entries[i].x - self.entries[j].x) ** 2 + (self.entries[i].y - self.entries[j].y) ** 2 <= (self.entries[i].radius + self.entries[j].radius) ** 2:
                    ei, ej = self.entries[i], self.entries[j]
                    if (ej.x - ei.x) * ei.dx + (ej.y - ei.y) * ei.dy > 0:
                        self.entries[i].collision()
                    if (ei.x - ej.x) * ej.dx + (ei.y - ej.y) * ej.dy > 0:
                        self.entries[j].collision()
    def time_fly(self, seconds):
        self.time += seconds
        stage = int(self.time / STAGE_TIME)
        for entry in self.entries:
            entry.move(seconds)
        self.handle_out()
        self.handle_collision()
        for goat in self.goats:
            goat.turn_angle(SHEEP_SPEED / GOAT_CIRCLE_RADIUS * seconds)
        if stage > self.stage:
            self.stage = stage
            for sheep in self.sheeps:
                sheep.turn_180()
        self.shepherd.action(self)

class Monitor(object):
    def __init__(self, scale=30):
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
        self.canvas.create_line(0, 3, ARENA_WIDTH * s, 3, fill='green', width=3)
        self.canvas.create_line(0, ARENA_HEIGHT * s + 1, ARENA_WIDTH * s, ARENA_HEIGHT * s + 1, fill='red', width=3)
        self.canvas.create_line(0, ARENA_HEIGHT * s / 2, ARENA_WIDTH * s, ARENA_HEIGHT * s / 2, fill='white', width=3)
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
        angle = 2 * math.pi / NUM_SHEEP * i
        dx = SHEEP_START_CIRCLE_RADIUS * math.cos(angle)
        dy = SHEEP_START_CIRCLE_RADIUS * math.sin(angle)
        x, y = ARENA_WIDTH / 2 + dx, ARENA_WIDTH / 2 + dy
        sheep = Sheep(x, y, dx, dy)
        arena.entries.append(sheep)
        arena.sheeps.append(sheep)
    for i in xrange(NUM_GOAT):
        angle = 2 * math.pi / NUM_GOAT * i
        dx = GOAT_CIRCLE_RADIUS * math.cos(angle)
        dy = GOAT_CIRCLE_RADIUS * math.sin(angle)
        goat = Goat(ARENA_WIDTH / 2 + dx, ARENA_WIDTH / 2 + dy, -dy, dx)
        arena.entries.append(goat)
        arena.goats.append(goat)
    shepherd = Shepherd(0, 0.5 * ARENA_HEIGHT, 1, 0)
    shepherd.turn_random()
    arena.entries.append(shepherd)
    arena.shepherd = shepherd
    monitor = Monitor()
    monitor.update(arena)

    start_time = time.time()
    now = start_time
    watch_speed = 20.0
    while True:
        previous = now
        now = time.time()
        if (now - start_time) * watch_speed >= MAX_TIME:
            sys.exit(0)
        delta_time = now - previous
        arena.time_fly(delta_time * watch_speed)
        monitor.update(arena)
