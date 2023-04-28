from tkinter import *
from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLU import *
from model.axis import Axis
from model.camera import Camera
from model.vertex import Vertex
from model.edge import Edge
from model.figure import Figure
from tkinter.ttk import Combobox
import math


def resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40.0, float(width / height), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def click_fill_figure():
    figures[figure_id].change_fill()


def get_figure():
    temp_figure = combo_select_figure.get()
    global figure_id
    if temp_figure == "Куб":
        figure_id = 0
    elif temp_figure == "Пирамида":
        figure_id = 1
    elif temp_figure == "Конус":
        figure_id = 2
    elif temp_figure == "Цилиндр":
        figure_id = 3


def camera_plus_tx(event):
    camera.tx = 0.1


def camera_minus_tx(event):
    camera.tx = -0.1


def camera_plus_tz(event):
    camera.tz = 0.1


def camera_minus_tz(event):
    camera.tz = -0.1


def camera_plus_ty(event):
    camera.ty = 0.1


def camera_minus_ty(event):
    camera.ty = -0.1


def camera_plus_ry(event):
    camera.ry = 1.0


def camera_minus_ry(event):
    camera.ry = -1.0


def camera_plus_rx(event):
    camera.rx = 1.0


def camera_minus_rx(event):
    camera.rx = -1.0


def camera_plus_rz(event):
    camera.rz = 1.0


def camera_minus_rz(event):
    camera.rz = -1.0


def plus_axes_x(event):
    figures[figure_id].tx = 0.01


def minus_axes_x(event):
    figures[figure_id].tx = -0.01


def plus_axes_y(event):
    figures[figure_id].ty = 0.01


def minus_axes_y(event):
    figures[figure_id].ty = -0.01


def plus_axes_z(event):
    figures[figure_id].tz = 0.01


def minus_axes_z(event):
    figures[figure_id].tz = -0.01


def plus_axes_rx(event):
    figures[figure_id].rx = 0.5


def minus_axes_rx(event):
    figures[figure_id].rx = -0.5


def plus_axes_ry(event):
    figures[figure_id].ry = 0.5


def minus_axes_ry(event):
    figures[figure_id].ry = -0.5


def plus_axes_rz(event):
    figures[figure_id].rz = 0.5


def minus_axes_rz(event):
    figures[figure_id].rz = -0.5


def plus_axes_sxyz(event):
    figures[figure_id].sxyz = 1.01


def minus_axes_sxyz(event):
    figures[figure_id].sxyz = 1 / 1.01


def camera_stop(event):
    if camera.tx > 0:
        camera.tx = 0
    elif camera.tx < 0:
        camera.tx = 0
    elif camera.tz > 0:
        camera.tz = 0
    elif camera.tz < 0:
        camera.tz = 0
    elif camera.ty > 0:
        camera.ty = 0.0
    elif camera.ty < 0:
        camera.ty = 0.0
    elif camera.ry > 0:
        camera.ry = 0.0
    elif camera.ry < 0:
        camera.ry = 0.0
    elif camera.rx < 0:
        camera.rx = 0.0
    elif camera.rx > 0:
        camera.rx = 0.0
    elif camera.rz < 0:
        camera.rz = 0.0
    elif camera.rz > 0:
        camera.rz = 0.0


def figure_stop(event):
    figures[figure_id].stop()


def createCircle(shift_x, shift_y, shift_z, R):
    global vertexes_circle
    steps = 100
    angle = math.pi * 2 / steps

    for i in range(steps):
        newX = R * math.sin(angle * i) + shift_x
        newY = -R * math.cos(angle * i) + shift_y
        vertexes_circle.append([newX, newY, shift_z])

    newX = R * math.sin(angle * 1000) + shift_x
    newY = -R * math.cos(angle * 1000) + shift_y
    vertexes_circle.append([newX, newY, shift_z])


class DrawingWindow(OpenGLFrame):  # создание класса на основе пакета pyopengltk

    def initgl(self):  # инициализация
        resize(*SCREEN_SIZE)

    def redraw(self):  # перерисовка
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glEnable(GL_DEPTH_TEST)

        camera.render()
        axis.render()

        get_figure()
        for i in range(len(figures)):
            figures[i].render()

        glPopMatrix()

        glMatrixMode(GL_PROJECTION)  # устанавливается текущая матрица
        glPushMatrix()  # сохраняется текущая матрица проекции на стек матриц
        glLoadIdentity()  # загружается единичная матрица проекции
        glOrtho(0.0, SCREEN_SIZE[0], SCREEN_SIZE[1], 0.0, 0.0, 1.0)  # устанавливатся ортографическая матрица проекции
        # Ортографическая матрица проекции позволяет рисовать объекты на экране без перспективной деформации.
        glMatrixMode(GL_MODELVIEW)

        glLoadIdentity()
        glDisable(GL_CULL_FACE)  # отключение отсечение граней

        glClear(GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)


root = Tk()  # главное окно
root.resizable(False, False)

axis = Axis()
camera = Camera()

vertex0_cube = Vertex(1, -1, -1)
vertex1_cube = Vertex(1, 1, -1)
vertex2_cube = Vertex(-1, 1, -1)
vertex3_cube = Vertex(-1, -1, -1)
vertex4_cube = Vertex(1, -1, 1)
vertex5_cube = Vertex(1, 1, 1)
vertex6_cube = Vertex(-1, -1, 1)
vertex7_cube = Vertex(-1, 1, 1)

edges_cube = (Edge(vertex0_cube, vertex1_cube),
              Edge(vertex0_cube, vertex3_cube),
              Edge(vertex0_cube, vertex4_cube),
              Edge(vertex2_cube, vertex1_cube),
              Edge(vertex2_cube, vertex3_cube),
              Edge(vertex2_cube, vertex7_cube),
              Edge(vertex6_cube, vertex3_cube),
              Edge(vertex6_cube, vertex4_cube),
              Edge(vertex6_cube, vertex7_cube),
              Edge(vertex5_cube, vertex1_cube),
              Edge(vertex5_cube, vertex4_cube),
              Edge(vertex5_cube, vertex7_cube),
              )

vertex1_pyramid = Vertex(-1, 0, 0)
vertex2_pyramid = Vertex(0, 0, 1)
vertex3_pyramid = Vertex(1, 0, 0)
vertex4_pyramid = Vertex(0, 0, -1)
vertex5_pyramid = Vertex(0, 1, 0)

edges_pyramid = (Edge(vertex1_pyramid, vertex5_pyramid),
                 Edge(vertex2_pyramid, vertex5_pyramid),
                 Edge(vertex3_pyramid, vertex5_pyramid),
                 Edge(vertex4_pyramid, vertex5_pyramid),
                 Edge(vertex1_pyramid, vertex4_pyramid),
                 Edge(vertex3_pyramid, vertex4_pyramid),
                 Edge(vertex2_pyramid, vertex3_pyramid),
                 Edge(vertex1_pyramid, vertex2_pyramid))

vertexes_circle = []
createCircle(0, 0, 0, 1)
edge_cone = []
vertex_cone = Vertex(0, 1, 0)

for i in range(len(vertexes_circle) - 1):
    temp_vertex1 = Vertex(vertexes_circle[i][0], vertexes_circle[i][2], vertexes_circle[i][1])
    temp_vertex2 = Vertex(vertexes_circle[i + 1][0], vertexes_circle[i + 1][2], vertexes_circle[i + 1][1])
    edge_cone.append(Edge(temp_vertex1, temp_vertex2))
    if i % 5 == 0:
        edge_cone.append(Edge(temp_vertex1, vertex_cone))

edge_cylinder = []
temp_circle = vertexes_circle.copy()
vertexes_circle.clear()
createCircle(0, 0, 1, 1)

for i in range(len(temp_circle) - 1):
    temp_vertex1 = Vertex(temp_circle[i][0], temp_circle[i][2], temp_circle[i][1])
    temp_vertex2 = Vertex(temp_circle[i + 1][0], temp_circle[i + 1][2], temp_circle[i + 1][1])

    temp1_vertex1 = Vertex(vertexes_circle[i][0], vertexes_circle[i][2], vertexes_circle[i][1])
    temp1_vertex2 = Vertex(vertexes_circle[i + 1][0], vertexes_circle[i + 1][2], vertexes_circle[i + 1][1])

    edge_cylinder.append(Edge(temp_vertex1, temp_vertex2))
    edge_cylinder.append(Edge(temp_vertex1, temp1_vertex1))
    edge_cylinder.append(Edge(temp1_vertex1, temp1_vertex2))

cylinder = Figure(edge_cylinder, [1, 0, 0], [-2, 2, -6, 1, 1.5, 0, 0, 1, 0])
cone = Figure(edge_cone, [0, 100, 0], [-5, 2, -6, 3, -1.5, 0, 0, 1, 0])
cube = Figure(edges_cube, [1, 0, 1], [-10, 2, -6, -1.6499988, -1.77999955, 0, 0, 1, 0])
pyramid = Figure(edges_pyramid, [1, 25, 0], [-2, 2, -6, -1.9699985, 0.36999992, 0, 0, 1, 0])

figures = [cube, pyramid, cone, cylinder]
#figures = []
figure_id = 0

window_width = 800  # размеры окна (ширина и высота)
window_height = 600
SCREEN_SIZE = (window_width, window_height)

app = DrawingWindow(root, width=window_width, height=window_height)  # создание окна для отрисови
app.pack(fill=BOTH, expand=YES)  # отобразить

root.bind('a', camera_plus_tx)
root.bind('d', camera_minus_tx)
root.bind('w', camera_plus_tz)
root.bind('s', camera_minus_tz)
root.bind('q', camera_plus_ty)
root.bind('e', camera_minus_ty)
root.bind('<Right>', camera_plus_ry)
root.bind('<Left>', camera_minus_ry)
root.bind('<Up>', camera_minus_rx)
root.bind('<Down>', camera_plus_rx)
root.bind('x', camera_plus_rz)
root.bind('z', camera_minus_rz)
root.bind('<KeyRelease>', camera_stop)

label_select_figure = Label(text="Выбор фигуры")
label_select_figure.place(x=685, y=0)
combo_select_figure = Combobox(app)
combo_select_figure['values'] = ("Куб", "Пирамида", "Конус", "Цилиндр")
combo_select_figure['state'] = 'readonly'
combo_select_figure.current(0)
combo_select_figure.place(x=655, y=25)

label_select_axis = Label(text="Перемещение по осям")
label_select_axis.place(x=660, y=50)

label_select_x = Label(text="x", width=2, height=1)
label_select_x.place(x=665, y=77)
button_plus_axes_x = Button(app, text="+", width=4)
button_plus_axes_x.place(x=690, y=75)
button_minus_axes_x = Button(app, text="-", width=4)
button_minus_axes_x.place(x=730, y=75)
button_plus_axes_x.bind('<Button-1>', minus_axes_x)
button_plus_axes_x.bind('<ButtonRelease-1>', figure_stop)
button_minus_axes_x.bind('<Button-1>', plus_axes_x)
button_minus_axes_x.bind('<ButtonRelease-1>', figure_stop)

label_select_y = Label(text="y", width=2, height=1)
label_select_y.place(x=665, y=102)
button_plus_axes_y = Button(app, text="+", width=4)
button_plus_axes_y.place(x=690, y=100)
button_minus_axes_y = Button(app, text="-", width=4)
button_minus_axes_y.place(x=730, y=100)
button_plus_axes_y.bind('<Button-1>', plus_axes_y)
button_plus_axes_y.bind('<ButtonRelease-1>', figure_stop)
button_minus_axes_y.bind('<Button-1>', minus_axes_y)
button_minus_axes_y.bind('<ButtonRelease-1>', figure_stop)

label_select_z = Label(text="z", width=2, height=1)
label_select_z.place(x=665, y=127)
button_plus_axes_z = Button(app, text="+", width=4)
button_plus_axes_z.place(x=690, y=125)
button_minus_axes_z = Button(app, text="-", width=4)
button_minus_axes_z.place(x=730, y=125)
button_plus_axes_z.bind('<Button-1>', minus_axes_z)
button_plus_axes_z.bind('<ButtonRelease-1>', figure_stop)
button_minus_axes_z.bind('<Button-1>', plus_axes_z)
button_minus_axes_z.bind('<ButtonRelease-1>', figure_stop)

label_select_axis = Label(text="Вращение по осям")
label_select_axis.place(x=665, y=155)

label_select_rx = Label(text="x", width=2, height=1)
label_select_rx.place(x=665, y=182)
button_plus_axes_rx = Button(app, text="+", width=4)
button_plus_axes_rx.place(x=690, y=180)
button_minus_axes_rx = Button(app, text="-", width=4)
button_minus_axes_rx.place(x=730, y=180)
button_plus_axes_rx.bind('<Button-1>', plus_axes_rx)
button_plus_axes_rx.bind('<ButtonRelease-1>', figure_stop)
button_minus_axes_rx.bind('<Button-1>', minus_axes_rx)
button_minus_axes_rx.bind('<ButtonRelease-1>', figure_stop)

label_select_ry = Label(text="y", width=2, height=1)
label_select_ry.place(x=665, y=207)
button_plus_axes_ry = Button(app, text="+", width=4)
button_plus_axes_ry.place(x=690, y=205)
button_minus_axes_ry = Button(app, text="-", width=4)
button_minus_axes_ry.place(x=730, y=205)
button_plus_axes_ry.bind('<Button-1>', plus_axes_ry)
button_plus_axes_ry.bind('<ButtonRelease-1>', figure_stop)
button_minus_axes_ry.bind('<Button-1>', minus_axes_ry)
button_minus_axes_ry.bind('<ButtonRelease-1>', figure_stop)

label_select_rz = Label(text="z", width=2, height=1)
label_select_rz.place(x=665, y=232)
button_plus_axes_rz = Button(app, text="+", width=4)
button_plus_axes_rz.place(x=690, y=230)
button_minus_axes_rz = Button(app, text="-", width=4)
button_minus_axes_rz.place(x=730, y=230)
button_plus_axes_rz.bind('<Button-1>', plus_axes_rz)
button_plus_axes_rz.bind('<ButtonRelease-1>', figure_stop)
button_minus_axes_rz.bind('<Button-1>', minus_axes_rz)
button_minus_axes_rz.bind('<ButtonRelease-1>', figure_stop)

label_select_axis = Label(text="Масштабирование")
label_select_axis.place(x=665, y=260)
label_select_sxyz = Label(text="xyz", width=3, height=1)
label_select_sxyz.place(x=665, y=285)
button_plus_axes_sxyz = Button(app, text="+", width=4)
button_plus_axes_sxyz.place(x=695, y=285)
button_minus_axes_sxyz = Button(app, text="-", width=4)
button_minus_axes_sxyz.place(x=735, y=285)
button_plus_axes_sxyz.bind('<Button-1>', plus_axes_sxyz)
button_plus_axes_sxyz.bind('<ButtonRelease-1>', figure_stop)
button_minus_axes_sxyz.bind('<Button-1>', minus_axes_sxyz)
button_minus_axes_sxyz.bind('<ButtonRelease-1>', figure_stop)

fill_figure = Button(app, text="Закрашивание", command=click_fill_figure)
fill_figure.place(x=695, y=570)

app.animate = 1
app.mainloop()
