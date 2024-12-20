# Lab 2: Shoot the Circles

CSE423 Computer Graphics, Fall 2024, BRAC University.

This is a small 2D shooter game. A spaceship at the bottom moves left and right and shoots at falling circles. The game uses the midpoint line and circle drawing algorithms. Everything is drawn with `GL_POINTS`. Collision detection uses axis-aligned bounding boxes (AABB).

## Files

- `src/shoot_the_circles.py`: the game.
- `docs/lab-02-handout.docx`: the lab handout.
- `docs/aabb-hitbox-mechanics.pdf`: the AABB slides.
- `docs/collision-diagram.png`: the collision diagram from the handout.

## How to run

From the repository root:

```bash
python3 -m pip install -r requirements.txt
python3 lab-02-shoot-the-circles/src/shoot_the_circles.py
```

You need a desktop session with OpenGL support. The game opens a 500x500 window.

## Controls

| Input | Action |
|-------|--------|
| `a` | Move the spaceship left |
| `d` | Move the spaceship right |
| Space | Shoot a projectile |
| Left click on the left arrow | Restart the game |
| Left click on the amber triangle | Pause or resume |
| Left click on the red cross | Quit |

The game starts paused. Click the amber triangle to start.

## Rules

- Hit a normal circle to get 1 point.
- Hit a pulsing circle to get 5 points.
- A circle that touches the spaceship ends the game.
- Three missed circles end the game.
- Three missed shots end the game.
- The score and game over messages are printed in the console.

## Drawing and collision

- `drawLine` uses the midpoint line algorithm with the 8-zone symmetry.
- `drawCircle` uses the midpoint circle algorithm with 8-way symmetry.
- `hasCollided` and `hasCollidedWithSpaceship` use AABB collision detection.
- The game uses delta time so movement is based on elapsed time, not frame count.

## Console messages

The game prints the score after each hit, the miss counts, and the reason the game ended. For example, it prints `Score: 5`, `Missed a circle! Total missed: 1`, and `Game Over: Missed too many circles!`.

## Known limits

- The restart button does not reset the misfire counter. After a restart, the old misfires still count toward the three-miss limit.
- The play/pause button always draws the play triangle. The icon does not change when the game is paused.
- The score is only printed in the console. It is not drawn on the game window.
