from model.edge import Edge
from OpenGL.GL import glPushMatrix, glMatrixMode, glColor4f, glPopMatrix, GL_MODELVIEW
from model.identity_mat import identity_mat44
from model.vertex import Vertex


class Axis:
    def __init__(self):  # класс под зарисовку осей
        self._identity_mat = identity_mat44()  # единичная матрица 4x4
        self._vertices = [Vertex(0, 0, 0),  # вершины под оси
                          Vertex(-100, 0, 0),
                          Vertex(0, 100, 0),
                          Vertex(0, 0, -100),
                          Vertex(100, 0, 0),
                          Vertex(0, -100, 0),
                          Vertex(0, 0, 100),
                          ]
        self._edges = [(0, 1),  # для отрисовки ребер
                       (0, 2),
                       (0, 3),
                       (0, 4),
                       (0, 5),
                       (0, 6),
                       ]

    def draw(self):

        glMatrixMode(GL_MODELVIEW)  # Эта функция сообщает OpenGL, что следующие операции над матрицами будут
        # применяться к матрице моделирования-вида, которая определяет положение и ориентацию камеры, а также положение
        # и ориентацию всех объектов, отображаемых на экране.
        glPushMatrix()  # Вызов glPushMatrix() позволяет сохранить текущее состояние матрицы в стеке матриц OpenGL,
        # чтобы его можно было восстановить позже с помощью функции glPopMatrix()
        #gluLookAt(-2, 2, -6, 0, 0, 0, 0, 1, 0)  # Таким образом, данная функция устанавливает камеру в точке (-2, 2, -6)
        # с направлением взгляда на точку (0, 0, 0) и считает, что направление "вверх" камеры определяется вектором
        # (0, 1, 0). Это позволяет создать 3D-вид, который можно использовать для рендеринга сцены с заданной камерой.

        # glMultMatrixf(self._identity_mat)
        color = 0
        colors = [(1, 0, 0),  # цвета осей
                  (1, 1, 0),
                  (0, 1, 1),
                  (1, 0, 0),
                  (1, 1, 0),
                  (0, 1, 1)
                  ]

        for edge in self._edges:
            glColor4f(colors[color][0], colors[color][1], colors[color][2], 1)
            if color > 2:  # отрицательные полуоси красятся точечными линиями
                Edge.draw_dotted_edge(Edge(self._vertices[edge[0]], self._vertices[edge[1]]))
            else:  # положительные полуоси красятся сплошными линиями
                Edge.draw_edge(Edge(self._vertices[edge[0]], self._vertices[edge[1]]))
            color += 1

        glPopMatrix()

    def render(self):
        self.draw()
