import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QFrame,QWidget,QBoxLayout, QMenu
from PyQt5.QtCore import QPoint,Qt
from PyQt5 import QtGui

class Geometry():
    def __init__(self,x:int,y:int,color = Qt.black):
        self.__center = QPoint(x,y)
        self.color = color
        self.__state = False

    def move(self,x:int,y:int):
        self.__center = QPoint(x,y)
    
    def draw(self, painter: QtGui.QPainter):
        raise NotImplementedError

    def Is_in(self, point:QPoint) -> bool:
        raise NotImplementedError
        
    def No_State(self):
        self.state = not self.state
    def is_state(self):
        return self.__state
    

class Circle():
    
    def __init__(self,x:int,y:int):
        super().__init__()
        self.state = False
        self.r =10

    def set_radius(self,r:int):
        if r>10:
            self.r = r

    def Is_in(self,point:QPoint)->bool:
        dx = self.center.x()-point.x()
        dy = self.center.y()-point.y()
        return dx*dx+dy*dy<=self.r*self.r
    def draw(self,pain:QtGui.QPainter):
        if self.state:
            color = Qt.red
        else:
            color = Qt.black
        pain.setPen(color)
        pain.setBrush(Qt.NoBrush)
        pain.drawEllipse(self.center,self.r,self.r)
    
class Rects(Geometry):
    def __init__(self):
         super().__init__()
         self.weight = 10
         self.hight = 10

    def Is_in(self,point:QPoint) ->bool:
        if point.x()>self.center.x()-self.hight and point.x()<self.center.x()+self.hight:
            if point.y()>self.center.y()-self.weight and point.y()<self.center.y()+self.weight:
                return True
        else:
            return False
    def draw(self, painter: QtGui.QPainter):
        if self.state:
            color = Qt.red
        else:
            color = Qt.black
        painter.setPen(color)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(self.__center,self.weight,self.hight)
        
        return super().draw(painter)

class Rectangl(Geometry):
    def __init__(self):
         super().__init__()
         self.weight = 10
         self.hight = 10

    def Is_in(self,point:QPoint) ->bool:
        if point.x()>self.center.x()-self.hight and point.x()<self.center.x()+self.hight:
            if point.y()>self.center.y()-self.weight and point.y()<self.center.y()+self.weight:
                return True
        else:
            return False
    def draw(self, painter: QtGui.QPainter):
        if self.state:
            color = Qt.red
        else:
            color = Qt.black
        painter.setPen(color)
        painter.setBrush(Qt.NoBrush)
        painter.drawPolygon()
        
        return super().draw(painter)