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

    def move(self, dx: int, dy: int, bounds: QRect):
        old_center = self.center
        self.center = QPoint(self.center.x() + dx, self.center.y() + dy)
        if not self.is_in_obvodka(bounds):
            self.center = old_center

    def resize(self, f: float, bounds: QRect) -> bool:
        return False

    def get_obvodka(self) -> QRect:
        raise NotImplementedError

    def is_in_obvodka(self, bounds: QRect) -> bool:
        r = self.get_obvodka()
        return (
            r.left() >= 0 and
            r.top() >= 0 and
            r.right() <= bounds.width() and
            r.bottom() <= bounds.height()
        )

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
    def __init__(self, x: int, y: int, color=Qt.blue):
        super().__init__(x, y, color)
        self.r = 20
        self.min = 5
        self.max = 100

    def get_obvodka(self) -> QRect:
        return QRect(self.center.x() - self.r, self.center.y() - self.r, 2 * self.r, 2 * self.r)

    def Is_in(self, point: QPoint) -> bool:
        dx = self.center.x() - point.x()
        dy = self.center.y() - point.y()
        return dx * dx + dy * dy <= self.r * self.r

    def draw(self, painter: QtGui.QPainter):
        pen_color = Qt.red if self._state else self.color
        painter.setPen(pen_color)
        painter.setBrush(pen_color)
        painter.drawEllipse(self.center, self.r, self.r)

    def resize(self, f: float, bounds: QRect) -> bool:
        new_r = self.r * f
        if not (self.min <= new_r <= self.max):
            return False
        old_r = self.r
        self.r = int(new_r)
        if self.is_in_obvodka(bounds):
            return True
        self.r = old_r
        return False


class Rects(Geometry):
    def __init__(self, x: int, y: int, color=Qt.magenta):
        super().__init__(x, y, color)
        self.width = 40
        self.height = 40
        self.min = 10
        self.max = 200

    def get_obvodka(self) -> QRect:
        return QRect(
            self.center.x() - self.width // 2,
            self.center.y() - self.height // 2,
            self.width,
            self.height
        )

    def Is_in(self, point: QPoint) -> bool:
        left = self.center.x() - self.width // 2
        right = self.center.x() + self.width // 2
        top = self.center.y() - self.height // 2
        bottom = self.center.y() + self.height // 2
        return left <= point.x() <= right and top <= point.y() <= bottom

    def draw(self, painter: QtGui.QPainter):
        pen_color = Qt.red if self._state else self.color
        painter.setPen(pen_color)
        painter.setBrush(pen_color)
        painter.drawRect(
            self.center.x() - self.width // 2,
            self.center.y() - self.height // 2,
            self.width,
            self.height
        )

    def resize(self, factor: float, bounds: QRect) -> bool:
        new_w = self.width * factor
        new_h = self.height * factor
        if not (self.min <= new_w <= self.max and self.min <= new_h <= self.max):
            return False
        old_w, old_h = self.width, self.height
        self.width, self.height = int(new_w), int(new_h)
        if self.is_in_obvodka(bounds):
            return True
        self.width, self.height = old_w, old_h
        return False


class Rectangle(Geometry):
    def __init__(self, x: int, y: int, color=Qt.yellow):
        super().__init__(x, y, color)
        self.width = 60
        self.height = 30
        self.min = 10
        self.max = 200

    def get_obvodka(self) -> QRect:
        return QRect(
            self.center.x() - self.width // 2,
            self.center.y() - self.height // 2,
            self.width,
            self.height
        )

    def Is_in(self, point: QPoint) -> bool:
        left = self.center.x() - self.width // 2
        right = self.center.x() + self.width // 2
        top = self.center.y() - self.height // 2
        bottom = self.center.y() + self.height // 2
        return left <= point.x() <= right and top <= point.y() <= bottom

    def draw(self, painter: QtGui.QPainter):
        pen_color = Qt.red if self._state else self.color
        painter.setPen(pen_color)
        painter.setBrush(pen_color)
        painter.drawRect(
            self.center.x() - self.width // 2,
            self.center.y() - self.height // 2,
            self.width,
            self.height
        )

    def resize(self, factor: float, bounds: QRect) -> bool:
        new_w = self.width * factor
        new_h = self.height * factor
        if not (self.min <= new_w <= self.max and self.min <= new_h <= self.max):
            return False
        old_w, old_h = self.width, self.height
        self.width, self.height = int(new_w), int(new_h)
        if self.is_in_obvodka(bounds):
            return True
        self.width, self.height = old_w, old_h
        return False


class Ellipse(Geometry):
    def __init__(self, x: int, y: int, color=Qt.green):
        super().__init__(x, y, color)
        self.rx = 30
        self.ry = 20
        self.min = 5
        self.max = 100

    def get_obvodka(self) -> QRect:
        return QRect(self.center.x() - self.rx, self.center.y() - self.ry, 2 * self.rx, 2 * self.ry)

    def Is_in(self, point: QPoint) -> bool:
        dx = (point.x() - self.center.x()) / self.rx
        dy = (point.y() - self.center.y()) / self.ry
        return dx * dx + dy * dy <= 1

    def draw(self, painter: QtGui.QPainter):
        pen_color = Qt.red if self._state else self.color
        painter.setPen(pen_color)
        painter.setBrush(pen_color)
        painter.drawEllipse(
            self.center.x() - self.rx,
            self.center.y() - self.ry,
            2 * self.rx,
            2 * self.ry
        )

    def resize(self, factor: float, bounds: QRect) -> bool:
        new_rx = self.rx * factor
        new_ry = self.ry * factor
        if not (self.min <= new_rx <= self.max and self.min <= new_ry <= self.max):
            return False
        old_rx, old_ry = self.rx, self.ry
        self.rx, self.ry = int(new_rx), int(new_ry)
        if self.is_in_obvodka(bounds):
            return True
        self.rx, self.ry = old_rx, old_ry
        return False


class Tringl(Geometry):
    def __init__(self, x: int, y: int, color=Qt.cyan):
        super().__init__(x, y, color)
        self.size = 40
        self.min = 10
        self.max = 150

    def get_obvodka(self) -> QRect:
        half = self.size // 2
        return QRect(self.center.x() - half, self.center.y() - half, self.size, self.size)

    def Is_in(self, point: QPoint) -> bool:
        half = self.size // 2
        left = self.center.x() - half
        right = self.center.x() + half
        top = self.center.y() - half
        bottom = self.center.y() + half
        return left <= point.x() <= right and top <= point.y() <= bottom

    def draw(self, painter: QtGui.QPainter):
        pen_color = Qt.red if self._state else self.color
        painter.setPen(pen_color)
        painter.setBrush(pen_color)
        points = [
            QPoint(self.center.x(), self.center.y() - self.size // 2),
            QPoint(self.center.x() - self.size // 2, self.center.y() + self.size // 2),
            QPoint(self.center.x() + self.size // 2, self.center.y() + self.size // 2),
        ]
        painter.drawPolygon(points)

    def resize(self, factor: float, bounds: QRect) -> bool:
        new_size = self.size * factor
        if not (self.min <= new_size <= self.max):
            return False
        old_size = self.size
        self.size = int(new_size)
        if self.is_in_obvodka(bounds):
            return True
        self.size = old_size
        return False


class Line(Geometry):
    def __init__(self, x: int, y: int, color=Qt.black):
        super().__init__(x, y, color)
        self.length = 50
        self.min = 10
        self.max = 300

    def get_obvodka(self) -> QRect:
        return QRect(self.center.x(), self.center.y() - 1, self.length, 3)

    def Is_in(self, point: QPoint) -> bool:
        return (abs(point.y() - self.center.y()) <= 2 and
                self.center.x() <= point.x() <= self.center.x() + self.length)

    def draw(self, painter: QtGui.QPainter):
        pen_color = Qt.red if self._state else self.color
        painter.setPen(pen_color)
        painter.setBrush(Qt.NoBrush)
        painter.drawLine(self.center, QPoint(self.center.x() + self.length, self.center.y()))

    def resize(self, factor: float, bounds: QRect) -> bool:
        new_len = self.length * factor
        if not (self.min <= new_len <= self.max):
            return False
        old_len = self.length
        self.length = int(new_len)
        if self.is_in_obvodka(bounds):
            return True
        self.length = old_len
        return False

class Container:
    def __init__(self):
        self._cont = []

    def add(self, geom):
        self._cont.append(geom)

    def return_cont(self):
        return self._cont

    def get_stated(self):
        return [s for s in self._cont if s.is_state()]

    def set_color(self, color):
        for s in self.get_stated():
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

    def move_stated(self, dx: int, dy: int, bounds: QRect):
        for s in self.get_stated():
            s.move(dx, dy, bounds)

    def resize_stated(self, f: float, bounds: QRect):
        for s in self.get_stated():
            s.resize(f, bounds)

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
        state = self.cont.get_stated()
        if not state:
            return

        dx, dy = 0, 0
        f = None

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
        elif event.key() in (Qt.Key_Plus, Qt.Key_Equal):
            f = 1.2
        elif event.key() == Qt.Key_Minus:
            f = 0.8
        else:
            super().keyPressEvent(event)
            return

        bounds = self.rect()
        if dx != 0 or dy != 0:
            self.cont.move_stated(dx, dy, bounds)
        elif f is not None:
            self.cont.resize_stated(f, bounds)

        self.update()

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Редактор")
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