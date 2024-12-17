from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

# GLOBAL VARIABLES
W_Width, W_Height = 500, 500
bg_color = (0, 0, 0, 0)

# Spaceship related
spaceship_x, spaceship_y = 0, -230  # position
spaceship_width, spaceship_height = 40, 20

# Falling circles
falling_circles = []  # List of dictionaries for falling circles
circle_spawn_timer = 0  # Timer to control circle spawning
last_time = time.time()  # Initialize with the current time

# Bullets/projectiles
projectiles = []  # List of dictionaries for projectiles
projectile_speed = 350

# Scores
missed_circles = 0  # Count missed circles
miss_fires = 0  # Count miss fires
score = 0  # Player score

# Game state
game_over = False  # Flag to check if the game is over

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

# GAME OBJECTS

## Space Ship
def drawSpaceship():
    global spaceship_x, spaceship_y, spaceship_width, spaceship_height
    # Common values
    half_width = spaceship_width // 2
    left_x = spaceship_x - half_width
    right_x = spaceship_x + half_width
    bottom_y = spaceship_y + spaceship_height
    top_y = spaceship_y + spaceship_height + 20

    # Colors for different parts
    body_color = (0.2, 0.2, 1.0)
    wing_color = (1.0, 1.0, 1.0)
    cockpit_color = (0.0, 1.0, 0.0)
    exhaust_color = (1.0, 0.5, 0.0)

    # Outline size in pixels
    glPointSize(3)
    # Draw the triangular wings
    glColor3f(*wing_color)
    drawLine(left_x, spaceship_y, spaceship_x, top_y)  # Left wing
    drawLine(right_x, spaceship_y, spaceship_x, top_y)  # Right wing

    # Draw the body (rectangular base)
    glColor3f(*body_color)
    drawLine(left_x, spaceship_y, right_x, spaceship_y)
    drawLine(left_x, spaceship_y, left_x, bottom_y)
    drawLine(right_x, spaceship_y, right_x, bottom_y)
    drawLine(left_x, bottom_y, right_x, bottom_y)

    # Draw the cockpit (circle at the top)
    glColor3f(*cockpit_color)
    drawCircle(8, spaceship_x, top_y + 10)

    # Draw two exhausts (circles at the bottom)
    glColor3f(*exhaust_color)
    drawCircle(6, left_x + 10, spaceship_y - 10)
    drawCircle(6, right_x - 10, spaceship_y - 10)

    glPointSize(1)

## Bullets/Projectiles
def shootProjectile():
    if not game_over:
        # Add a new projectile at the current spaceship position
        projectiles.append({'x': spaceship_x, 'y': spaceship_y})

def updateProjectiles(delta_time):
    global projectiles, miss_fires, game_over, projectile_speed

    for projectile in projectiles[:]:
        # Move the projectile upward
        projectile['y'] += projectile_speed * delta_time

        # Remove projectile if it goes off the top of the screen
        if projectile['y'] > W_Height // 2:
            projectiles.remove(projectile)
            miss_fires += 1
            print('Miss fired! Total misfires:', miss_fires)
            if miss_fires >= 3:
                endGame("You misfired too many times!")  # End the game after 3 misfires
                return

def drawProjectiles():
    for projectile in projectiles:
        glColor3f(0, 1, 0)
        drawCircle(5, projectile['x'], projectile['y'])

## Falling circles
def createFallingCircle():
    global falling_circles
    x = random.randint(-W_Width // 2 + 20, W_Width // 2 - 20)
    y = W_Height // 2
    unique = random.choice([True, False])  # unique circles time to time

    if unique:
        radius = 25
    else:
        radius = 20

    speed = 50
    pulse_direction = 1  # 1 = expanding, -1 = shrinking
    pulse_speed = 0.01

    falling_circles.append({
        'x': x, 'y': y, 'radius': radius, 'speed': speed,
        'unique': unique, 'pulse_direction': pulse_direction, 'pulse_speed': pulse_speed
    })

def updateFallingCircles(delta_time):
    global falling_circles, missed_circles, game_over

    for circle in falling_circles[:]:
        # Move the circle down
        circle['y'] -= circle['speed'] * delta_time

        # Unique circle pulsing animation
        if circle['unique']:
            circle['radius'] += circle['pulse_direction'] * circle['pulse_speed']
            # Reverse direction if the radius reaches limits
            if circle['radius'] >= 25:  # Maximum size
                circle['pulse_direction'] = -1
            elif circle['radius'] <= 15:  # Minimum size
                circle['pulse_direction'] = 1

        # Check if the circle touches the spaceship
        if hasCollidedWithSpaceship(circle):
            endGame("A circle touched the spaceship!")  # End the game immediately
            return

        # Check if the circle is missed (crosses the bottom boundary)
        if circle['y'] < -W_Height // 2:
            falling_circles.remove(circle)
            missed_circles += 1
            print("Missed a circle! Total missed:", missed_circles)
            if missed_circles >= 3:
                endGame("Missed too many circles!")  # End the game after 3 misses
                return

def drawFallingCircles():
    glPointSize(3)
    for circle in falling_circles:
        if circle['unique']:
            glColor3f(0.0, 1.0, 1.0)
        else:
            glColor3f(1.0, 0.5, 0.0)
        drawCircle(circle['radius'], circle['x'], circle['y'])  # Draw the circle
    glPointSize(1)

def endGame(reason):
    global game_over, falling_circles, projectiles
    game_over = True  # Set the game_over flag to True
    falling_circles.clear()  # Clear all falling circles
    projectiles.clear()  # Clear all projectiles
    print(f"Game Over: {reason}")  # Print the reason for the game ending
    print(f"Final Score: {score}")

# HELPER FUNCTIONS

## Collision detection
def hasCollidedWithSpaceship(circle):
    global spaceship_x, spaceship_y, spaceship_width, spaceship_height

    # Bounding box for the spaceship
    spaceship_box = {
        'x': spaceship_x - spaceship_width // 2,
        'y': spaceship_y,
        'width': spaceship_width,
        'height': spaceship_height
    }

    # Bounding box for the circle
    circle_box = {
        'x': circle['x'] - circle['radius'],
        'y': circle['y'] - circle['radius'],
        'width': 2 * circle['radius'],
        'height': 2 * circle['radius']
    }

    # AABB collision detection
    return (
        spaceship_box['x'] < circle_box['x'] + circle_box['width'] and
        spaceship_box['x'] + spaceship_box['width'] > circle_box['x'] and
        spaceship_box['y'] < circle_box['y'] + circle_box['height'] and
        spaceship_box['y'] + spaceship_box['height'] > circle_box['y']
    )

def hasCollided(circle, projectile):
    circle_box = {'x': circle['x'] - circle['radius'], 'y': circle['y'] - circle['radius'],
                  'width': 2 * circle['radius'], 'height': 2 * circle['radius']}
    projectile_box = {'x': projectile['x'] - 2, 'y': projectile['y'] - 2, 'width': 4, 'height': 4}
    return (circle_box['x'] < projectile_box['x'] + projectile_box['width'] and
            circle_box['x'] + circle_box['width'] > projectile_box['x'] and
            circle_box['y'] < projectile_box['y'] + projectile_box['height'] and
            circle_box['y'] + circle_box['height'] > projectile_box['y'])

def checkCollisions():
    global falling_circles, projectiles, score
    for circle in falling_circles[:]:
        for projectile in projectiles[:]:
            if hasCollided(circle, projectile):
                falling_circles.remove(circle)
                projectiles.remove(projectile)
                score += 5 if circle['unique'] else 1
                print("Score:", score)

# Input listener functions
def keyboardListener(key, x, y):
    global spaceship_x, W_Width, spaceship_width, game_over

    move_speed = 10  # Adjust this value to control spaceship movement

    if not game_over:
        if key == b'a':  # Move spaceship left
            spaceship_x = max(spaceship_x - move_speed, -W_Width // 2 + spaceship_width // 2)
        elif key == b'd':  # Move spaceship right
            spaceship_x = min(spaceship_x + move_speed, W_Width // 2 - spaceship_width // 2)
        elif key == b' ':  # Spacebar to shoot
            shootProjectile()

    glutPostRedisplay()

# OpenGL related functions
def animate():
    global last_time, circle_spawn_timer

    current_time = time.time()

    if not game_over:
        # Calculate delta_time only when the game is running
        delta_time = current_time - last_time
        last_time = current_time  # Update last_time only when the game is running

        circle_spawn_timer += delta_time
        if circle_spawn_timer > 2:  # Spawn a new circle every 2 seconds
            createFallingCircle()
            circle_spawn_timer = 0

        updateFallingCircles(delta_time)
        updateProjectiles(delta_time)
        checkCollisions()
    else:
        # Keep the timer current while the game is over
        last_time = current_time

    glutPostRedisplay()

def display():
    global bg_color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(*bg_color)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)

    # Draw game objects
    drawSpaceship()
    drawFallingCircles()
    drawProjectiles()

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

wind = glutCreateWindow(b"Lab 2: Shoot the Circles")
init()

glutDisplayFunc(display)  # Display callback
glutIdleFunc(animate)  # Idle callback
glutKeyboardFunc(keyboardListener)

glutMainLoop()  # Start the GLUT event loop
