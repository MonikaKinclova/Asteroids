import pyglet
import math
from math import sin, cos
from pyglet.window import key, gl

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
    distance_squared = (distance(a.x, b.x, width = 800) ** 2 +
                        distance(a.y, b.y, height = 500) ** 2)
    max_distance_squared = (a.radius + b.radius) ** 2
    return distance_squared < max_distance_squared