import pygame as pg
import math
from pygame.math import Vector2 as vect2
import keyboard

pg.init()

w = pg.display.set_mode((700, 600))
pg.display.set_caption("Verlet Physics")

Running = True
clock = pg.time.Clock()
fps = 60
obj = []


class obj_:
    def __init__(self, pos_current, pos_old, accel):
        self.pos_current: vect2 = pos_current
        self.pos_old: vect2 = pos_old
        self.accel: vect2 = accel

    def update(self, gravity, dt):
        self.accel += gravity
        self.vel = self.pos_current - self.pos_old
        self.pos_old = self.pos_current
        self.pos_current = self.pos_current + self.vel + self.accel * (dt ** 2)
        self.accel = vect2()

    def accelerate(self, acc):
        self.accel += acc


ball1 = obj_(vect2(700 / 2, 600 / 2), vect2(700 / 2, 600 / 2), vect2(0, 0))
ball2 = obj_(vect2(700 / 2,600 / 2 + 50), vect2(700 / 2,600 / 2 + 50), vect2(0, 0))
obj.append(ball1)
obj.append(ball2)

class Solver:
    def __init__(self, gravity):
        self.gravity: vect2 = gravity

    def update(self, dt):
        self.sub_steps = 2
        self.sub_dt = dt / float(self.sub_steps)
        

        for i in range(self.sub_steps, 0, -1):
            self.apply_gravity(dt)
            self.apply_cons()
            self.solve_collision()
            self.update_pos(dt)

    def update_pos(self, dt):
        for objs in obj:
            objs.update(self.gravity, dt)

    def apply_gravity(self, dt):
        global w
        for objs in obj:
            pg.draw.circle(w, "#03a66b", objs.pos_current, 10.0, 0)
            
	
    def apply_cons(self):
        self.position = vect2(700 /2, 600 /2)
        self.radius = 200
        
        for objs in obj:
            self.to_obj = objs.pos_current - self.position
            self.dist : float  = math.sqrt(self.to_obj.x ** 2 + self.to_obj.y ** 2)
            if (self.dist > self.radius - 50.0):
                self.n = self.to_obj / self.dist
                objs.pos_current = self.position + self.n * (self.radius - 50.0)
                
	
    def solve_collision(self):
        self.obj_count = len(obj)
        
        for i in range(self.obj_count):
            for k in range(i + 1, self.obj_count):
                self.coll_axis : vect2 = obj[0].pos_current - obj[1].pos_current
                self.dist = math.sqrt(self.coll_axis.x ** 2 + self.coll_axis.y ** 2) 
                if (self.dist < 20):
                    self.n = self.coll_axis / self.dist
                    self.delta : float = 20 - self.dist
                    obj[0].pos_current += 0.5 * self.delta * self.n
                    obj[1].pos_current -= 0.5 * self.delta * self.n




gravity = vect2(0, 1000.0)
solver = Solver(gravity)

while Running:
    clock.tick(60)
    dt = clock.tick(fps) / 1000

    w.fill('#296baa')
    
	
    pg.draw.circle(w, "#0a0d22", (700 / 2, 600 /2), 158.55, 0)

    solver.update(dt)
    

    for event in pg.event.get():
        if event.type == pg.QUIT:
            Running = False

    #if keyboard.is_pressed("space"):
    #    obj[0].pos_current -= vect2(0, 1)
    #if keyboard.is_pressed("a"):
    #    obj[0].pos_current -= vect2(0.5, 0)
    #if keyboard.is_pressed("d"):
    #    obj[0].pos_current += vect2(0.5, 0)
    
    pg.display.update()