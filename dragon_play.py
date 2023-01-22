import math
import random
from math import sin, cos
import pyglet
from pyglet.window import key
from pyglet.image import Animation, AnimationFrame

#nastavení okna
window = pyglet.window.Window(width=800, height=500)

#obecné nastavení
ROTATION_SPEED = 100 # radians per second.. zatím nevyužívám
ACCELERATION = 50
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

#vytvořeni astronauta
image_astronaut =  pyglet.image.load('astronaut.png')
sprite_astronaut =  pyglet.sprite.Sprite(image_astronaut)
sprite_astronaut.scale= 0.15

# Vesmírnou loď  reprezentuje objekt třídy Spaceship.
class Spaceship():
    #nastavení základních vlastností
    def __init__(self):
        self.x = window.width/2
        self.y = window.width/2
        self.rotation = 0
        self.x_speed = 0
        self.y_speed = 0
        self.rotation_speed = 10 #zatím nepouživané
        self.radius = 30 #zatím nepoužívané
        self.sprite = pyglet.sprite.Sprite(image)
        self.sprite.scale= 0.1
        pyglet.clock.schedule_interval(self.tick, 1/60)

    def draw(self):
        self.sprite.x= self.x
        self.sprite.y= self.y
        self.sprite.draw()

    def tick(self, dt):
        self.x= self.x + self.x_speed * dt
        self.y= self.y + self.y_speed * dt
        #nastavení pohybu nahoru
        if pyglet.window.key.UP in pressed_keys:
            self.x_speed=  ACCELERATION * sin(self.rotation)
            self.y_speed= ACCELERATION * cos(self.rotation)
         #nastavení pohybu doprava(drak letí dopředu)
        if pyglet.window.key.RIGHT in pressed_keys:
            self.x_speed=  ACCELERATION * cos(self.rotation)
            self.y_speed= ACCELERATION * sin(self.rotation)
        #zastavení draka.. funguje, ale pak se nerozjede znova
        if pyglet.window.key.SPACE in pressed_keys:
            self.x_speed= self.x_speed * 0
            self.y_speed= self.y_speed * 0
         #nastavení pohybu dozadu 
        if pyglet.window.key.LEFT in pressed_keys:
            self.x_speed= - ACCELERATION * cos(self.rotation)
            self.y_speed= - ACCELERATION * sin(self.rotation)
        #nastavení pohybu zatím nefunguje
        if pyglet.window.key.DOWN in pressed_keys:
            self.x_speed=  - ACCELERATION * sin(self.rotation)
            self.y_speed=  - ACCELERATION * cos(self.rotation)
        #nastavení at nevyjede z okna
        if self.x > window.width:
             self.x = 0
        if self.y > window.width:
             self.y = 0   
        if self.x < 0:
             self.x = window.width
        if self.y < 0:
             self.y = window.width  


#vytvoření draka
drak = Spaceship()

class Asteroid:
        #nastavení základních vlastností
    def __init__(self):
        self.x = random.randint(0, window.width)
        self.y = random.randint(0, window.height)
        self.x_speed = 10
        self.y_speed = 10
        self.rotation = math.pi/2
        self.rotation_speed = 10
        self.sprite_astronaut = pyglet.sprite.Sprite(image_astronaut)
    

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

astronaut = Asteroid()


#nefungující mávání křídly
t = 0.3
def zmen(t):
        drak.image = obrazek2
        pyglet.clock.schedule_once(zmen_zpatky, 0.2)
def zmen_zpatky(t):
        drak.image = image
        pyglet.clock.schedule_once(zmen, 0.2)
pyglet.clock.schedule_interval(drak.tick, 1/30)
pyglet.clock.schedule_once(zmen, 1)


#ovládání draka (uloží zmáčknuté tlačítko nahoru do seznamu)
def on_key_press(key, mod):
    pressed_keys.add(key)

#vyčištění okna, vykresleni draka, zobrazeni pozadi
def on_draw():
    window.clear()
    background_sprite.draw()
    sprite_astronaut.draw()
    drak.draw()

#rotace astronauta
def update(dt):
    astronaut.rotation += 1*dt


#registrace funkcí (no nebo jak se to jmenuje)   
window.push_handlers(
    on_key_press,
    on_draw)



pyglet.clock.schedule_interval(update, 1/60.)

#spuštění aplikace ... uplně konec programu
pyglet.app.run()