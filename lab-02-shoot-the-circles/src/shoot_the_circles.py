from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# GLOBAL VARIABLES
W_Width, W_Height = 500, 500
bg_color = (0, 0, 0, 0)

# DRAWING ALGORITHMS

## Midpoint Line Drawing
def find_zone(dx, dy):
    if abs(dx) >= abs(dy):  # Slope <= 1
        if dx >= 0 and dy >= 0:
            return 0  # Zone 0
        elif dx < 0 and dy >= 0:
            return 3  # Zone 3
        elif dx < 0 and dy < 0:
            return 4  # Zone 4
        elif dx > 0 and dy < 0:
            return 7  # Zone 7
    else:  # Slope > 1
        if dx >= 0 and dy > 0:
            return 1  # Zone 1
        elif dx < 0 and dy > 0:
            return 2  # Zone 2
        elif dx < 0 and dy < 0:
            return 5  # Zone 5
        elif dx >= 0 and dy < 0:
            return 6

def drawLine(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    # Determine the zone
    zone = find_zone(dx, dy)

    # Transform points to Zone 0
    x1, y1 = to_zone0(x1, y1, zone)
    x2, y2 = to_zone0(x2, y2, zone)

    # Ensure x1 <= x2 for Zone 0
    if x1 > x2:
        x1, y1, x2, y2 = x2, y2, x1, y1

    # Midpoint Line Algorithm in Zone 0
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    x, y = x1, y1

    glBegin(GL_POINTS)
    while x <= x2:
        # Transform back to the original zone before plotting
        original_x, original_y = from_zone0(x, y, zone)
        glVertex2i(original_x, original_y)
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE
        x += 1
    glEnd()

def to_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y

def from_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

## Midpoint circle drawing algorithm
def drawCircle(radius, cx=0, cy=0):
    x = 0
    y = radius
    d = 1 - radius  # Initial decision parameter

    glBegin(GL_POINTS)
    while x <= y:
        # Plot points in all 8 octants
        plot_circle_points(cx, cy, x, y)
        if d < 0:
            # Choose East
            d += 2 * x + 3
        else:
            # Choose South-East
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
    glEnd()

def plot_circle_points(cx, cy, x, y):
    glVertex2i(int(cx + x), int(cy + y))  # Octant 1
    glVertex2i(int(cx + y), int(cy + x))  # Octant 2
    glVertex2i(int(cx - y), int(cy + x))  # Octant 3
    glVertex2i(int(cx - x), int(cy + y))  # Octant 4
    glVertex2i(int(cx - x), int(cy - y))  # Octant 5
    glVertex2i(int(cx - y), int(cy - x))  # Octant 6
    glVertex2i(int(cx + y), int(cy - x))  # Octant 7
    glVertex2i(int(cx + x), int(cy - y))

# OpenGL related functions
def display():
    global bg_color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(*bg_color)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)

    # Draw a line in zone 0 and a line in zone 3
    glPointSize(3)
    glColor3f(1.0, 1.0, 1.0)
    drawLine(-150, -100, 150, 100)
    glColor3f(0.0, 1.0, 1.0)
    drawLine(150, -100, -150, 100)

    # Draw two circles
    glColor3f(0.0, 1.0, 0.0)
    drawCircle(80, 0, 0)
    glColor3f(1.0, 0.5, 0.0)
    drawCircle(40, -150, 100)
    glPointSize(1)

    glutSwapBuffers()

def init():
    global bg_color
    # Clear the screen
    glClearColor(*bg_color)
    # Load the projection matrix
    glMatrixMode(GL_PROJECTION)
    # Initialize the matrix
    glLoadIdentity()
    # Set the perspective. The first value is the field of view in degrees.
    # The second value is the aspect ratio. The last two are the near and far planes.
    gluPerspective(104, 1, 1, 1000.0)

# DRIVER CODE
glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)  # Depth buffer, double buffer, RGB color

wind = glutCreateWindow(b"Lab 2: Midpoint Line and Circle Drawing")
init()

glutDisplayFunc(display)  # Display callback

glutMainLoop()  # Start the GLUT event loop
