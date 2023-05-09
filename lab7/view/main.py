from tkinter import *
from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLU import *
from model.axis import Axis
from model.camera import Camera
from model.vertex import Vertex
from model.edge import Edge
from model.figure import Figure
from model.lighter import Lighter
from tkinter.ttk import Combobox
from tkinter.ttk import Scale
import math


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


def get_light():
    temp_light = combo_select_light.get()
    global light_sample
    if temp_light == "Направленный":
        light_sample[0] = 0
    elif temp_light == "Точечный":
        light_sample[0] = 1
    elif temp_light == "Прожектор":
        light_sample[0] = 2


def set_light_default(event):
    if light_sample[0] == 0:
        position[0] = 0
        position[1] = 0
        position[2] = 0
    elif light_sample[0] == 1:
        position[0] = 0
        position[1] = 0
        position[2] = -13.20000000000001
    elif light_sample[0] == 2:
        direction[0] = -1.1102230246251565e-16
        direction[1] = 0.2999999999999999
        direction[2] = 0.0

        position[0] = 1.1102230246251565e-16
        position[1] = -0.6000000000000003
        position[2] = -10.500000000000004


def change_ambient():
    global check_ambient
    if check_ambient < 2:
        check_ambient += 1
    else:
        check_ambient = 0
    if check_ambient == 0:

        label_GL_AMBIENT.config(text="LIGHT_AMBIENT")
        label_GL_DIFFUSE.config(text="LIGHT_DIFFUSE")
        label_GL_SPECULAR.config(text="LIGHT_SPECULAR")

    elif check_ambient == 1:

        label_GL_AMBIENT.config(text="MODEL_AMBIENT")
    elif check_ambient == 2:
        label_GL_AMBIENT.config(text="MATERIAL_AMBIENT")
        label_GL_DIFFUSE.config(text="MATERIAL_DIFFUSE")
        label_GL_SPECULAR.config(text="MATERIAL_SPECULAR")


def change_local_viewer():
    if local_viewer[0] == 0:
        button_local_viewer.config(text="local_viewer_on")
        local_viewer[0] = 1
    else:
        button_local_viewer.config(text="local_viewer_off")
        local_viewer[0] = 0


def change_two_side():
    if two_side[0] == 0:
        button_two_side.config(text="two_side_on")
        two_side[0] = 1
    else:
        button_two_side.config(text="two_side_off")
        two_side[0] = 0


def change_face():
    global check_face
    if check_face < 2:
        check_face += 1
    else:
        check_face = 0
    if check_face == 0:
        button_face.config(text="FRONT_AND_BACK")
        face[0] = GL_FRONT_AND_BACK
    elif check_face == 1:
        button_face.config(text="FRONT")
        face[0] = GL_FRONT
    else:
        button_face.config(text="BACK")
        face[0] = GL_BACK


def change_cutoff(event):
    global check_cutoff
    check_cutoff = not check_cutoff
    if check_cutoff:
        button_GL_SPOT_CUTOFF.config(text="180")
    else:
        button_GL_SPOT_CUTOFF.config(text="<-")
    cutoff[0] = 180


def plus_lighter_direction_x(event):
    direction[0] += 0.3


def plus_lighter_x(event):
    position[0] += 0.3


def minus_lighter_direction_x(event):
    direction[0] -= 0.3


def minus_lighter_x(event):
    position[0] -= 0.3


def plus_lighter_direction_y(event):
    direction[1] += 0.3


def plus_lighter_y(event):
    position[1] += 0.3


def minus_lighter_direction_y(event):
    direction[1] -= 0.3


def minus_lighter_y(event):
    position[1] -= 0.3


def plus_lighter_direction_z(event):
    direction[2] += 0.3


def plus_lighter_z(event):
    position[2] += 0.3


def minus_lighter_direction_z(event):
    direction[2] -= 0.3


def minus_lighter_z(event):
    position[2] -= 0.3


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


def resize(width, height):
    glViewport(0, 0, width, height)


def change_select_matrix_projection():
    global select_matrix_projection
    select_matrix_projection = not select_matrix_projection
    if select_matrix_projection:
        label_select_matrix.config(text="Перспективная проекция")
    else:
        label_select_matrix.config(text="Параллельная проекция")


class DrawingWindow(OpenGLFrame):  # создание класса на основе пакета pyopengltk

    def initgl(self):  # инициализация
        resize(*SCREEN_SIZE)

        global light_sample
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_NORMALIZE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # glEnable(GL_BLEND)

    def redraw(self):  # перерисовка
        glEnable(GL_LIGHT0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if not select_matrix_projection:
            glOrtho(-4, 4, -4, 4, -150, 150)  # left right bottom top near far # ортографическая
            # left - координата левой границы видимой области вдоль оси X;
            # right - координата правой границы видимой области вдоль оси X;
            # bottom - координата нижней границы видимой области вдоль оси Y;
            # top - координата верхней границы видимой области вдоль оси Y;
            # near - координата ближней плоскости отсечения;
            # far - координата дальней плоскости отсечения.
        else:
            gluPerspective(40.0, float(SCREEN_SIZE[0] / SCREEN_SIZE[1]), 0.1, 50.0)  # перспективная
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()

        get_light()
        constant[0] = float(scale_GL_CONSTANT_ATTENUATION.get())
        linear[0] = float(scale_GL_LINEAR_ATTENUATION.get())
        quadratic[0] = float(scale_GL_QUADRATIC_ATTENUATION.get())
        if check_cutoff:
            cutoff[0] = float(scale_GL_SPOT_CUTOFF.get())
        exponent[0] = float(scale_GL_SPOT_EXPONENT.get())
        shininess[0] = float(scale_SHININESS.get())

        if check_ambient == 0:
            ambient[0] = float(scale_GL_AMBIENT_r.get())
            ambient[1] = float(scale_GL_AMBIENT_g.get())
            ambient[2] = float(scale_GL_AMBIENT_b.get())
            #ambient[3] = float(scale_GL_AMBIENT_a.get())

            diffuse[0] = float(scale_GL_DIFFUSE_r.get())
            diffuse[1] = float(scale_GL_DIFFUSE_g.get())
            diffuse[2] = float(scale_GL_DIFFUSE_b.get())
            #diffuse[3] = float(scale_GL_DIFFUSE_a.get())

            specular[0] = float(scale_GL_SPECULAR_r.get())
            specular[1] = float(scale_GL_SPECULAR_g.get())
            specular[2] = float(scale_GL_SPECULAR_b.get())
            #specular[3] = float(scale_GL_SPECULAR_a.get())
        elif check_ambient == 1:
            model_ambient[0] = float(scale_GL_AMBIENT_r.get())
            model_ambient[1] = float(scale_GL_AMBIENT_g.get())
            model_ambient[2] = float(scale_GL_AMBIENT_b.get())
            #model_ambient[3] = float(scale_GL_AMBIENT_a.get())
        elif check_ambient == 2:
            material_ambient[0] = float(scale_GL_AMBIENT_r.get())
            material_ambient[1] = float(scale_GL_AMBIENT_g.get())
            material_ambient[2] = float(scale_GL_AMBIENT_b.get())
            #material_ambient[3] = float(scale_GL_AMBIENT_a.get())

            material_diffuse[0] = float(scale_GL_DIFFUSE_r.get())
            material_diffuse[1] = float(scale_GL_DIFFUSE_g.get())
            material_diffuse[2] = float(scale_GL_DIFFUSE_b.get())
            #material_diffuse[3] = float(scale_GL_DIFFUSE_a.get())

            material_specular[0] = float(scale_GL_SPECULAR_r.get())
            material_specular[1] = float(scale_GL_SPECULAR_g.get())
            material_specular[2] = float(scale_GL_SPECULAR_b.get())
            #material_specular[3] = float(scale_GL_SPECULAR_a.get())

        camera.render()
        axis.render()
        lighter.render()

        get_figure()
        for i in range(len(figures)):
            figures[i].render()

        glPopMatrix()
        glDisable(GL_LIGHT0)


root = Tk()  # главное окно
root.resizable(False, False)

axis = Axis()
camera = Camera()
lighter = Lighter()

select_matrix_projection = True
position = lighter.position
light_sample = lighter.light_sample
constant = lighter.constant
linear = lighter.linear
quadratic = lighter.quadratic
cutoff = lighter.cutoff
check_cutoff = True
exponent = lighter.exponent
direction = lighter.direction
ambient = lighter.ambient
diffuse = lighter.diffuse
specular = lighter.specular
local_viewer = lighter.model_local_viewer
two_side = lighter.model_two_side
model_ambient = lighter.model_ambient
check_ambient = 0
face = lighter.face
check_face = 0
shininess = lighter.shininess
material_ambient = lighter.material_ambient
material_diffuse = lighter.material_diffuse
material_specular = lighter.material_specular

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
root.bind('r', set_light_default)

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

label_select_matrix = Label(text="Перспективная проекция")
label_select_matrix.place(x=0, y=0)
button_select_matrix_projection = Button(app, text="Сменить", command=change_select_matrix_projection)
button_select_matrix_projection.place(x=0, y=23)

label_select_light = Label(text="Тип источника света")
label_select_light.place(x=660, y=315)
combo_select_light = Combobox(app)
combo_select_light['values'] = ("Направленный", "Точечный", "Прожектор")
combo_select_light['state'] = 'readonly'
combo_select_light.current(0)
combo_select_light.place(x=660, y=340)

label_GL_POSITION = Label(text="POSITION")
label_GL_POSITION.place(x=690, y=365)

label_select_lighter_x = Label(text="x", width=2, height=1)
label_select_lighter_x.place(x=639, y=390)
button_plus_lighter_x = Button(app, text="+", width=1)
button_plus_lighter_x.place(x=657, y=390)
button_minus_lighter_x = Button(app, text="-", width=1)
button_minus_lighter_x.place(x=675, y=390)
button_plus_lighter_x.bind('<Button-1>', minus_lighter_x)
button_minus_lighter_x.bind('<Button-1>', plus_lighter_x)

label_select_lighter_y = Label(text="y", width=2, height=1)
label_select_lighter_y.place(x=693, y=390)
button_plus_lighter_y = Button(app, text="+", width=1)
button_plus_lighter_y.place(x=711, y=390)
button_minus_lighter_y = Button(app, text="-", width=1)
button_minus_lighter_y.place(x=729, y=390)
button_plus_lighter_y.bind('<Button-1>', plus_lighter_y)
button_minus_lighter_y.bind('<Button-1>', minus_lighter_y)

label_select_lighter_y = Label(text="z", width=2, height=1)
label_select_lighter_y.place(x=747, y=390)
button_plus_lighter_y = Button(app, text="+", width=1)
button_plus_lighter_y.place(x=765, y=390)
button_minus_lighter_y = Button(app, text="-", width=1)
button_minus_lighter_y.place(x=783, y=390)
button_plus_lighter_y.bind('<Button-1>', minus_lighter_z)
button_minus_lighter_y.bind('<Button-1>', plus_lighter_z)

label_GL_CONSTANT_ATTENUATION = Label(text="CONSTANT")
label_GL_CONSTANT_ATTENUATION.place(x=639, y=420)
scale_GL_CONSTANT_ATTENUATION = Scale(from_=0, to=1, orient=HORIZONTAL, value=0, length=85)
scale_GL_CONSTANT_ATTENUATION.place(x=710, y=420)

label_GL_LINEAR_ATTENUATION = Label(text="LINEAR")
label_GL_LINEAR_ATTENUATION.place(x=639, y=445)
scale_GL_LINEAR_ATTENUATION = Scale(from_=0, to=1, orient=HORIZONTAL, value=0, length=85)
scale_GL_LINEAR_ATTENUATION.place(x=710, y=445)

label_GL_QUADRATIC_ATTENUATION = Label(text="QUADRATIC")
label_GL_QUADRATIC_ATTENUATION.place(x=639, y=470)
scale_GL_QUADRATIC_ATTENUATION = Scale(from_=0, to=1, orient=HORIZONTAL, value=0, length=85)
scale_GL_QUADRATIC_ATTENUATION.place(x=710, y=470)

label_GL_SPOT_CUTOFF = Label(text="CUTOFF")
label_GL_SPOT_CUTOFF.place(x=639, y=495)
button_GL_SPOT_CUTOFF = Button(app, text="180", width=2, height=1)
button_GL_SPOT_CUTOFF.bind('<Button-1>', change_cutoff)
button_GL_SPOT_CUTOFF.place(x=690, y=495)
scale_GL_SPOT_CUTOFF = Scale(from_=0, to=90, orient=HORIZONTAL, value=0, length=80)
scale_GL_SPOT_CUTOFF.place(x=715, y=495)

label_GL_SPOT_EXPONENT = Label(text="EXPONENT")
label_GL_SPOT_EXPONENT.place(x=639, y=520)
scale_GL_SPOT_EXPONENT = Scale(from_=0, to=128, orient=HORIZONTAL, value=0, length=85)
scale_GL_SPOT_EXPONENT.place(x=710, y=520)

label_GL_SPOT_DIRECTION = Label(text="DIRECTION")
label_GL_SPOT_DIRECTION.place(x=690, y=545)

label_select_lighter_direction_x = Label(text="x", width=2, height=1)
label_select_lighter_direction_x.place(x=639, y=570)
button_plus_lighter_direction_x = Button(app, text="+", width=1)
button_plus_lighter_direction_x.place(x=657, y=570)
button_minus_lighter_direction_x = Button(app, text="-", width=1)
button_minus_lighter_direction_x.place(x=675, y=570)
button_plus_lighter_direction_x.bind('<Button-1>', minus_lighter_direction_x)
button_minus_lighter_direction_x.bind('<Button-1>', plus_lighter_direction_x)

label_select_lighter_direction_y = Label(text="y", width=2, height=1)
label_select_lighter_direction_y.place(x=693, y=570)
button_plus_lighter_direction_y = Button(app, text="+", width=1)
button_plus_lighter_direction_y.place(x=711, y=570)
button_minus_lighter_direction_y = Button(app, text="-", width=1)
button_minus_lighter_direction_y.place(x=729, y=570)
button_plus_lighter_direction_y.bind('<Button-1>', plus_lighter_direction_y)
button_minus_lighter_direction_y.bind('<Button-1>', minus_lighter_direction_y)

label_select_lighter_direction_y = Label(text="z", width=2, height=1)
label_select_lighter_direction_y.place(x=747, y=570)
button_plus_lighter_direction_y = Button(app, text="+", width=1)
button_plus_lighter_direction_y.place(x=765, y=570)
button_minus_lighter_direction_y = Button(app, text="-", width=1)
button_minus_lighter_direction_y.place(x=783, y=570)
button_plus_lighter_direction_y.bind('<Button-1>', minus_lighter_direction_z)
button_minus_lighter_direction_y.bind('<Button-1>', plus_lighter_direction_z)

label_GL_AMBIENT = Label(text="LIGHT_AMBIENT")
label_GL_AMBIENT.place(x=0, y=50)

label_GL_AMBIENT_r = Label(text="R")
label_GL_AMBIENT_r.place(x=0, y=104)
scale_GL_AMBIENT_r = Scale(from_=-1, to=1, orient=HORIZONTAL, value=0, length=50)
scale_GL_AMBIENT_r.place(x=15, y=102)

label_GL_AMBIENT_g = Label(text="G")
label_GL_AMBIENT_g.place(x=0, y=129)
scale_GL_AMBIENT_g = Scale(from_=-1, to=1, orient=HORIZONTAL, value=0, length=50)
scale_GL_AMBIENT_g.place(x=15, y=127)

label_GL_AMBIENT_b = Label(text="B")
label_GL_AMBIENT_b.place(x=0, y=154)
scale_GL_AMBIENT_b = Scale(from_=-1, to=1, orient=HORIZONTAL, value=0, length=50)
scale_GL_AMBIENT_b.place(x=15, y=152)

#label_GL_AMBIENT_a = Label(text="A")
#label_GL_AMBIENT_a.place(x=0, y=179)
#scale_GL_AMBIENT_a = Scale(from_=-1, to=1, orient=HORIZONTAL, value=1, length=50)
#scale_GL_AMBIENT_a.place(x=15, y=177)

label_GL_DIFFUSE = Label(text="LIGHT_DIFFUSE")
label_GL_DIFFUSE.place(x=0, y=205)

label_GL_DIFFUSE_r = Label(text="R")
label_GL_DIFFUSE_r.place(x=0, y=229)
scale_GL_DIFFUSE_r = Scale(from_=-1, to=1, orient=HORIZONTAL, value=1, length=50)
scale_GL_DIFFUSE_r.place(x=15, y=227)

label_GL_DIFFUSE_g = Label(text="G")
label_GL_DIFFUSE_g.place(x=0, y=254)
scale_GL_DIFFUSE_g = Scale(from_=-1, to=1, orient=HORIZONTAL, value=1, length=50)
scale_GL_DIFFUSE_g.place(x=15, y=252)

label_GL_DIFFUSE_b = Label(text="B")
label_GL_DIFFUSE_b.place(x=0, y=279)
scale_GL_DIFFUSE_b = Scale(from_=-1, to=1, orient=HORIZONTAL, value=1, length=50)
scale_GL_DIFFUSE_b.place(x=15, y=277)

#label_GL_DIFFUSE_a = Label(text="A")
#label_GL_DIFFUSE_a.place(x=0, y=304)
#scale_GL_DIFFUSE_a = Scale(from_=-1, to=1, orient=HORIZONTAL, value=1, length=50)
#scale_GL_DIFFUSE_a.place(x=15, y=302)

label_GL_SPECULAR = Label(text="LIGHT_SPECULAR")
label_GL_SPECULAR.place(x=0, y=330)

label_GL_SPECULAR_r = Label(text="R")
label_GL_SPECULAR_r.place(x=0, y=354)
scale_GL_SPECULAR_r = Scale(from_=-1, to=1, orient=HORIZONTAL, value=1, length=50)
scale_GL_SPECULAR_r.place(x=15, y=352)

label_GL_SPECULAR_g = Label(text="G")
label_GL_SPECULAR_g.place(x=0, y=379)
scale_GL_SPECULAR_g = Scale(from_=-1, to=1, orient=HORIZONTAL, value=1, length=50)
scale_GL_SPECULAR_g.place(x=15, y=377)

label_GL_SPECULAR_b = Label(text="B")
label_GL_SPECULAR_b.place(x=0, y=404)
scale_GL_SPECULAR_b = Scale(from_=-1, to=1, orient=HORIZONTAL, value=1, length=50)
scale_GL_SPECULAR_b.place(x=15, y=402)

#label_GL_SPECULAR_a = Label(text="A")
#label_GL_SPECULAR_a.place(x=0, y=429)
#scale_GL_SPECULAR_a = Scale(from_=-1, to=1, orient=HORIZONTAL, value=1, length=50)
#scale_GL_SPECULAR_a.place(x=15, y=427)

button_switch_model_light = Button(text="Сменить", command=change_ambient)
button_switch_model_light.place(x=0, y=74)

button_local_viewer = Button(text="local_viewer_off", command=change_local_viewer)
button_local_viewer.place(x=0, y=455)

button_two_side = Button(text="two_side_off", command=change_two_side)
button_two_side.place(x=0, y=481)

button_face = Button(text="FRONT_AND_BACK", command=change_face)
button_face.place(x=0, y=507)

label_SHININESS = Label(text="SHININESS")
label_SHININESS.place(x=0, y=541)

scale_SHININESS = Scale(from_=0, to=128, orient=HORIZONTAL, value=1, length=47)
scale_SHININESS.place(x=65, y=538)

fill_figure = Button(app, text="Закрашивание", command=click_fill_figure)
fill_figure.place(x=0, y=570)

app.animate = 1
app.mainloop()
