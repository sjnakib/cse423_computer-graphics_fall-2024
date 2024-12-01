# OpenGL Reference

These files are course reference material for the OpenGL labs.

## Contents

- `cse423-opengl-lab-reference.ipynb`: a reference notebook with OpenGL and GLUT function definitions and small examples. It is a reference sheet, not a single runnable program.
- `first-program/hello_opengl.py`: a small starter program that opens a 500x500 window and draws one yellow point at the center.
- `first-program/lets_draw_sth.py`: a starter program with a moving point, axes, a triangle, a quad, and mouse and keyboard handlers.

## How to use

The notebook is meant to be read. If you want to open it, use Jupyter Notebook or JupyterLab. The two Python files need PyOpenGL:

```bash
python3 -m pip install -r requirements.txt
python3 docs/reference/first-program/hello_opengl.py
python3 docs/reference/first-program/lets_draw_sth.py
```

The original starter folder included a copy of PyOpenGL. I removed that copy and used `requirements.txt` instead.
