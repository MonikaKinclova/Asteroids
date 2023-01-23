import math
import random
from math import sin, cos
import pyglet
from pyglet.window import key
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

# Hlavní postava hry
class Dragon():
    #nastavení základních vlastností
    def __init__(self):
        self.x = window.width/2
        self.y = window.width/2
        self.rotation = 0
        self.sprite = pyglet.sprite.Sprite(image)
        self.sprite.scale= 0.1
        pyglet.clock.schedule_interval(self.move, 1/30)

    #nastavení vykreslení
    def draw(self):
        self.sprite.x= self.x
        self.sprite.y= self.y
        self.sprite.draw()

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
        self.x = random.randint(0, window.width)
        self.y = random.randint(0, window.height)
        self.x_speed = 10
        self.y_speed = 10
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

    def tick(self, dt):
        self.x= self.x + 20 * dt
        self.y= self.y + 20 * dt
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

#vytvoření astronata
astronaut = Astronaut()

class Asteroid:
        #nastavení základních vlastností
    def __init__(self):
        self.x = window.width
        self.y = random.randint(0, window.height)
        self.x_speed = -20
        self.y_speed = -20
        self.rotation = math.pi/2
        self.rotation_speed = 30
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
    fire_asteroid.draw()
    asteroid.draw()
    astronaut.draw()
    drak.draw()
    
#rotace astronauta
def update(dt):
    astronaut.rotation += 1*dt


#registrace funkcí (no nebo jak se to jmenuje)   
window.push_handlers(
    on_key_press,
    on_key_release,
    on_draw)

pyglet.clock.schedule_interval(update, 1/60.)

#spuštění aplikace ... uplně konec programu
pyglet.app.run()