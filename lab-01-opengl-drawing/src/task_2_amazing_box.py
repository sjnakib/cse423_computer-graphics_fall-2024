"""Draw an animated box of points with mouse and keyboard controls.

Right click adds a point, left click toggles blinking, space freezes the
points, the up and down arrow keys change the speed, and Esc quits.
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

# GLOBAL VARIABLES
W_Width, W_Height = 500, 500

# Controlling variables
points = []  # List of all points created
speed = 0.1
frozen = False
blink = False  # Blink mode on/off
blink_state = False  # True = bg_color, False = original color
last_blink_time = 0

# Colors
bg_color = [0.0, 0.0, 0.0, 0.0]

# Drawing Class
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = [random.random(), random.random(), random.random()]  # Random color
        self.temp_color = self.color
        self.velocity = (random.uniform(-1, 1), random.uniform(-1, 1))  # Random direction
        self.blinking = False  # Track if the point is blinking

    def update(self):
        global frozen, blink, last_blink_time, bg_color, blink_state
        # Update point's position
        if not frozen:
            self.x += self.velocity[0] * speed
            self.y += self.velocity[1] * speed

        # Bounce off the window borders
        # x-axis borders
        if self.x <= -W_Width / 2 or self.x >= W_Width / 2:
            self.velocity = (-self.velocity[0], self.velocity[1])
        # y-axis borders
        if self.y <= -W_Height / 2 or self.y >= W_Height / 2:
            self.velocity = (self.velocity[0], -self.velocity[1])

        # toggle between background color and previous color if blinking is enabled
        if blink:
            if blink_state:
                self.color = bg_color
            else:
                self.color = self.temp_color

    def drawPoint(self):
        glPointSize(5)
        glColor3f(self.color[0], self.color[1], self.color[2])
        glBegin(GL_POINTS)
        glVertex2f(self.x, self.y)
        glEnd()

# Helper functions
def create_point(x, y):
    # create a point object and add the object to the list of points
    points.append(Point(x, y))

# Input listener functions
def mouseListener(button, state, x, y):
    global points, W_Width, W_Height, blink
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:

        # Convert mouse coordinates to OpenGL coordinates
        a = x - (W_Width/2)
        b = (W_Height/2) - y

        create_point(a, b)

    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        blink = not blink
        print('Blinking on:', blink)

    glutPostRedisplay()

def keyboardListener(key, x, y):
    global speed, frozen
    if key == b'\x1b':  # Esc key
        glutLeaveMainLoop() # Quit
    elif key == b' ':
        frozen = not frozen
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global speed
    if key == GLUT_KEY_UP:
        speed *= 1.5  # Increase speed
        print(f"Speed increased to {round(speed, 2)}")
    elif key == GLUT_KEY_DOWN:
        speed /= 1.5  # Decrease speed
        print(f"Speed decreased to {round(speed, 2)}")
    glutPostRedisplay()

# OpenGL related functions
def animate():
    global blink, last_blink_time, blink_state

    # Update global blink state every 0.5 seconds
    if blink:
        current_time = time.time()
        if current_time - last_blink_time > 0.5:  # Blink interval
            blink_state = not blink_state  # Toggle blink state
            last_blink_time = current_time  # Reset timer

    # Update all points
    for point in points:
        point.update()

    glutPostRedisplay()

def display():
    global bg_color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(*bg_color)  # Set background color
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)

    for point in points:
        point.drawPoint()

    glutSwapBuffers()

def init():
    # Clear the screen
    glClearColor(0, 0, 0, 0)
    # Load the projection matrix
    glMatrixMode(GL_PROJECTION)
    # Initialize the matrix
    glLoadIdentity()
    # Set the perspective. The first value is the field of view in degrees.
    # The second value is the aspect ratio. The last two are the near and far planes.
    gluPerspective(104, 1, 1, 1000.0)

# Driver code
glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)  # Depth buffer, double buffer, RGB color

wind = glutCreateWindow(b"Task 2: Amazing Box")
init()

glutDisplayFunc(display)  # Display callback
glutIdleFunc(animate)  # Idle callback
glutMouseFunc(mouseListener)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)

glutMainLoop()  # Start the GLUT event loop
