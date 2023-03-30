from tkinter import *
from pyopengltk import OpenGLFrame
from OpenGL import GL, GLU
from tkinter.ttk import Entry
from random import uniform
import re


def is_valid(newval):
    return re.match("(^\d{0,3})|(^[+]?([.]\d+|\d+([.]\d+)?))$", newval) is not None


def curve(p0, p1, p2, p3, w0, w1, w2, w3, t_arr):
    len_weights = w0 + w1 + w2 + w3
    w0 = w0 / len_weights
    w1 = w1 / len_weights
    w2 = w2 / len_weights
    w3 = w3 / len_weights

    GL.glBegin(GL.GL_LINE_STRIP)

    for i in range(len(t_arr)):
        t = t_arr[i]
        up_x = w0 * p0[0] * (1 - t) ** 3 + 3 * w1 * p1[0] * t * (1 - t) ** 2 + 3 * w2 * p2[0] * t ** 2 * (1 - t) + w3 * \
               p3[0] * t ** 3
        down = w0 * (1 - t) ** 3 + 3 * w1 * t * (1 - t) ** 2 + 3 * w2 * t ** 2 * (1 - t) + w3 * t ** 3
        x = up_x / down

        up_y = w0 * p0[1] * (1 - t) ** 3 + 3 * w1 * p1[1] * t * (1 - t) ** 2 + 3 * w2 * p2[1] * t ** 2 * (1 - t) + w3 * \
               p3[1] * t ** 3
        y = up_y / down

        # t += 0.01

        GL.glVertex3d(x, y, 0)
    GL.glEnd()


def draw():  # отрисовка

    GL.glBegin(GL.GL_LINE_STRIP)  # непосредстенно отрисова виджета
    for i in range(len(control_points)):  # в цикле отрисовка вершин по координатам из списка
        GL.glColor4f(255, 0, 0, 0)  # установка цвета
        GL.glVertex3f(control_points[i][0], control_points[i][1], 0.0)
    GL.glEnd()

    w0 = entry_w0.get()
    w1 = entry_w1.get()
    w2 = entry_w2.get()
    w3 = entry_w3.get()
    w4 = entry_w4.get()
    w5 = entry_w5.get()

    if w0 != "" and w0 != "0" and w0 != "0.":
        w0 = float(w0)
        if w0 <= 100:
            weights[0] = w0
    if w1 != "" and w1 != "0" and w1 != "0.":
        w1 = float(w1)
        if w1 <= 100:
            weights[1] = w1
    if w2 != "" and w2 != "0" and w2 != "0.":
        w2 = float(w2)
        if w2 <= 100:
            weights[2] = w2
    if w3 != "" and w3 != "0" and w3 != "0.":
        w3 = float(w3)
        if w3 <= 100:
            weights[3] = w3
    if w4 != "" and w4 != "0" and w4 != "0.":
        w4 = float(w4)
        if w4 <= 100:
            weights[4] = w4
    if w5 != "" and w5 != "0" and w5 != "0.":
        w5 = float(w5)
        if w5 <= 100:
            weights[5] = w5

    GL.glColor4f(0, 0, 255, 0)

    curve(control_points[0], control_points[1], control_points[2], control_points[3], weights[0], weights[1],
          weights[2], weights[3], t1_arr)

    GL.glColor4f(0, 255, 0, 0)

    curve(control_points[1], control_points[2], control_points[3], control_points[4], weights[1], weights[2],
          weights[3], weights[4], t2_arr)

    GL.glColor4f(0, 255, 255, 0)

    curve(control_points[2], control_points[3], control_points[4], control_points[5], weights[2], weights[3],
          weights[4], weights[5], t3_arr)

    GL.glFlush()


def drag(event):
    canvas_item_id = event.widget.gettags("current")[0]

    mouse_x = app.winfo_pointerx() - app.winfo_rootx()
    mouse_y = app.winfo_pointery() - app.winfo_rooty()
    event.widget.place(x=mouse_x - 5, y=mouse_y - 5)

    control_points[int(canvas_item_id)] = [mouse_x, mouse_y]


class DrawingWindow(OpenGLFrame):  # создание класса на основе пакета pyopengltk

    def initgl(self):  # инициализация
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)  # очистка буфферов от цветов ~ очищение экарана
        GL.glClearColor(1, 1, 1, 0)  # задает цвет, в который окно будет окрашиваться при его очистке ~ очищение
        # цветопередачи
        GL.glMatrixMode(GL.GL_PROJECTION)  # матрица проекции (для проецирования 3D прсостранства в 2D)
        GL.glLoadIdentity()  # единичная матрица ~ очистика
        GLU.gluOrtho2D(0, window_width, window_height, 0)  # смещецение оси координат (чтобы не возникало искажения при
        # отрисовке

    def redraw(self):  # перерисовка
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        draw()  # функция для отрисовки


t1 = 0
t1_arr = [0]
while t1 < 1:
    temp = uniform(0, 0.001)
    t1 += temp
    t1_arr.append(t1)

t2 = 0
t2_arr = [0]
while t2 < 1:
    temp = uniform(0, 0.001)
    t2 += temp
    t2_arr.append(t2)

t3 = 0
t3_arr = [0]
while t3 < 1:
    temp = uniform(0, 0.001)
    t3 += temp
    t3_arr.append(t3)

root = Tk()  # главное окно
root.resizable(False, False)

window_width = 800  # размеры окна (ширина и высота)
window_height = 600
coordinates = []  # (координаты вершин)

control_points = [[100, 250], [200, 300], [270, 260], [400, 310], [470, 240], [580, 290]]
weights = [0.1, 0.3, 0.6, 1, 0.6, 0.3]

app = DrawingWindow(root, width=window_width, height=window_height)  # создание окна для отрисови
app.pack(fill=BOTH, expand=YES)  # отобразить
app.animate = 1  # для отрисовки в реальном времени

Point_0 = Canvas(app, width=5, height=5)
Point_0.place(x=control_points[0][0] - 5, y=control_points[0][1] - 5)
Point_0.create_rectangle(0, 0, 10, 10, fill="red", tags="0")

Point_1 = Canvas(app, width=5, height=5)
Point_1.place(x=control_points[1][0] - 5, y=control_points[1][1] - 5)
Point_1.create_rectangle(0, 0, 10, 10, fill="red", tags="1")

Point_2 = Canvas(app, width=5, height=5)
Point_2.place(x=control_points[2][0] - 5, y=control_points[2][1] - 5)
Point_2.create_rectangle(0, 0, 10, 10, fill="red", tags="2")

Point_3 = Canvas(app, width=5, height=5)
Point_3.place(x=control_points[3][0] - 5, y=control_points[3][1] - 5)
Point_3.create_rectangle(0, 0, 10, 10, fill="red", tags="3")

Point_4 = Canvas(app, width=5, height=5)
Point_4.place(x=control_points[4][0] - 5, y=control_points[4][1] - 5)
Point_4.create_rectangle(0, 0, 10, 10, fill="red", tags="4")

Point_5 = Canvas(app, width=5, height=5)
Point_5.place(x=control_points[5][0] - 5, y=control_points[5][1] - 5)
Point_5.create_rectangle(0, 0, 10, 10, fill="red", tags="5")

Point_0.bind("<B1-Motion>", drag)
Point_1.bind("<B1-Motion>", drag)
Point_2.bind("<B1-Motion>", drag)
Point_3.bind("<B1-Motion>", drag)
Point_4.bind("<B1-Motion>", drag)
Point_5.bind("<B1-Motion>", drag)

check_valid = (app.register(is_valid), "%P")
label_Entry = Label(text="Веса для контрольных точек")
label_Entry.place(x=0, y=0)

label_w0 = Label(text="w0 = ")
label_w0.place(x=0, y=23)
entry_w0 = Entry(width=10, validate="key", validatecommand=check_valid)
entry_w0.place(x=35, y=23)
entry_w0.insert(0, str(weights[0]))

label_w1 = Label(text="w1 = ")
label_w1.place(x=0, y=48)
entry_w1 = Entry(width=10, validate="key", validatecommand=check_valid)
entry_w1.place(x=35, y=48)
entry_w1.insert(0, str(weights[1]))

label_w2 = Label(text="w2 = ")
label_w2.place(x=0, y=73)
entry_w2 = Entry(width=10, validate="key", validatecommand=check_valid)
entry_w2.place(x=35, y=73)
entry_w2.insert(0, str(weights[2]))

label_w3 = Label(text="w3 = ")
label_w3.place(x=0, y=98)
entry_w3 = Entry(width=10, validate="key", validatecommand=check_valid)
entry_w3.place(x=35, y=98)
entry_w3.insert(0, str(weights[3]))

label_w4 = Label(text="w4 = ")
label_w4.place(x=0, y=123)
entry_w4 = Entry(width=10, validate="key", validatecommand=check_valid)
entry_w4.place(x=35, y=123)
entry_w4.insert(0, str(weights[4]))

label_w5 = Label(text="w5 = ")
label_w5.place(x=0, y=148)
entry_w5 = Entry(width=10, validate="key", validatecommand=check_valid)
entry_w5.place(x=35, y=148)
entry_w5.insert(0, str(weights[5]))

app.mainloop()  # запуск главного цикла
