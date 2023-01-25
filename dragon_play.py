import math
import random
from math import sin, cos
from time import sleep
import pyglet
from pyglet.window import key, gl
from pyglet.image import Animation, AnimationFrame

#nastavení okna
window = pyglet.window.Window(width=800, height=500)

#obecné nastavení
ROTATION_SPEED = 500 # radians per second.. zatím nevyužívám
ACCELERATION = 0.5
ASTEROID_SPEED = 1
FIREBALL_SPEED = 2
FIREBALL_INTERVAL = 0.3
i= 20

#pamatuje si zmáčknuté klávesy
pressed_keys =set()

#úvodní obrázek, zobrazí se a po 10s začne hra.. nefunguje, ještě, , příjdu na to
intro = pyglet.image.load('background_intro.jpg')
intro_sprite = pyglet.sprite.Sprite(intro)
intro_sprite.scale= 0.15

#konec, zobrazí se obrázek, že jsem prohrála.. nefunguje, ještě, příjdu na to
game_over = pyglet.image.load('background_game_over.jpg')
game_over_sprite = pyglet.sprite.Sprite(game_over)
game_over_sprite.scale= 0.15

#načtení obrázku draka
image = pyglet.image.load('drak-1.png')
image.anchor_x= image.width // 2
image.anchor_y= image.height // 2

#načtení obrázku na pozadí a nastavení jako pozadí okna
background_image = pyglet.image.load('background.jpg')
background_sprite = pyglet.sprite.Sprite(background_image)
background_sprite.scale= 0.15

#načtení obrázku astronauta
image_astronaut =  pyglet.image.load('astronaut.png')
image_astronaut.anchor_x= image_astronaut.width // 2
image_astronaut.anchor_y= image_astronaut.height // 2

#načtení obrázku asteroidu
image_asteroid =  pyglet.image.load('meteor.png')
image_asteroid.anchor_x= image_asteroid.width // 2
image_asteroid.anchor_y= image_asteroid.height // 2

#načtení obrázku dračí střely
image_fireball =  pyglet.image.load('fireball_1.png')
image_fireball.anchor_x= image_fireball.width // 2
image_fireball.anchor_y= image_fireball.height // 2

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
class Dragon:
    #nastavení základních vlastností
    def __init__(self):
        self.x = window.width/2
        self.y = window.width/2
        self.rotation = 0
        self.radius = 30
        self.sprite = pyglet.sprite.Sprite(image)
        self.sprite.scale= 0.1
        self.next_shot = 0
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
    #střílení a kontrola, jestli drak nenaboural do něčeho
    def tick(self, dt):
        if pyglet.window.key.SPACE in pressed_keys and self.next_shot <= 0:
            print('Mačkám mezerník - střílím')
            fireball = Fireball()
            objects.append(fireball)
            self.next_shot = FIREBALL_INTERVAL
            fireball.x = self.x
            fireball.y=  self.y
        self.next_shot = self.next_shot - dt

        for obj in list(objects):
            if overlaps(self, obj) and self != obj:
                obj.hit_by_dragon(self)
                print('Naboural si')


       #když drak potká fireball.. nic se nestane
    def hit_by_fireball(self, fireball):
        pass


    def delete(self):
        try:
            objects.remove(self)
        except ValueError:
            pass

class Fireball:
    #nastavení základních vlastností
    def __init__(self):
        self.x = window.width
        self.y = random.randint(0, window.height)
        self.x_speed = 10
        self.y_speed = 10
        self.radius = 15
        self.sprite_fireball = pyglet.sprite.Sprite(image_fireball)
        self.sprite_fireball.rotation = 180
        self.sprite_fireball.scale = 0.15
        pyglet.clock.schedule_interval(self.tick, 1/30)
    
    #vykreslení, zbytek vykreslení je uveden v Class Dragon, kde se objekt vytváří
    def draw(self):
        self.sprite_fireball.x = self.x + 50
        self.sprite_fireball.y = self.y
        self.sprite_fireball.draw()
        draw_circle(self.x, self.y, self.radius)

    def tick(self, dt):
        self.x= self.x + 100 * dt
        self.y= self.y + 0 * dt
   
    #funkce na odsranění objektu z hracího pole
    def delete(self):
        try:
            objects.remove(self)
        except ValueError:
            pass

    def hit_by_dragon (self, drak):
        pass
   
    #sestřelení fireballem
    def hit_by_fireball(self, fireball):
        self.delete()
        fireball.delete()

class Space_object:
    #nastavení základních vlastností
    def __init__(self, image):
        self.x = window.width
        self.y = random.randint(0, window.height)
        self.x_speed = 10
        self.y_speed = 10
        self.radius = 40
        self.rotation = math.pi
        self.rotation_speed = 10
        self.sprite = pyglet.sprite.Sprite(image)
        self.sprite.scale = 0.15
        pyglet.clock.schedule_interval(self.tick, 1/30)
    
    def update_rotation(self,dt):
        self.rotation += self.rotation_speed * dt
        pyglet.clock.schedule_interval(self.update_rotation, 1/60)

    def draw(self):
        self.sprite.x= self.x
        self.sprite.y= self.y
        self.sprite.rotation= math.radians(self.rotation)
        self.sprite.draw()
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
    
        for obj in list(objects):
            if overlaps(self, obj) and self != obj:
                obj.hit_by_fireball(self)
                print('Fireball sestřelil objekt')
    

    #funkce na odsranění objektu z hracího pole
    def delete(self):
        try:
            objects.remove(self)
        except ValueError:
            pass
    
    #srážka s drakem   
    def hit_by_dragon (self, drak):
        print('naboural tě astronaut')
        drak.delete()
    
    #sestřelení fireballem
    def hit_by_fireball(self, fireball):
        self.delete()
        fireball.delete()

#vyčištění okna, vykresleni draka a  dalších objektů, zobrazeni pozadi
def on_draw():
    window.clear()
    background_sprite.draw()
    for obj in objects:
        obj.draw()
    
#seznam objektů, které jsou ve hře
drak=Dragon()
astronaut= Space_object(image_astronaut)
asteroid= Space_object(image_asteroid)

#seznam objektů ve vesmíru
objects = [drak, asteroid, astronaut, Fireball()]

#funkce kontrolující objekty a vytváří nové objekty po sestřelení
def check_objects(xxx):
    #tisk pro kontrolu co je v objektech.. pak smazat, az to bude fungovat
    for obj in objects:
        print(obj.__class__.__name__, 'kontrola seznamu objektů')

    #vytváření nových objektů do vesmíru, když se sestřelí ty co už tam byly
    if 'asteroid' not in [type(obj).__name__ for obj in objects]:
        objects.append(Space_object(image_asteroid))
        on_draw()
        draw_circle(obj.x, obj.y, obj.radius)
    elif 'astronaut' not in [type(obj).__name__ for obj in objects]:
        objects.append(Space_object(image_astronaut))
        on_draw()
        draw_circle(obj.x, obj.y, obj.radius)
    #mělo by vykreslit GAME OVER
    #if 'drak' not in [type(obj).__name__ for obj in objects]:
       # game_over.sprite.draw()
       # on_draw()
      

pyglet.clock.schedule_interval(check_objects, 1.0)

#ovládání draka (uloží zmáčknuté tlačítko nahoru do seznamu a v druhé funkci zase smaže)
def on_key_press(key, mod):
    pressed_keys.add(key)

def on_key_release(key, mod):
    pressed_keys.remove(key)

#kontrola kolize 
def tick (dt):
    for obj in objects:
            obj.tick(dt)
pyglet.clock.schedule_interval(tick, 1/30)

#registrace funkcí (no nebo jak se to jmenuje)   
window.push_handlers(
    on_key_press,
    on_key_release,
    on_draw)

#spuštění aplikace ... uplně konec programu
pyglet.app.run()