import math
from OpenGL import GL
import OpenGL.GL.shaders
import ctypes
import numpy
import pyopengltk
import tkinter as tk


def compileShader(source, shaderType):  # принимает (код шейдера, тип шейдера), возвращает скомпилированный шейдер
    shader = GL.glCreateShader(shaderType)  # создание объекта шейдера (принимает тип создаваемого шейдера)
    GL.glShaderSource(shader, source)  # загрузка кода в созданный объект шейдера
    GL.glCompileShader(shader)  # компиляция кода, загруженного ранее в объект шейдера
    return shader


vertex_shader = """
in vec3 position;
varying vec3 vertex_color;
void main()
{
   gl_Position = vec4(position, 1.0);
   vertex_color = vec4(0.0f, 1.0f, 1.0f, 1.0f);
}
"""

fragment_shader = """
varying vec3 vertex_color;
uniform float alpha;
void main()
{
   gl_FragColor = vec4(vertex_color, alpha);
}
"""


def create_object(shader):  # принимает программу шейдеров, возвращает вершинны массив
    vertex_array_object = GL.glGenVertexArrays(1)  # создание вершинного массива (количество объектов - 1)
    GL.glBindVertexArray(vertex_array_object)  # связывание вершинного массива с текущим контекстом (при связывании
    # все последующие операции с вершинными массивами будут использовать вершинные данные, указанные в этом массиве

    vertex_buffer = GL.glGenBuffers(1)  # генерация идентификаторов буферов для хранения данных в памяти видеокарты
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vertex_buffer)  # связывание буфера с текущим контекстом

    position = GL.glGetAttribLocation(shader, 'position')  # получаем индекс атрибута вершины в шейдере по имени
    # (расположение вершин)
    GL.glEnableVertexAttribArray(position)  # принимает индекс атрибута вершины и включает использование массива
    # атрибутов вершин, связанных с этим индексом, в процессе рисования графических примитивов.
    GL.glVertexAttribPointer(position, 3, GL.GL_FLOAT, False, 0, ctypes.c_void_p(0))  # описывает формат массива
    # атрибутов вершин и указывает OpenGL, как использовать эти атрибуты при рисовании графических примитивов.
    # position - индекс атрибута вершины, для которого мы хотим описать формат массива
    # 3 - количество компонентов в атрибуте вершины (для x,y,z - 3)
    # GL.GL_FLOAT - тип данных компонентов в атрибуте
    # False - указывает, должны ли значения атрибутов быть нормализованы между 0 и 1
    # 0 - количество байт между двумя соседними атрибутами вершин
    # ctypes.c_void_p(0) - смещение от начала вершины до начала первого компонента атрибута вершины

    vs = vertices.tobytes()
    GL.glBufferData(GL.GL_ARRAY_BUFFER, len(vs), vs, GL.GL_STATIC_DRAW)  # для передачи вершинных данных в буфер объекта
    #отвязываем от контекста
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(position)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object


class ShaderFrame(pyopengltk.OpenGLFrame):

    def initgl(self):
        GL.glClearColor(1.0, 1.0, 1.0, 1.0)
        GL.glEnable(GL.GL_DEPTH_TEST)  # буфер глубины (z-координата) (для 3D)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glEnable(GL.GL_BLEND)

        self.shader = GL.shaders.compileProgram(  # создание шейдерной программы
            #  Функция shaders.compileProgram() компилирует заданные шейдеры и связывает их вместе для создания
            #  программы шейдеров. Она принимает два аргумента - объекты вершинного и фрагментного шейдеров
            compileShader(vertex_shader, GL.GL_VERTEX_SHADER),  # компилируем вершинный шейдер
            compileShader(fragment_shader, GL.GL_FRAGMENT_SHADER)  # компилируем фрагментный шейдер
        )

        self.vertex_array_object = create_object(self.shader)
        self.alpha = 1

    def redraw(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        vertexColorLocation = GL.glGetUniformLocation(self.shader, "alpha")
        if self.alpha != 0:
            self.alpha -= 0.001

        GL.glUseProgram(self.shader)  # Вызов функции glUseProgram устанавливает программу шейдеров, которая
        # будет использоваться для отрисовки графики на экране.
        GL.glUniform1f(vertexColorLocation, self.alpha)
        GL.glBindVertexArray(self.vertex_array_object)
        GL.glDrawArrays(GL.GL_POLYGON, 0, len(vertices))  # отрисовка примитивов
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)


def createCircle(shift_x, shift_y, R):
    global vertices
    steps = 2000
    angle = math.pi * 2 / steps

    for i in range(steps):
        newX = R * math.sin(angle * i) + shift_x
        newY = -R * math.cos(angle * i) + shift_y
        vertices = numpy.append(vertices, [newX, newY, 0]).astype(numpy.float32)


root = tk.Tk()

vertices = numpy.array([[0, 0, 0.0]]).astype(numpy.float32)

createCircle(0, 0, 0.1)
createCircle(0, 0.12, 0.1)
createCircle(0.1, 0.05, 0.1)
createCircle(0.1, -0.05, 0.1)
createCircle(0, -0.1, 0.1)
createCircle(-0.1, 0.05, 0.1)
createCircle(-0.1, -0.05, 0.1)

app = ShaderFrame(root, width=800, height=600)
app.pack(fill=tk.BOTH, expand=tk.YES)
app.after(100, app.printContext)
app.animate = 1000 // 60
app.animate = 1
app.mainloop()
