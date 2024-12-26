# CSE423 Computer Graphics

**Fall 2024, BRAC University**

![Stars](https://img.shields.io/github/stars/sjnakib/cse423_computer-graphics_fall-2024?style=for-the-badge&logo=github&color=yellow)
![Last Commit](https://img.shields.io/github/last-commit/sjnakib/cse423_computer-graphics_fall-2024?style=for-the-badge&color=blue)
![Repo Size](https://img.shields.io/github/repo-size/sjnakib/cse423_computer-graphics_fall-2024?style=for-the-badge&color=green)
![Language](https://img.shields.io/github/languages/top/sjnakib/cse423_computer-graphics_fall-2024?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenGL](https://img.shields.io/badge/OpenGL-PyOpenGL-5586A4?style=for-the-badge&logo=opengl&logoColor=white)
![BRAC University](https://img.shields.io/badge/BRAC%20University-CSE423-006A4E?style=for-the-badge)
![Semester](https://img.shields.io/badge/Semester-Fall%202024-6A1B9A?style=for-the-badge)

This repository holds my coursework for CSE423 Computer Graphics at BRAC University in Fall 2024. It has the two OpenGL labs, one theory assignment on color interpolation, and the study notes I used during the course. The lab code is in Python and uses PyOpenGL.

## 📚 Assignments

| # | Title | What it does | Tech | Folder |
|---|-------|--------------|------|--------|
| 1 | 🏠 Lab 1: OpenGL Drawing | Draws a house in the rain and an animated box of points. | Python, PyOpenGL, GLUT | [lab-01-opengl-drawing](lab-01-opengl-drawing/) |
| 2 | 🚀 Lab 2: Shoot the Circles | A 2D shooter that uses midpoint line and circle drawing and AABB collision. | Python, PyOpenGL, GLUT | [lab-02-shoot-the-circles](lab-02-shoot-the-circles/) |
| 3 | 🎨 Assignment 1: Color Interpolation | Uses Gouraud shading to find RGB colors and converts them to HSV. | Handwritten PDF | [assignment-01-color-interpolation](assignment-01-color-interpolation/) |

## 🎮 Project

The final project for this course is [Hill Climb Racing](https://github.com/sjnakib/opengl-hill-climb-racing), kept in a separate repository. Group: Shafaat Jamil Nakib, A.B.M. Danial, and Rabaya Farzana Sikder.

## 📝 Study materials

The `study-materials/` folder has my class notes, the course outline, a post-midterm topic list, a practice sheet, and lecture notes from Mr. Shakir Rouf. The textbook PDFs and instructor slides are not included because they are copyrighted. See [study-materials/README.md](study-materials/README.md) for the details.

## 📖 Reference

The `docs/reference/` folder has the OpenGL lab reference notebook and the two starter programs from the course. The original starter folder included a copy of PyOpenGL. I removed that copy and used `requirements.txt` instead.

## 📂 Project structure

```text
.
├── assignment-01-color-interpolation/
│   ├── README.md
│   └── docs/
├── docs/
│   └── reference/
├── lab-01-opengl-drawing/
│   ├── README.md
│   └── src/
├── lab-02-shoot-the-circles/
│   ├── README.md
│   ├── docs/
│   └── src/
├── study-materials/
│   ├── README.md
│   ├── course-outline/
│   ├── notes/
│   └── practice-sheets/
├── .gitignore
├── README.md
└── requirements.txt
```

## ▶️ How to run

1. Clone the repository:

   ```bash
   git clone https://github.com/sjnakib/cse423_computer-graphics_fall-2024.git
   cd cse423_computer-graphics_fall-2024
   ```

2. Install the Python dependency:

   ```bash
   python3 -m pip install -r requirements.txt
   ```

3. Run a lab program from the repository root:

   ```bash
   python3 lab-01-opengl-drawing/src/task_1_house_in_rain.py
   python3 lab-01-opengl-drawing/src/task_2_amazing_box.py
   python3 lab-02-shoot-the-circles/src/shoot_the_circles.py
   ```

The labs need a desktop session with OpenGL support. They open a 500x500 window. See each lab README for the controls.

## 🛠️ Skills shown

- Drawing with OpenGL points, lines, and circles.
- Midpoint line drawing with 8-zone symmetry.
- Midpoint circle drawing with 8-way symmetry.
- Keyboard and mouse input in GLUT.
- Animation with delta time.
- AABB collision detection.
- Color interpolation with Gouraud shading and RGB to HSV conversion.
- Organizing a small Python project and writing setup notes.

## 👤 Author

**Shafaat Jamil Nakib**

GitHub: [@sjnakib](https://github.com/sjnakib)
