from OpenGL.GL import *
from OpenGL.GLU import gluLookAt
from model.identity_mat import identity_mat44


class Figure:
    def __init__(self, edges, color, coordinates):  # конструктору нужно передать ребра куба
        self._trans_mat = identity_mat44()  # матрица перемещения
        self._rotation_mat = identity_mat44()  # матрица поворота
        self._scale_mat = identity_mat44()  # матрица масштабирования
        self._edges = edges
        self.tx = 0  # координаты перемещения
        self.ty = 0
        self.tz = 0
        self.rx = 0  # углы поворота
        self.ry = 0
        self.rz = 0
        self.sxyz = 1  # масштабирование
        self.fill = False
        self.color = color
        self.coordinates = coordinates

    def change_fill(self):  # для закрашывания фигуры
        self.fill = not self.fill

    def draw(self):
        glPushMatrix()

        glColor3f(self.color[0], self.color[1], self.color[2])
        temp_vertexes = []

        for edge in self._edges:  # отрисовка ребер
            edge.draw_edge()
            temp_vertexes.append(edge.get_vertexes()[0])
            temp_vertexes.append(edge.get_vertexes()[1])

        if self.fill:  # закрашивание граней
            glBegin(GL_POLYGON)
            for i in range(len(temp_vertexes)):
                temp_vertexes[i].draw()
            glEnd()

        glPopMatrix()

    def render(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        gluLookAt(self.coordinates[0], self.coordinates[1], self.coordinates[2], self.coordinates[3],
                  self.coordinates[4], self.coordinates[5], self.coordinates[6], self.coordinates[7],
                  self.coordinates[8])  # перемещение куба
        # в начало координат (его центра)
        glMultMatrixf(self._trans_mat)  # перемножение матриц, чтобы сохранить преобразования
        glMultMatrixf(self._rotation_mat)
        glMultMatrixf(self._scale_mat)

        glPushMatrix()
        self.move_x()  # перемещение
        self.move_y()
        self.move_z()
        glPopMatrix()

        glPushMatrix()
        glLoadIdentity()
        # if local_rot:
        # self.rotate_local()
        # else:
        self.rotate_global()  # поворот
        self._rotation_mat = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix()

        glPushMatrix()
        glLoadIdentity()
        self.scale()  # масштабирование
        self._scale_mat = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix()

        self.draw()
        glPopMatrix()

    # def rotate(self):
    #   glPushMatrix()
    #  glLoadMatrixf(self._trans_mat)
    # glRotatef(0.5, 0, 1, 0)
    # self._trans_mat = glGetFloatv(GL_MODELVIEW_MATRIX)
    # glPopMatrix()

    def move_x(self):  # перемещение по x
        glLoadMatrixf(self._trans_mat)  # загрузка единичной матрицы
        glTranslatef(self.tx, 0, 0)  # перемещение на tx, 0, 0
        self._trans_mat = glGetFloatv(GL_MODELVIEW_MATRIX)  # чтобы получить новую матрицу моделирования и просмотра,
        # которая включает в себя поворот вокруг оси X, и сохраняет ее в переменную self._trans_mat

    def move_y(self):  # то же самое по y
        glLoadMatrixf(self._trans_mat)
        glTranslatef(0, self.ty, 0)
        self._trans_mat = glGetFloatv(GL_MODELVIEW_MATRIX)

    def move_z(self):  # то же самое по z
        glLoadMatrixf(self._trans_mat)
        glTranslatef(0, 0, self.tz)
        self._trans_mat = glGetFloatv(GL_MODELVIEW_MATRIX)

    # def rotate_local(self):  # вращает объект сначала вокруг его собственной системы координат, а затем применяет
    # глобальную матрицу преобразования. Это означает, что объект вращается сначала вокруг своей собственной оси,
    # а затем его новая ориентация преобразуется в глобальную систему координат.
    #    glMultMatrixf(self._rotation_mat)
    #   glRotatef(self.rx, 1, 0, 0)
    #  glRotatef(self.ry, 0, 1, 0)
    # glRotatef(self.rz, 0, 0, 1)

    def rotate_global(self):  # сначала поворачивает объект вокруг глобальной системы координат, а затем применяет
        # локальную матрицу преобразования. Это означает, что объект вращается вокруг глобальной оси, а затем его
        # новая ориентация преобразуется обратно в локальную систему координат.
        glRotatef(self.rx, 1, 0, 0)
        glRotatef(self.ry, 0, 1, 0)
        glRotatef(self.rz, 0, 0, 1)
        glMultMatrixf(self._rotation_mat)

    def scale(self):
        glScale(self.sxyz, self.sxyz, self.sxyz)
        glMultMatrixf(self._scale_mat)

    def stop(self):  # остановить все преобразования
        self.tx = 0
        self.ty = 0
        self.tz = 0
        self.ry = 0
        self.rx = 0
        self.rz = 0
        self.sxyz = 1
