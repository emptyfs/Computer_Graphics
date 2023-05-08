from OpenGL.GL import *

from model.identity_mat import identity_mat44


class Camera:
    def __init__(self):
        self._identity_mat = identity_mat44()  # матрица преобразований (изначально единичная матрица 4x4)
        self.tx = 0  # координаты по перемещению
        self.ty = 0
        self.tz = 0
        self.ry = 0  # координаты по вращению
        self.rx = 0
        self.rz = 0

    def rotate_x(self):  # поворот фигуры по оси x
        glLoadIdentity()  # загрузка единичной матрицы
        glRotatef(self.rx, 1, 0, 0)  # поворот вокруг оси X на угол rx
        glMultMatrixf(self._identity_mat)  # перемножает текущую матрицу с единичной матрицей,
        # чтобы сохранить текущее положение объекта.
        self._identity_mat = glGetFloatv(GL_MODELVIEW_MATRIX)  # чтобы получить новую матрицу моделирования и просмотра,
        # которая включает в себя поворот вокруг оси X, и сохраняет ее в переменную self._identity_mat

    def rotate_y(self):  # то же самое, но по оси y
        glLoadIdentity()
        glRotatef(self.ry, 0, 1, 0)
        glMultMatrixf(self._identity_mat)
        self._identity_mat = glGetFloatv(GL_MODELVIEW_MATRIX)

    def rotate_z(self):  # то же самое, но по оси z
        glLoadIdentity()
        glRotatef(self.rz, 0, 0, 1)
        glMultMatrixf(self._identity_mat)
        self._identity_mat = glGetFloatv(GL_MODELVIEW_MATRIX)

    def translate(self):  # перемещение фигуры
        glLoadIdentity()  # загрузка единичной матрицы
        glTranslatef(self.tx, self.ty, self.tz)  # перемещение на tx, ty, tz
        glMultMatrixf(self._identity_mat)  # перемножает текущую матрицу с единичной матрицей,
        # чтобы сохранить текущее положение объекта.
        self._identity_mat = glGetFloatv(GL_MODELVIEW_MATRIX)  # чтобы получить новую матрицу моделирования и просмотра,
        # которая включает в себя поворот вокруг оси X, и сохраняет ее в переменную self._identity_mat

    def render(self):  # рендер измененного объекта
        self.translate()
        self.rotate_y()
        self.rotate_x()
        self.rotate_z()
