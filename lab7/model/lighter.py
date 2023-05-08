from OpenGL.GL import *
from OpenGL.GLU import *
from model.identity_mat import identity_mat44


class Lighter:
    def __init__(self):
        self._rotation_mat = identity_mat44()  # матрица поворота
        self.position = [0.0, 0.0, 0.0, 0]
        self.tx = 0
        self.ty = 0
        self.tz = 0
        self.ry = 0
        self.rx = 0
        self.rz = 0
        self.light_sample = [0.0]
        self.constant = [0.0]
        self.linear = [0.0]
        self.quadratic = [0.0]
        self.cutoff = [0.0]
        self.exponent = [0.0]
        self.direction = [0.0, 0.0, 0.0, 1]
        self.ambient = [0.0, 0.0, 0.0, 1]
        self.diffuse = [1.0, 1.0, 1.0, 1.0]
        self.specular = [1.0, 1.0, 1.0, 1.0]
        self.model_ambient = [0.2, 0.2, 0.2, 1]
        self.model_local_viewer = [0]
        self.model_two_side = [0]
        self.face = [GL_FRONT_AND_BACK]
        self.shininess = [1.0]
        self.material_ambient = [0.2, 0.2, 0.2, 1]
        self.material_diffuse = [0.8, 0.8, 0.8, 1]
        self.material_specular = [0.0, 0.0, 0.0, 1]

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        x = self.position[0]
        y = self.position[1]
        z = self.position[2]

        glCullFace(self.face[0])
        glMaterialfv(self.face[0], GL_AMBIENT, self.material_ambient)  # определяют рассеянный цвет материала
        glMaterialfv(self.face[0], GL_DIFFUSE, self.material_diffuse)  # определяют цвет диффузного отражения материала
        glMaterialfv(self.face[0], GL_SPECULAR, self.material_specular)  # определяют цвет зеркального отражения
        # материала
        glMaterialfv(self.face[0], GL_SHININESS, self.shininess[0])  # определяет степень зеркального отражения
        # материала

        #glMaterialfv(GL_FRONT, GL_SPECULAR, (1, 1, 1, 1))
        #glMaterialfv(GL_FRONT, GL_SHININESS, 1)
        #glColorMaterial(self.face[0], GL_AMBIENT_AND_DIFFUSE)

        glLightfv(GL_LIGHT0, GL_AMBIENT, self.ambient)  # цвет фонового освещения
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.diffuse)  # цвет диффузного освещения
        glLightfv(GL_LIGHT0, GL_SPECULAR, self.specular)  # цвет зеркального отражения

        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, self.model_ambient)  # цвет глобального фонового света
        glLightModelfv(GL_LIGHT_MODEL_LOCAL_VIEWER, self.model_local_viewer)  # является ли точка наблюдения локальной
        # или удаленной
        glLightModelfv(GL_LIGHT_MODEL_TWO_SIDE, self.model_two_side)  # правильно ли происходит закрашивание обеих
        # сто-рон полигона

        if self.light_sample[0] == 0:

            glColor4f(0, 0, 255, 1)

            self.position[3] = 0

            glLightfv(GL_LIGHT0, GL_POSITION, self.position)
            glLightfv(GL_LIGHT0, GL_SPOT_CUTOFF, 180)

            glLineWidth(4)
            glBegin(GL_LINES)
            glVertex3f(0, 0, 0)
            glVertex3f(x, y, z)
            glEnd()

        elif self.light_sample[0] == 1:

            glColor4f(255, 255, 255, 1)

            self.position[3] = 1

            glLightfv(GL_LIGHT0, GL_POSITION, self.position)  # задает положение источника света в пространстве.
            # Чем дальше источник света от поверхности, тем больше затухание света.
            glLight(GL_LIGHT0, GL_CONSTANT_ATTENUATION, self.constant)  # задает постоянное затухание света в
            # зависимости от расстояния между источником света и поверхностью. Чем больше это значение,
            # тем меньше затухание.
            glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION, self.linear)  # задает линейное затухание света. Оно
            # увеличивает затухание света линейно в зависимости от расстояния между источником света и поверхностью
            glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, self.quadratic)  # задает квадратичное затухание света.
            # Оно увеличивает затухание света квадратично в зависимости от расстояния между источником света
            # и поверхностью.

            glPointSize(50)
            glBegin(GL_POINTS)
            glVertex3f(x, y, z)
            glEnd()

        elif self.light_sample[0] == 2:

            self.position[3] = 1

            direction = self.direction
            position = self.position

            glLightfv(GL_LIGHT0, GL_POSITION, position)
            glLightfv(GL_LIGHT0, GL_CONSTANT_ATTENUATION, self.constant)
            glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION, self.linear)
            glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, self.quadratic)

            glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, direction)  # направление света прожектора.
            glLightfv(GL_LIGHT0, GL_SPOT_CUTOFF, self.cutoff)  # угловая ширина светового луча.
            glLightfv(GL_LIGHT0, GL_SPOT_EXPONENT, self.exponent)  # концентрация светового луча.

            glPointSize(50)
            glBegin(GL_LINES)
            glColor4f(0, 255, 255, 1)
            glVertex3f(x, y, z)
            glColor4f(255, 255, 0, 1)
            glVertex3f(self.direction[0], self.direction[1], self.direction[2])
            glEnd()

            gluLookAt(-2, 2, -6, 0, 0, 0, 0, 1, 0)

        glPopMatrix()

    def render(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glMultMatrixf(self._rotation_mat)

        glPushMatrix()
        glLoadIdentity()
        self._rotation_mat = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix()
        self.draw()
        glPopMatrix()
