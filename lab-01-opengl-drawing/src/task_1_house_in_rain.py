"""Draw a house in the rain with a day and night background.

Press b for day, d for night, and the left or right arrow key to bend the rain.
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# GLOBAL VARIABLES
W_Width, W_Height = 500, 500

## Animation
### Rain
rain_speed = 0.3
rain_bend = 0.0  # Bending factor (-ve for left, +ve for right)
rain_drops = [[random.randint(-250, 250), random.randint(0, 500)] for _ in range(150)]  # Random raindrops
### Rain boundaries
roof_left = -120
roof_right = 120
roof_top = -100
### Background Transition
transition_speed = 0.01  # Speed for day-night transitions

## Colors
bg_color = [0.0, 0.0, 0.0, 0.0]

### House colors
roof_color = [0.5, 0.1, 0.7]   # roof
house_color = [1.0, 1.0, 1.0]   # walls, door, windows, and windows' crossbars
knob_color = [0.9, 0.8, 0.5]  # door knob


# FUNCTIONS

# Drawing Functions
def drawHouse():
    global roof_color, house_color, knob_color

    # Line width
    glLineWidth(2.0)

    # Roof
    glBegin(GL_TRIANGLES)
    glColor3f(*roof_color)  # Use the global color instead of a fixed color
    glVertex2d(-120, -100)  # Left vertex
    glVertex2d(120, -100)  # Right vertex
    glVertex2d(0, 0)     # Top vertex
    glEnd()

    # Walls
    glBegin(GL_LINES)
    glColor3f(*house_color)
    ##  Bottom wall
    glVertex2d(-100, -230)
    glVertex2d(100, -230)
    ## Right wall
    glVertex2d(100, -230)
    glVertex2d(100, -100)
    ## Top wall
    glVertex2d(100, -100)
    glVertex2d(-100, -100)
    ## Left wall
    glVertex2d(-100, -100)
    glVertex2d(-100, -230)
    glEnd()

    # Door
    glBegin(GL_LINES)
    glColor3f(*house_color)
    ## Bottom of the door
    glVertex2d(-30, -230)
    glVertex2d(30, -230)
    ## Left side of the door
    glVertex2d(-30, -230)
    glVertex2d(-30, -150)
    ## Top of the door
    glVertex2d(-30, -150)
    glVertex2d(30, -150)
    ## Right side of the door
    glVertex2d(30, -150)
    glVertex2d(30, -230)
    glEnd()

    # Door knob
    glPointSize(5.0)
    glBegin(GL_POINTS)
    glColor3f(*knob_color)
    glVertex2d(20, -190)
    glEnd()

    # Left window
    glBegin(GL_LINES)
    glColor3f(*house_color)
    ## Bottom of the window
    glVertex2d(-90, -190)
    glVertex2d(-50, -190)
    ## Left side of the window
    glVertex2d(-90, -190)
    glVertex2d(-90, -150)
    ## Top of the window
    glVertex2d(-90, -150)
    glVertex2d(-50, -150)
    ## Right of the window
    glVertex2d(-50, -150)
    glVertex2d(-50, -190)
    glEnd()

    # Right window
    glBegin(GL_LINES)
    glColor3f(*house_color)
    ## Bottom of the window
    glVertex2d(50, -190)
    glVertex2d(90, -190)
    ## Left of the window
    glVertex2d(50, -190)
    glVertex2d(50, -150)
    ## Top of the window
    glVertex2d(50, -150)
    glVertex2d(90, -150)
    ## Right of the window
    glVertex2d(90, -150)
    glVertex2d(90, -190)
    glEnd()

    # Cross-bars for windows
    glBegin(GL_LINES)
    glColor3f(*house_color)
    ## Left window cross-bars
    glVertex2d(-70, -190)
    glVertex2d(-70, -150)
    glVertex2d(-90, -170)
    glVertex2d(-50, -170)
    ## Right window cross-bars
    glVertex2d(70, -190)
    glVertex2d(70, -150)
    glVertex2d(50, -170)
    glVertex2d(90, -170)
    glEnd()

def drawRain():
    global rain_drops, rain_speed, rain_bend

    glBegin(GL_POINTS)
    glColor3f(0.0, 0.5, 1.0)  # Rain color (blue)
    for drop in rain_drops:
        x, y = drop

        # Hide drops that fall behind the roof
        if ((roof_left <= x) and (x <= roof_right)) and (y <= roof_top):
            y = roof_top  # Stop at the roof
        else:
            glVertex2d(x, y)  # Draw raindrop

        drop[1] -= rain_speed  # Move downward
        drop[0] += rain_bend   # Apply bending

        # Reset raindrop if it falls below the screen
        if drop[1] < -250:
            drop[1] = random.randint(250, 500)
            drop[0] = random.randint(-250, 250)

        # Reset raindrop if it goes out of bounds horizontally
        if drop[0] < -250 or drop[0] > 250:
            drop[0] = random.randint(-250, 250)
    glEnd()

# Helper Functions
def adjust_color(target_color):
    global bg_color, house_color

    for i in range(3):  # RGB channels only
        if bg_color[i] < target_color[i]:
            bg_color[i] += transition_speed
        elif bg_color[i] > target_color[i]:
            bg_color[i] -= transition_speed

    # Update house_color
    house_color = [1 - bg_color[0], 1 - bg_color[1], 1 - bg_color[2]]


# Input listener functions
def keyboardListener(key, x, y):
    global rain_bend, bg_color

    if key == b'b':  # Daytime transition
        adjust_color([1.0, 1.0, 1.0])
    elif key == b'd':  # Nighttime transition
        adjust_color([0.0, 0.0, 0.0])

def specialKeyListener(key, x, y):
    global rain_bend
    if key == GLUT_KEY_LEFT:
        rain_bend = max(rain_bend - 0.02, -0.5)  # Limit left bend
    elif key == GLUT_KEY_RIGHT:
        rain_bend = min(rain_bend + 0.02, 0.5)  # Limit right bend

# OpenGL related functions
def animate():
    glutPostRedisplay()

def display():
    global bg_color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(*bg_color)  # Set background color
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)

    # Draw the scene
    drawRain()
    drawHouse()

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

wind = glutCreateWindow(b"Task 1: House in Rainfall")
init()

glutDisplayFunc(display)  # Display callback
glutIdleFunc(animate)  # Idle callback

glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)

glutMainLoop()  # Start the GLUT event loop
