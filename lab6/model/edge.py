from OpenGL.GL import *


class Edge:  # класс под зарисовку ребер
    def __init__(self, vertex1, vertex2):  # конструктор принимает 2 вершины для ребра
        self._vertex1 = vertex1
        self._vertex2 = vertex2

    def draw_edge(self):  # рисует сплошнуб линию через класс vertex
        glLineWidth(2)
        glBegin(GL_LINES)
        self._vertex1.draw()
        self._vertex2.draw()
        glEnd()

    def draw_dotted_edge(self):  # рисует точечную линию через класс vertex
        glPushAttrib(GL_ENABLE_BIT)
        glLineStipple(1, 0x1111)
        glEnable(GL_LINE_STIPPLE)
        self.draw_edge()
        glPopAttrib()

    def get_vertexes(self):  # возвращает вершины ребра
        return [self._vertex1, self._vertex2]
