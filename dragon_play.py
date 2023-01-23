import math
import random
from math import sin, cos
import pyglet
from pyglet.window import key, gl
from pyglet.image import Animation, AnimationFrame

#nastavení okna
window = pyglet.window.Window(width=800, height=500)

#obecné nastavení
ROTATION_SPEED = 500 # radians per second.. zatím nevyužívám
ACCELERATION = 0.5
ASTEROID_SPEED = 1
i= 20

#pamatuje si zmáčknuté klávesy
pressed_keys =set()

#vytvořeni Bathe
batch = pyglet.graphics.Batch()

#načtení obrázku draka
image = pyglet.image.load('drak-1.png')
image.anchor_x= image.width // 2
image.anchor_y= image.height // 2

obrazek2 = pyglet.image.load('drak-2.png')
sprite = pyglet.sprite.Sprite(image)
#batch = pyglet.graphics.Batch().. zatím nepoužívám

#načtení obrázku na pozadí a nastavení jako pozadí okna
background_image = pyglet.image.load('background.jpg')
background_sprite = pyglet.sprite.Sprite(background_image)
background_sprite.scale= 0.15

#načtení obrázku astronauta
image_astronaut =  pyglet.image.load('astronaut.png')
image_astronaut.anchor_x= image_astronaut.width // 2
image_astronaut.anchor_y= image_astronaut.height // 2

#načtení obrázku hořícího asteroidu
image_a_fire =  pyglet.image.load('meteor_f.png')
image_a_fire.anchor_x= image_a_fire.width // 2
image_a_fire.anchor_y= image_a_fire.height // 2

#načtení obrázku hořícího asteroidu
image_asteroid =  pyglet.image.load('meteor.png')
image_asteroid.anchor_x= image_asteroid.width // 2
image_asteroid.anchor_y= image_asteroid.height // 2


#kód zkopírovaný, na vykreslení kolečka kolem objektů
def draw_circle(x, y, radius):
    iterations = 20
    s = math.sin(2*math.pi / iterations)
    c = math.cos(2*math.pi / iterations)

    dx, dy = radius, 0

    gl.glBegin(gl.GL_LINE_STRIP)
    for i in range(iterations+1):
        gl.glVertex2f(x+dx, y+dy)
        dx, dy = (dx*c - dy*s), (dy*c + dx*s)
    gl.glEnd()

#kód zkopírovaný ze zadaní, měří vzdálenost mezi objekty a vyhodnocuje jestli se srazili
def distance(a, b, wrap_size):
    """Distance in one direction (x or y)"""
    result = abs(a - b)
    if result > wrap_size / 2:
        result = wrap_size - result
    return result

def overlaps(a, b):
    """Returns true iff two space objects overlap"""
    distance_squared = (distance(a.x, b.x, window.width) ** 2 +
                        distance(a.y, b.y, window.height) ** 2)
    max_distance_squared = (a.radius + b.radius) ** 2
    return distance_squared < max_distance_squared



# Hlavní postava hry
class Dragon():
    #nastavení základních vlastností
    def __init__(self):
        self.x = window.width/2
        self.y = window.width/2
        self.rotation = 0
        self.radius = 30
        self.sprite = pyglet.sprite.Sprite(image)
        self.sprite.scale= 0.1
        pyglet.clock.schedule_interval(self.move, 1/30)

    #nastavení vykreslení
    def draw(self):
        self.sprite.x= self.x
        self.sprite.y= self.y
        self.sprite.draw()
        draw_circle(self.x, self.y, self.radius)

    #nastavení pohybu
    def move(self, t):
        #základní pohyb
        if pyglet.window.key.UP in pressed_keys:
            self.y += 10 * ACCELERATION
        if pyglet.window.key.DOWN in pressed_keys:
            self.y -= 10 * ACCELERATION
        if pyglet.window.key.RIGHT in pressed_keys:
            self.x += 10 * ACCELERATION
        if pyglet.window.key.LEFT in pressed_keys:
            self.x -= 10 * ACCELERATION
        #nastavení, že když vyjede z okna vrátí se na opačné straně
        if self.x > window.width:
            self.x = 0
        if self.y > window.width:
            self.y = 0   
        if self.x < 0:
            self.x = window.width
        if self.y < 0:
            self.y = window.width  
        
#vytvoření draka
drak = Dragon()

class Astronaut:
        #nastavení základních vlastností
    def __init__(self):
        self.x = window.width
        self.y = random.randint(0, window.height)
        self.x_speed = 10
        self.y_speed = 10
        self.radius = 60
        self.rotation = math.pi
        self.rotation_speed = 10
        self.sprite_astronaut = pyglet.sprite.Sprite(image_astronaut)
        self.sprite_astronaut.scale = 0.15
        pyglet.clock.schedule_interval(self.tick, 1/30)
    
    def update_rotation(self,dt):
        self.rotation += self.rotation_speed * dt
        pyglet.clock.schedule_interval(self.update_rotation, 1/60)

    def draw(self):
        self.sprite_astronaut.x= self.x
        self.sprite_astronaut.y= self.y
        self.sprite_astronaut.rotation= math.radians(self.rotation)
        self.sprite_astronaut.draw()
        draw_circle(self.x, self.y, self.radius)

    def tick(self, dt):
        self.x= self.x - random.randint(20, 40) * dt
        self.y= self.y - 0 * dt
        self.rotation += -ROTATION_SPEED * dt
        
        #nastavení at nevyjede z okna
        if self.x > window.width:
             self.x = 0
        if self.y > window.width:
             self.y = 0   
        if self.x < 0:
             self.x = window.width
        if self.y < 0:
             self.y = window.width       

#vytvoření astronata
astronaut = Astronaut()

class Asteroid:
        #nastavení základních vlastností
    def __init__(self):
        self.x = window.width
        self.y = random.randint(0, window.height)
        self.x_speed = -20
        self.y_speed = -20
        self.radius = 50
        self.rotation = math.pi/2
        self.rotation_speed = 70
        self.sprite_a_fire = pyglet.sprite.Sprite(image_a_fire)
        self.sprite_a_fire.scale = 0.15
        pyglet.clock.schedule_interval(self.tick, 1/30)
    
    #def update_rotation(self,dt):
       # self.rotation += self.rotation_speed * dt
       # pyglet.clock.schedule_interval(self.update_rotation, 1/60)

    def draw(self):
        self.sprite_a_fire.x= self.x
        self.sprite_a_fire.y= self.y
        self.sprite_a_fire.rotation= math.radians(self.rotation)
        self.sprite_a_fire.draw()
        draw_circle(self.x, self.y, self.radius)

    def tick(self, dt):
        self.x= self.x - 20 * dt
        self.y= self.y - 0 * dt
        #self.rotation += ROTATION_SPEED * dt
        
        #nastavení at nevyjede z okna
        if self.x > window.width:
             self.x = 0
        if self.y > window.width:
             self.y = 0   
        if self.x < 0:
             self.x = window.width
        if self.y < 0:
             self.y = window.width       

#vytvoření hořícího asteroidu
fire_asteroid = Asteroid()

class Asteroid_normal:
    #nastavení základních vlastností
    def __init__(self):
        self.x = window.width
        self.y = random.randint(0, window.height)
        self.x_speed = -20
        self.y_speed = 0
        self.radius = 35
        self.rotation = math.pi/2
        self.rotation_speed = 100
        self.sprite_asteroid = pyglet.sprite.Sprite(image_asteroid)
        self.sprite_asteroid.scale = 0.15
        pyglet.clock.schedule_interval(self.tick, 1/30)
    
    def update_rotation(self,dt):
       self.rotation += self.rotation_speed * dt
       pyglet.clock.schedule_interval(self.update_rotation, 1/60)

    def draw(self):
        self.sprite_asteroid.x= self.x
        self.sprite_asteroid.y= self.y
        self.sprite_asteroid.rotation= math.radians(self.rotation)
        self.sprite_asteroid.draw()
        draw_circle(self.x, self.y, self.radius)

    def tick(self, dt):
        self.x= self.x - random.randint(20, 60) * dt
        self.y= self.y - 0 * dt
        self.rotation += ROTATION_SPEED * dt
        
        #nastavení at nevyjede z okna
        if self.x > window.width:
             self.x = 0
        if self.y > window.width:
             self.y = 0   
        if self.x < 0:
             self.x = window.width
        if self.y < 0:
             self.y = window.width 
#vytvoření normálního asteroidu
asteroid = Asteroid_normal()




#ovládání draka (uloží zmáčknuté tlačítko nahoru do seznamu a v druhé funkci zase smaže)
def on_key_press(key, mod):
    pressed_keys.add(key)

def on_key_release(key, mod):
    pressed_keys.remove(key)



#vyčištění okna, vykresleni draka, zobrazeni pozadi
def on_draw():
    window.clear()
    background_sprite.draw()
    batch.draw()
    fire_asteroid.draw()
    asteroid.draw()
    astronaut.draw()
    drak.draw()
    
    


#registrace funkcí (no nebo jak se to jmenuje)   
window.push_handlers(
    on_key_press,
    on_key_release,
    on_draw)



#spuštění aplikace ... uplně konec programu
pyglet.app.run()