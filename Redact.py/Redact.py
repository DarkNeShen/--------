import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFrame, QWidget, QVBoxLayout,
    QToolBar, QAction, QColorDialog
)
from PyQt5.QtCore import QPoint, Qt, QRect
from PyQt5 import QtGui

class Geometry:
    def __init__(self, x: int, y: int, color=Qt.black):
        self.center = QPoint(x, y)
        self.color = color
        self._state = False

    def resize(self, f:float, bounds: QRect):
        pass
    def move(self, dx: int, dy: int, bounds: QRect):

        pass

    def Is_in(self, point: QPoint) -> bool:
        raise NotImplementedError

    def draw(self, painter: QtGui.QPainter):
        raise NotImplementedError

    def Replace_state(self):
        self._state = not self._state

    def bas_state(self):
        self._state = False

    def is_state(self) -> bool:
        return self._state

    def set_color(self, color):
        self.color = color



class Circle(Geometry):
    r = 20
    min=5
    max = 60
    def Is_in(self, point: QPoint) -> bool:
        dx = self.center.x() - point.x()
        dy = self.center.y() - point.y()
        return dx * dx + dy * dy <= self.r * self.r
    def resize(self, factor: float, bounds: QRect) -> bool:
        new_r = self.r * factor
        if not (self.min <= new_r <= self.max):
            return False

        left = self.center.x() - new_r
        right = self.center.x() + new_r
        top = self.center.y() - new_r
        bottom = self.center.y() + new_r

        if left >= 0 and top >= 0 and right <= bounds.width() and bottom <= bounds.height():
            self.r = int(new_r)
            return True
        return False
    def draw(self, painter: QtGui.QPainter):
        pen_color = Qt.red if self._state else self.color
        painter.setPen(pen_color)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(self.center, self.r, self.r)

    def move(self, dx: int, dy: int, bounds: QRect):
        new_x = max(self.r, min(self.center.x() + dx, bounds.width() - self.r))
        new_y = max(self.r, min(self.center.y() + dy, bounds.height() - self.r))
        self.center = QPoint(new_x, new_y)


class Rects(Geometry):
    width = 40
    height = 40
    max = 100
    min = 10
    def resize(self, factor: float, bounds: QRect) -> bool:
        new_w = self.width * factor
        new_h = self.height * factor
        if not (self.min <= new_w <= self.max and self.min <= new_h <= self.max):
            return False

        half_w = new_w / 2
        half_h = new_h / 2
        left = self.center.x() - half_w
        right = self.center.x() + half_w
        top = self.center.y() - half_h
        bottom = self.center.y() + half_h

        if left >= 0 and top >= 0 and right <= bounds.width() and bottom <= bounds.height():
            self.width = int(new_w)
            self.height = int(new_h)
            return True
        return False
    def Is_in(self, point: QPoint) -> bool:
        left = self.center.x() - self.width // 2
        right = self.center.x() + self.width // 2
        top = self.center.y() - self.height // 2
        bottom = self.center.y() + self.height // 2
        return left <= point.x() <= right and top <= point.y() <= bottom

    def draw(self, painter: QtGui.QPainter):
        pen_color = Qt.red if self._state else self.color
        painter.setPen(pen_color)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(
            self.center.x() - self.width // 2,
            self.center.y() - self.height // 2,
            self.width, self.height
        )

    def move(self, dx: int, dy: int, bounds: QRect):
        half_w = self.width // 2
        half_h = self.height // 2
        new_x = max(half_w, min(self.center.x() + dx, bounds.width() - half_w))
        new_y = max(half_h, min(self.center.y() + dy, bounds.height() - half_h))
        self.center = QPoint(new_x, new_y)


class Rectangle(Geometry):
    width = 60
    height = 30
    min= 10
    max = 200

    def resize(self, factor: float, bounds: QRect) -> bool:
        new_w = self.width * factor
        new_h = self.height * factor
        if not (self.min <= new_w <= self.max and self.min <= new_h <= self.max):
            return False

        half_w = new_w / 2
        half_h = new_h / 2
        left = self.center.x() - half_w
        right = self.center.x() + half_w
        top = self.center.y() - half_h
        bottom = self.center.y() + half_h

        if left >= 0 and top >= 0 and right <= bounds.width() and bottom <= bounds.height():
            self.width = int(new_w)
            self.height = int(new_h)
            return True
        return False
    def Is_in(self, point: QPoint) -> bool:
        left = self.center.x() - self.width // 2
        right = self.center.x() + self.width // 2
        top = self.center.y() - self.height // 2
        bottom = self.center.y() + self.height // 2
        return left <= point.x() <= right and top <= point.y() <= bottom

    def draw(self, painter: QtGui.QPainter):
        pen_color = Qt.red if self._state else self.color
        painter.setPen(pen_color)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(
            self.center.x() - self.width // 2,
            self.center.y() - self.height // 2,
            self.width, self.height
        )

    def move(self, dx: int, dy: int, bounds: QRect):
        half_w = self.width // 2
        half_h = self.height // 2
        new_x = max(half_w, min(self.center.x() + dx, bounds.width() - half_w))
        new_y = max(half_h, min(self.center.y() + dy, bounds.height() - half_h))
        self.center = QPoint(new_x, new_y)


class Ellipse(Geometry):
    rx = 30
    ry = 20
    min = 5
    max = 100

    def resize(self, factor: float, bounds: QRect) -> bool:
        new_rx = self.rx * factor
        new_ry = self.ry * factor
        if not (self.min <= new_rx <= self.max and self.min <= new_ry <= self.max):
            return False

        left = self.center.x() - new_rx
        right = self.center.x() + new_rx
        top = self.center.y() - new_ry
        bottom = self.center.y() + new_ry

        if left >= 0 and top >= 0 and right <= bounds.width() and bottom <= bounds.height():
            self.rx = int(new_rx)
            self.ry = int(new_ry)
            return True
        return False
    def Is_in(self, point: QPoint) -> bool:
        dx = (point.x() - self.center.x()) / self.rx
        dy = (point.y() - self.center.y()) / self.ry
        return dx * dx + dy * dy <= 1

    def draw(self, painter: QtGui.QPainter):
        pen_color = Qt.red if self._state else self.color
        painter.setPen(pen_color)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(
            self.center.x() - self.rx,
            self.center.y() - self.ry,
            2 * self.rx,
            2 * self.ry
        )

    def move(self, dx: int, dy: int, bounds: QRect):
        new_x = max(self.rx, min(self.center.x() + dx, bounds.width() - self.rx))
        new_y = max(self.ry, min(self.center.y() + dy, bounds.height() - self.ry))
        self.center = QPoint(new_x, new_y)


class Tringl(Geometry):
    size = 40
    min = 10
    max = 150

  

    def resize(self, factor: float, bounds: QRect) -> bool:
        new_size = self.size * factor
        if not (self.min <= new_size <= self.max):
            return False

        half = new_size / 2
        left = self.center.x() - half
        right = self.center.x() + half
        top = self.center.y() - half
        bottom = self.center.y() + half

        if left >= 0 and top >= 0 and right <= bounds.width() and bottom <= bounds.height():
            self.size = int(new_size)
            return True
        return False
    def Is_in(self, point: QPoint) -> bool:
        
        left = self.center.x() - self.size // 2
        right = self.center.x() + self.size // 2
        top = self.center.y() - self.size // 2
        bottom = self.center.y() + self.size // 2
        return left <= point.x() <= right and top <= point.y() <= bottom

    def draw(self, painter: QtGui.QPainter):
        pen_color = Qt.red if self._state else self.color
        painter.setPen(pen_color)
        painter.setBrush(Qt.NoBrush)
        points = [
            QPoint(self.center.x(), self.center.y() - self.size // 2),
            QPoint(self.center.x() - self.size // 2, self.center.y() + self.size // 2),
            QPoint(self.center.x() + self.size // 2, self.center.y() + self.size // 2),
        ]
        painter.drawPolygon(points)

    def move(self, dx: int, dy: int, bounds: QRect):
        half = self.size // 2
        new_x = max(half, min(self.center.x() + dx, bounds.width() - half))
        new_y = max(half, min(self.center.y() + dy, bounds.height() - half))
        self.center = QPoint(new_x, new_y)


class Line(Geometry):
    length = 50
    min = 10
    max = 300

    def resize(self, factor: float, bounds: QRect) -> bool:
        new_len = self.length * factor
        if not (self.min <= new_len <= self.max):
            return False

        left = self.center.x()
        right = self.center.x() + new_len
        top = self.center.y() - 2
        bottom = self.center.y() + 2

        if left >= 0 and top >= 0 and right <= bounds.width() and bottom <= bounds.height():
            self.length = int(new_len)
            return True
        return False
    def Is_in(self, point: QPoint) -> bool:
        
                self.center.x() <= point.x() <= self.center.x() + self.length

    def draw(self, painter: QtGui.QPainter):
        pen_color = Qt.red if self._state else self.color
        painter.setPen(pen_color)
        painter.setBrush(Qt.NoBrush)
        painter.drawLine(self.center, QPoint(self.center.x() + self.length, self.center.y()))

    def move(self, dx: int, dy: int, bounds: QRect):
        new_x = max(0, min(self.center.x() + dx, bounds.width() - self.length))
        new_y = max(0, min(self.center.y() + dy, bounds.height()))
        self.center = QPoint(new_x, new_y)


class Container:
    def __init__(self):
        self._cont = []

    def add(self, geom):
        self._cont.append(geom)
    def resize_selected(self, f: float,bounds:QRect):
        for s in self.get_selected():
            s.resize(f,bounds)
    def return_cont(self):
        return self._cont
    def get_selected(self):
        return [s for s in self._cont if s.is_state()]
    def set_color(self, color):
        for s in self.get_selected():
            s.set_color(color)

    def remove_cont(self):
        self._cont = [s for s in self._cont if not s.is_state()]

    def base_state(self):
        for s in self._cont:
            s.bas_state()

    def Popal(self, point: QPoint, ctrl: bool):
        
        for geom in reversed(self._cont):
            if geom.Is_in(point):
                if not ctrl:
                    self.base_state()
                geom.Replace_state()
                return True
       
        if not ctrl:
            self.base_state()
        return False

    def move_selected(self, dx: int, dy: int, bounds: QRect):
        for s in self.get_selected():
            s.move(dx, dy, bounds)



class Drawing(QFrame):
    def __init__(self, cont: Container):
        super().__init__()
        self.cont = cont
        self.object = Circle
        self.setFocusPolicy(Qt.StrongFocus)

    def set_obj(self, tool_class):
        self.object = tool_class

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        for c in self.cont.return_cont():
            c.draw(painter)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            ctrl = bool(event.modifiers() & Qt.ControlModifier)
            popal = self.cont.Popal(event.pos(), ctrl)
            if not popal:
                nes_geom = self.object(event.x(), event.y())
                self.cont.add(nes_geom)
            self.update()

    def keyPressEvent(self, event):
        selected = self.cont.get_selected()
        if not selected:
            return

        dx, dy = 0, 0
        factor = None

        if event.key() == Qt.Key_Left:
            dx = -5
        elif event.key() == Qt.Key_Right:
            dx = 5
        elif event.key() == Qt.Key_Up:
            dy = -5
        elif event.key() == Qt.Key_Down:
            dy = 5
        elif event.key() == Qt.Key_Delete:
            self.cont.remove_cont()
            self.update()
            return
        elif event.key() == Qt.Key_C:
            color = QColorDialog.getColor()
            if color.isValid():
                self.cont.set_color(color)
            self.update()
            return
        elif event.key() == Qt.Key_Plus or event.key() == Qt.Key_Equal:
        
            factor = 1.2
        elif event.key() == Qt.Key_Minus:
            factor = 0.8
        else:
            super().keyPressEvent(event)
            return

        if dx != 0 or dy != 0:
            bounds = self.rect()
            self.cont.move_selected(dx, dy, bounds)
        elif factor is not None:
            bounds = self.rect()
            self.cont.resize_selected(factor,bounds)

        self.update()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа 4")
        self.setGeometry(300, 200, 800, 600)

        self.cont = Container()
        self.drawing = Drawing(self.cont)

        layout = QVBoxLayout()
        layout.addWidget(self.drawing)

        toolbar = QToolBar()
        self.addToolBar(toolbar)

        tools = [
            ("Круг", Circle),
            ("Квадрат", Rects),
            ("Прямоугольник", Rectangle),
            ("Эллипс", Ellipse),
            ("Треугольник", Tringl),
            ("Линия", Line)
        ]

        for name, cls in tools:
            action = QAction(name, self)
            action.triggered.connect(lambda ch, c=cls: self.drawing.set_obj(c))
            toolbar.addAction(action)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.drawing.setFocus()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())