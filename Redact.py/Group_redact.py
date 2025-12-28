import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFrame, QWidget, QVBoxLayout,
    QToolBar, QAction, QColorDialog, QFileDialog
)
from PyQt5.QtCore import QPoint, Qt, QRect
from PyQt5 import QtGui
import json

class Geometry():
    name = "Geometry"
    def __init__(self,x:int,y:int,color = Qt.black):
        self._center = QPoint(x,y)
        self._state = False
        self.color = color
    
    def is_in_obvodka(self, bounds: QRect) -> bool:
        r = self.get_obvodka()
        return (r.left() >= 0 and r.top() >= 0 and r.right() <= bounds.width() and r.bottom() <= bounds.height())
    
    def move(self, dx:int,dy:int,bounds :QRect)->bool:
        old_center = self._center
        self._center = QPoint(self._center.x() + dx,self._center.y()+dy)
        if not self.is_in_obvodka(bounds):
            self._center = old_center
            return False
        return True
    def get_old_size(self):
        raise NotImplementedError
    
    def resize(self, f: float, bounds: QRect) -> bool:
        return False

    def get_obvodka(self) -> QRect:
        raise NotImplementedError

    def Is_in(self, point: QPoint) -> bool:
        raise NotImplementedError

    def draw(self, painter: QtGui.QPainter):
        raise NotImplementedError

    def Replace_state(self):
        self._state = not self._state

    def base_state(self):
        self._state = False

    def is_state(self) -> bool:
        return self._state

    def set_color(self, color):
        self.color = color

    def from_data_object(self,data):
        return NotImplementedError
    def data_object(self):
        return{"name": self.name,"x":self._center.x(),"y":self._center.y(),"color":self.color ,"state":self._state}
    def save(self,filename):
        json.dump(self.data_object(),filename)
        filename.write("\n")
    @staticmethod
    def load(in_file):
        line = in_file.readline()
        if not line.strip():
            return None
        data = json.loads(line.strip())
        type_name = data["name"]
        if type_name == "Group":
            return Group.from_data_object(data)
        elif type_name == "Circle":
            return Circle.from_data_object(data)
        elif type_name == "Rects":
            return Rects.from_data_object(data)
        elif type_name == "Rectangle":
            return Rectangle.from_data_object(data)
        elif type_name == "Ellipse":
            return Ellipse.from_data_object(data)
        elif type_name == "Tringl":
            return Tringl.from_data_object(data)
        elif type_name == "Line":
            return Line.from_data_object(data)
        else:
            raise ValueError(f"Не найдн данный тип объекта: {type_name}")
    
    

class Circle(Geometry):
    
    name = "Circle"
    def __init__(self,x:int,y:int,color = Qt.magenta,r=40):
        super().__init__(x,y,color)
        self._r = r
        self._min = 5
        self._max = 80
        
    
    def get_obvodka(self) -> QRect:
        return QRect(self._center.x()-self._r,self._center.y()-self._r,self._r*2,self._r*2)
    def Is_in(self, point: QPoint) -> bool:
        dx = self._center.x()-point.x()
        dy = self._center.y()-point.y()
        return (dx*dx+dy*dy)<=self._r*self._r
    
    def draw(self, painter: QtGui.QPainter):
        pen_color = Qt.red if self._state else self.color
        painter.setPen(pen_color)
        painter.setBrush(pen_color)
        painter.drawEllipse(self._center, self._r, self._r)

   
    
    def resize(self, f: float, bounds: QRect) -> bool:
        new_r = self._r * f
        if not (self._min<=new_r<=self._max):
            return False
        old_r = self._r
        self._r = int(new_r)
        if self.is_in_obvodka(bounds):
            return True
        self._r = old_r
        return False
    
    def data_object(self):
        data = super().data_object()
        data["r"]= self._r
        return data
    @classmethod
    def from_data_object(cls,data):
        obj = Circle(data["x"], data["y"], QtGui.QColor(data["color"]), data.get("r", 40))
        obj._state = data.get("state", False)
        return obj
    

class Ellipse(Geometry):
    name = "Ellipse"
    def __init__(self, x: int, y: int, color=Qt.green,rx=60,ry=30):
        super().__init__(x, y, color)
        self.rx = rx
        self.ry = ry
        self.min = 5
        self.max = 100
    

    def get_obvodka(self) -> QRect:
        return QRect(self._center.x() - self.rx, self._center.y() - self.ry, 2 * self.rx, 2 * self.ry)

    def Is_in(self, point: QPoint) -> bool:
        dx = (point.x() - self._center.x()) / self.rx
        dy = (point.y() - self._center.y()) / self.ry
        return dx * dx + dy * dy <= 1

    def draw(self, painter: QtGui.QPainter):
        pen_color = Qt.red if self._state else self.color
        painter.setPen(pen_color)
        painter.setBrush(pen_color)
        painter.drawEllipse(
            self._center.x() - self.rx,
            self._center.y() - self.ry,
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
    
    def data_object(self):
        data = super().data_object()
        data["rx"]= self.rx
        data["ry"] = self.ry
        return data
    @classmethod
    def from_data_object(cls,data):
        obj = Ellipse(data["x"], data["y"], QtGui.QColor(data["color"]), data.get("rx", 60),data.get("ry",30))
        obj._state = data.get("state", False)
        return obj

class Rects(Geometry):
    name = "Rects"
    def __init__(self, x: int, y: int, color=Qt.magenta,w=80,h=80):
        super().__init__(x, y, color)
        self.width = w
        self.height = h
        self.min = 10
        self.max = 200
       

    def get_obvodka(self) -> QRect:
        return QRect(
            self._center.x() - self.width // 2,
            self._center.y() - self.height // 2,
            self.width,
            self.height
        )

    def Is_in(self, point: QPoint) -> bool:
        left = self._center.x() - self.width // 2
        right = self._center.x() + self.width // 2
        top = self._center.y() - self.height // 2
        bottom = self._center.y() + self.height // 2
        return left <= point.x() <= right and top <= point.y() <= bottom

    def draw(self, painter: QtGui.QPainter):
        pen_color = Qt.red if self._state else self.color
        painter.setPen(pen_color)
        painter.setBrush(pen_color)
        painter.drawRect(
            self._center.x() - self.width // 2,
            self._center.y() - self.height // 2,
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
        self.width, self.height =old_w, old_h
        return False
    
    def data_object(self):
        data = super().data_object()
        data["w"]= self.width
        data["h"] = self.height
        return data
    @classmethod
    def from_data_object(cls,data):
        obj = Rects(data["x"], data["y"], QtGui.QColor(data["color"]), data.get("w", 80),data.get("h",80))
        obj._state = data.get("state", False)
        return obj

class Rectangle(Geometry):
    name = "Rectangle"
    def __init__(self, x: int, y: int, color=Qt.yellow,w=80,h=60):
        super().__init__(x, y, color)
        self.width = w
        self.height = h
        self.min = 10
        self.max = 200
        

    def get_obvodka(self) -> QRect:
        return QRect(
            self._center.x() - self.width // 2,
            self._center.y() - self.height // 2,
            self.width,
            self.height
        )

    def Is_in(self, point: QPoint) -> bool:
        left = self._center.x() - self.width // 2
        right = self._center.x() + self.width // 2
        top = self._center.y() - self.height // 2
        bottom = self._center.y() + self.height // 2
        return left <= point.x() <= right and top <= point.y() <= bottom

    def draw(self, painter: QtGui.QPainter):
        pen_color = Qt.red if self._state else self.color
        painter.setPen(pen_color)
        painter.setBrush(pen_color)
        painter.drawRect(
            self._center.x() - self.width // 2,
            self._center.y() - self.height // 2,
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
    
    def data_object(self):
        data = super().data_object()
        data["w"]= self.width
        data["h"] = self.height
        return data
    @classmethod
    def from_data_object(cls,data):
        obj = Rectangle(data["x"], data["y"], QtGui.QColor(data["color"]), data.get("w", 80),data.get("h",60))
        obj._state = data.get("state", False)
        return obj

class Tringl(Geometry):
    name = "Tringl"
    def __init__(self, x: int, y: int, color=Qt.cyan,s =60):
        super().__init__(x, y, color)
        self.size = s
        self.min = 10
        self.max = 150
        

    def get_obvodka(self) -> QRect:
        half = self.size // 2
        return QRect(self._center.x() - half, self._center.y() - half, self.size, self.size)

    def Is_in(self, point: QPoint) -> bool:
        half = self.size // 2
        left = self._center.x() - half
        right = self._center.x() + half
        top = self._center.y() - half
        bottom = self._center.y() + half
        return (left+half//2 <= point.x() <= right-half//2 and top+half <= point.y() <= bottom)or(left <= point.x() <= left+half//2 and top+half//2 <= point.y() <= bottom)or(right-half//2 <= point.x() <= right and top+half//2 <= point.y() <= bottom) or(left+half//2 <= point.x() <= right-half//2 and top <= point.y() <= bottom-half) 

    def draw(self, painter: QtGui.QPainter):
        pen_color = Qt.red if self._state else self.color
        painter.setPen(pen_color)
        painter.setBrush(pen_color)
        points = [
            QPoint(self._center.x(), self._center.y() - self.size // 2),
            QPoint(self._center.x() - self.size // 2, self._center.y() + self.size // 2),
            QPoint(self._center.x() + self.size // 2, self._center.y() + self.size // 2),
        ]
        painter.drawPolygon(points)
    
        
    def resize(self, factor: float, bounds: QRect) -> bool:
        new_size = self.size * factor
        if not (self.min <= new_size <= self.max):
            return False
        old_s = self.size
        self.size = int(new_size)
        if self.is_in_obvodka(bounds):
            return True
        self.size = old_s
        return False

    def data_object(self):
        data = super().data_object()
        data["size"]= self.size
        return data
    @classmethod
    def from_data_object(cls,data):
        obj = Tringl(data["x"], data["y"], QtGui.QColor(data["color"]), data.get("size", 60))
        obj._state = data.get("state", False)
        return obj
class Line(Geometry):
    name = "Line"
    def __init__(self, x: int, y: int, color=Qt.black,l =100):
        super().__init__(x, y, color)
        self.len = l
        self.min = 10
        self.max = 300
        

    def get_obvodka(self) -> QRect:
        return QRect(self._center.x(), self._center.y() - 1, self.len, 3)

    def Is_in(self, point: QPoint) -> bool:
        return (abs(point.y() - self._center.y()) <= 2 and
                self._center.x() <= point.x() <= self._center.x() + self.len)

    def draw(self, painter: QtGui.QPainter):
        pen_color = Qt.red if self._state else self.color
        painter.setPen(pen_color)
        painter.setBrush(Qt.NoBrush)
        painter.drawLine(self._center, QPoint(self._center.x() + self.len, self._center.y()))
    
        
    def resize(self, factor: float, bounds: QRect) -> bool:
        new_len = self.len * factor
        if not (self.min <= new_len <= self.max):
            return False
        old_l = self.len
        self.len = int(new_len)
        if self.is_in_obvodka(bounds):
            return True
        self.len = old_l
        return False

    def data_object(self):
        data = super().data_object()
        data["len"]= self.len
  
        return data
    @classmethod
    def from_data_object(cls,data):
        obj = Line(data["x"], data["y"], QtGui.QColor(data["color"]), data.get("len", 100))
        obj._state = data.get("state", False)
        return obj
    
class Container():
    def __init__(self):
        self._cont = []

    def add(self, geo: Geometry):
        self._cont.append(geo)
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
            s.base_state()

    def Popal(self, point: QPoint, ctrl: bool):
        popal = []
        i=0
        for geom in reversed(self._cont):
            if geom.Is_in(point):
                    popal.append(geom)
        if not popal:
            if not ctrl:
                self.base_state()
            return False
        else:
            if not ctrl:
                self.base_state()

            for geom in popal:
                if not ctrl:
                    geom.Replace_state()
                    return True
                geom.base_state()    
                geom.Replace_state()
            return True
    def move_stated(self, dx: int, dy: int, bounds: QRect):
        for s in self.get_stated():
            s.move(dx, dy, bounds)

    def resize_stated(self, f: float, bounds: QRect):
        for s in self.get_stated():
            s.resize(f, bounds)
    
    def group_selected(self):
        selected = [s for s in self._cont if s.is_state()]
        if len(selected) < 2:
            return
        group = Group(0, 0, object= selected)
        self._cont = [s for s in self._cont if s not in selected]
        self._cont.append(group)
        for c in selected:
            c.base_state()
        
        

    def ungroup_selected(self):
        new_cont = []
        for obj in self._cont:
            if isinstance(obj, Group) and obj.is_state():
                
                for a in obj.objects:
                    new_cont.append(a)
                for o in obj.objects:
                    o.base_state()
            else:
                new_cont.append(obj)
        self._cont = new_cont
    
    def save_file(self,filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"{len(self._cont)}\n")
            for obj in self._cont:
                obj.save(f)

    def load_from_file(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            n = int(f.readline().strip())
            self._cont = []
            for _ in range(n):
                obj = Geometry.load(f)
                if obj:
                    self._cont.append(obj)

class Group(Geometry):
    name = "Group"
    def __init__(self, x: int, y: int, color=Qt.black,object=None):
        super().__init__(x, y, color)
        self.objects = object or []
        if self.objects:
            self._center_Group()
    
    
    def _center_Group(self):
        if not self.objects:
            return
        rect = self.get_obvodka()
        self._center = QPoint(rect.center().x(),rect.center().y())
    
    def get_obvodka(self) -> QRect:
        if not self.objects:
            return QRect(0,0,0,0)
        l = min(c.get_obvodka().left() for c in self.objects)
        r = max(c.get_obvodka().right() for c in self.objects)
        b = max(c.get_obvodka().bottom() for c in self.objects)
        t = min(c.get_obvodka().top() for c in self.objects)
        return QRect(l,t,r-l,b-t)
    def Is_in(self, point: QPoint) -> bool:
        return self.get_obvodka().contains(point)
    
    def draw(self, painter: QtGui.QPainter):
        pen_color = Qt.red if self._state else self.color
        painter.setPen(pen_color)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(self.get_obvodka())
        for c in self.objects:
            c.set_color(self.color)
            c.draw(painter)
            
    
    def move(self, dx: int, dy: int, bounds: QRect)->bool:
        old_center = [QPoint(obj._center.x(), obj._center.y()) for obj in self.objects]
        for obj in self.objects:

            if not obj.move(dx,dy,bounds):
                for i,ob in enumerate(self.objects):
                    ob._center = old_center[i]
                return False
        self._center_Group()
        if not self.is_in_obvodka(bounds):
            for i,ob in enumerate(self.objects):
                ob._center = old_center[i]
            return False
        return True
        
    def resize(self, f: float, bounds: QRect) -> bool:
        
        for c in self.objects:
            if not c.resize(f,bounds):
                return False
        return True
    
    def data_object(self):
        data = super().data_object()
        data["objects"] = [obj.data_object() for obj in self.objects]
        return data
    @classmethod
    def from_data_object(cls,data):
        x,y = data["x"],data["y"]
        color = QtGui.QColor(data["color"])
        group = Group(x,y,color=color)
        group.objects = []
        for data_obj in data["objects"]:
            type_obj = data_obj["name"]
            if type_obj == "Group":
                obj = Group.from_data_object(data_obj)
            elif type_obj==Circle.name:
                obj = Circle.from_data_object(data_obj)
            elif type_obj=="Tringl":
                obj = Tringl.from_data_object(data_obj)
            elif type_obj=="Ellipse":
                obj = Ellipse.from_data_object(data_obj)
            elif type_obj=="Line":
                obj = Line.from_data_object(data_obj)
            elif type_obj=="Rectangle":
                obj = Rectangle.from_data_object(data_obj)
            elif type_obj=="Rects":
                obj = Rects.from_data_object(data_obj)
            group.objects.append(obj)
        group._center_Group()
        group._state = data.get("state",False)
        return group

    
        
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
            f = 1.0/1.2 
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
        
        group_action = QAction("Группировать", self)
        group_action.triggered.connect(self.cont.group_selected)
        toolbar.addAction(group_action)

        ungroup_action = QAction("Разгруппировать", self)
        ungroup_action.triggered.connect(self.cont.ungroup_selected)
        toolbar.addAction(ungroup_action)

        save_action = QAction("Сохранить", self)
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)

        load_action = QAction("Загрузить", self)
        load_action.triggered.connect(self.load_file)
        toolbar.addAction(load_action)
       
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.drawing.setFocus()

    def save_file(self):
        fname, _ = QFileDialog.getSaveFileName(self, "Сохранить проект", "", "Text Files (*.txt)")
        if fname:
            if not fname.endswith(".txt"):
                fname += ".txt"
            self.cont.save_file(fname)

    def load_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Загрузить проект", "", "Text Files (*.txt)")
        if fname:
            self.cont.load_from_file(fname)
            self.drawing.update()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())