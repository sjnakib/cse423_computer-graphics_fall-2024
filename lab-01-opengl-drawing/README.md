# Lab 1: OpenGL Drawing

CSE423 Computer Graphics, Fall 2024, BRAC University.

This lab has two separate OpenGL programs. Both use PyOpenGL and GLUT.

## Files

- `src/task_1_house_in_rain.py`: draws a house in the rain. The background changes between day and night, and the rain can bend left or right.
- `src/task_2_amazing_box.py`: draws a box of moving points. You can add points, make them blink, freeze them, and change their speed.

## How to run

From the repository root:

```bash
python3 -m pip install -r requirements.txt
python3 lab-01-opengl-drawing/src/task_1_house_in_rain.py
python3 lab-01-opengl-drawing/src/task_2_amazing_box.py
```

You need a desktop session with OpenGL support. Each program opens a 500x500 window.

## Controls

### Task 1: House in the rain

| Key | Action |
|-----|--------|
| `b` | Change the background to day |
| `d` | Change the background to night |
| Left arrow | Bend the rain to the left |
| Right arrow | Bend the rain to the right |

Close the window to stop the program.

### Task 2: Amazing box

| Input | Action |
|-------|--------|
| Right click | Add a point at the mouse position |
| Left click | Turn blinking on or off |
| Space | Freeze or unfreeze the points |
| Up arrow | Increase the speed |
| Down arrow | Decrease the speed |
| `Esc` | Quit |

## Notes

- The rain drops are hidden when they reach the roof, so the rain does not fall through the house.
- The wall color changes with the background so the house stays visible.
- Task 2 prints the blink state and speed changes to the console.
