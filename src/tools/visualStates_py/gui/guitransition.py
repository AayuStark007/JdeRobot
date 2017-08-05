'''
   Copyright (C) 1997-2016 JDERobot Developers Team
 
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.
 
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU Library General Public License for more details.
 
   You should have received a copy of the GNU General Public License
   along with this program; if not, see <http://www.gnu.org/licenses/>.
 
   Authors : Samuel Rey <samuel.rey.escudero@gmail.com> 
 
  '''

from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsRectItem, QGraphicsPolygonItem, QGraphicsItem
from PyQt5.QtGui import QPen, QBrush, QPolygonF
from PyQt5.QtCore import Qt, QPointF, QLineF, QRectF
from . import guistate, idtextboxgraphicsitem
from . import recthandlegraphicsitem
from . import transitiontype
import math

# CONST
SQUARE_SIDE = 10
ARROW_SIZE = 12
PEN_NORMAL_WIDTH = 1
PEN_FOCUS_WIDTH = 3

class TransitionGraphicsItem(QGraphicsLineItem):
    def __init__(self, orig, dest, id, name='transition'):
        super().__init__()

        self.id = id
        self.name = name
        self.code = ""
        self.transitionType = transitiontype.TransitionType.TEMPORAL
        self.temporal = 0 # when to transition
        self.condition = ""

        self.origin = orig
        self.origin.addOriginTransition(self)
        self.destination = dest
        self.destination.addTargetTransition(self)


        self.originLine = None
        self.destinationLine = None
        self.arrow = None
        self.textGraphics = None
        self.middleHandle = None

        self.isEventsRemoved = False

        #
        # startPoint = QPointF(self.origin.scenePos().x(), self.origin.scenePos().y())
        # midPoint = QPointF((self.destination.scenePos().x() + self.origin.scenePos().x())/2.0,
        # 				   (self.destination.scenePos().y() + self.origin.scenePos().y()) / 2.0)
        # endPoint = QPointF(self.destination.scenePos().x(), self.destination.scenePos().y())
        #
        # polygon = QPolygonF()
        # polygon << startPoint << midPoint << endPoint
        # self.setPolygon(polygon)

        # connect position changed event
        self.origin.posChanged.connect(self.statePosChanged)
        self.destination.posChanged.connect(self.statePosChanged)

        self.midPointX = (self.destination.scenePos().x() + self.origin.scenePos().x()) / 2.0
        self.midPointY = (self.destination.scenePos().y() + self.origin.scenePos().y()) / 2.0
        # self.setPos(self.midPointX, self.midPointY)
        print('transition pos:' + str(self.pos()))

        self.createOriginLine()
        self.createDestinationLine()

        self.createArrow()
        self.createMiddleHandle()
        self.createIdTextBox()

    def statePosChanged(self, state):
        if self.origin == state:
            self.createOriginLine()
        elif self.destination == state:
            self.createDestinationLine()
            self.createArrow()

    def createOriginLine(self):
        if self.originLine == None:
            self.originLine = QGraphicsLineItem(self.midPointX, self.midPointY, self.origin.scenePos().x(),
                                                self.origin.scenePos().y(), self)
        else:
            self.originLine.setLine(QLineF(self.midPointX, self.midPointY, self.origin.scenePos().x(),
                                           self.origin.scenePos().y()))
        myLine = self.originLine.line()
        myLine.setLength(myLine.length() - guistate.NODE_WIDTH / 2)
        self.originLine.setLine(myLine)

    def createDestinationLine(self):
        if self.destinationLine == None:
            self.destinationLine = QGraphicsLineItem(self.midPointX, self.midPointY, self.destination.scenePos().x(),
                                                     self.destination.scenePos().y(), self)
        else:
            self.destinationLine.setLine(QLineF(self.midPointX, self.midPointY, self.destination.scenePos().x(),
                                                self.destination.scenePos().y()))

        myLine = self.destinationLine.line()
        myLine.setLength(myLine.length() - guistate.NODE_WIDTH / 2)
        self.destinationLine.setLine(myLine)

    def createArrow(self):
        # add an arrow to destination line
        myLine = self.destinationLine.line()
        myLine.setLength(myLine.length() - ARROW_SIZE)
        rotatePoint = myLine.p2() - self.destinationLine.line().p2()

        rightPointX = rotatePoint.x() * math.cos(math.pi / 6) - rotatePoint.y() * math.sin(math.pi / 6)
        rightPointY = rotatePoint.x() * math.sin(math.pi / 6) + rotatePoint.y() * math.cos(math.pi / 6)
        rightPoint = QPointF(rightPointX + self.destinationLine.line().x2(),
                             rightPointY + self.destinationLine.line().y2())

        leftPointX = rotatePoint.x() * math.cos(-math.pi / 6) - rotatePoint.y() * math.sin(-math.pi / 6)
        leftPointY = rotatePoint.x() * math.sin(-math.pi / 6) + rotatePoint.y() * math.cos(-math.pi / 6)
        leftPoint = QPointF(leftPointX + self.destinationLine.line().x2(),
                            leftPointY + self.destinationLine.line().y2())

        polygon = QPolygonF()
        polygon << rightPoint << leftPoint << self.destinationLine.line().p2() << rightPoint

        if self.arrow == None:
            self.arrow = QGraphicsPolygonItem(polygon, self)
        else:
            self.arrow.setPolygon(polygon)

        brush = QBrush(Qt.SolidPattern)
        brush.setColor(Qt.black)
        self.arrow.setBrush(brush)

    def createMiddleHandle(self):
        # create middle handle
        if self.middleHandle == None:
            self.middleHandle = recthandlegraphicsitem.RectHandleGraphicsItem(SQUARE_SIDE, self)
            self.middleHandle.setFlag(QGraphicsItem.ItemIsMovable)

        self.middleHandle.setPos(self.midPointX, self.midPointY)

    def createIdTextBox(self):
        if self.textGraphics == None:
            self.textGraphics = idtextboxgraphicsitem.IdTextBoxGraphicsItem(self.name, self)
            self.textGraphics.textChanged.connect(self.nameChanged)
        else:
            self.textGraphics.setPlainText(self.name)
        textWidth = self.textGraphics.boundingRect().width()
        self.textGraphics.setPos(self.midPointX - textWidth / 2, self.midPointY + SQUARE_SIDE - (SQUARE_SIDE / 2) + 5)

    def updateMiddlePoints(self, newPosition):
        self.midPointX = newPosition.x()
        self.midPointY = newPosition.y()
        self.createOriginLine()
        self.createDestinationLine()
        self.createArrow()
        self.createIdTextBox()

    def nameChanged(self, name):
        self.name = name
        self.createIdTextBox()

    def removeEventConnections(self):
        if not self.isEventsRemoved:
            if self.origin == self.destination:
                self.origin.posChanged.disconnect(self.statePosChanged)
            else:
                self.origin.posChanged.disconnect(self.statePosChanged)
                self.destination.posChanged.disconnect(self.statePosChanged)
            self.eventsRemoved = True

    def setType(self, type):
        self.transitionType = type

    def getType(self):
        return self.transitionType

    def setTemporalTime(self, time):
        self.temporal = time

    def getTemporalTime(self):
        return self.temporal

    def setCondition(self, cond):
        self.condition = cond

    def getCondition(self):
        return self.condition

    def setCode(self, code):
        self.code = code

    def getCode(self):
        return self.code