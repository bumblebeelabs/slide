#!/usr/bin/env python
# Copyright 2020 Bumble Bee Laboratories Pte Ltd
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
# 20200813TM - add jpeg and case insensitive extensions

import sys
import os
from PySide2 import QtCore, QtWidgets, QtGui

class W(QtWidgets.QWidget):

  def __init__(self):
    super().__init__()
    self.init()

  def init(self):
    global app
    screen = app.primaryScreen()
    screenGeometry = screen.geometry()
    height = screenGeometry.height() * 0.8
    width = screenGeometry.width() * 0.8
    self.slidemode = False
    self.querymode = False
    self.screensize = QtCore.QSize(width, height)
    self.setWindowTitle('slide')
    self.show()
    picdir = os.path.dirname(sys.argv[1])
    bname = os.path.basename(sys.argv[1])
    if len(picdir) == 0:
      picdir = "./"

    self.piclist = []
    self.picptr = 0
    for fe in os.scandir(picdir):
      fep = fe.path
      feps = fep.lower()
      if feps.endswith(".png") or feps.endswith(".jpg") or feps.endswith(".jpeg"):
        print(fep)
        self.piclist.append(fep)
    
    self.piclist.sort()

    i = 0
    for fep in self.piclist:
      if fep.endswith(bname):
        self.picptr = i
        print(bname)
      i += 1
    self.ticks = 0
    self.maxticks = 45

    self.onreload(self.picptr)

    self.timer = QtCore.QTimer(self)
    self.timer.timeout.connect(self.ontime)
    self.timer.start(1000)


  def load(self, filename):
    image = QtGui.QImage(filename)
    pixmap = QtGui.QPixmap(image)
    return pixmap

  def setPixmap(self, pixmap, ssz):
    sz = pixmap.size()
    imageaspect = sz.width() / sz.height()
    screenaspect = ssz.width()/ssz.height()
    if imageaspect > screenaspect:
      width = ssz.width()
      height = ssz.width() / imageaspect
    else:
      width = ssz.height() * imageaspect
      height = ssz.height()
    sz2 = QtCore.QSize(width, height)
    self.pixmap = pixmap.scaled(sz2 , QtCore.Qt.KeepAspectRatio , QtCore.Qt.SmoothTransformation)
    return sz2

  def onreload(self, i):
    path = self.piclist[i]
    pixmap = self.load(path)
    picsz = self.setPixmap(pixmap, self.screensize)
    self.resize(picsz)

  def advance(self):
    self.picptr += 1
    if self.picptr >= len(self.piclist):
      self.picptr = 0
    print("advance")
    self.onreload(self.picptr)
    self.repaint()

  def retreat(self):
    self.picptr -= 1
    if self.picptr < 0:
      self.picptr = len(self.piclist) - 1
    print("retreat")
    self.onreload(self.picptr)
    self.repaint()

  def onduration(self):
    self.advance()

  def ontime(self):
    if self.slidemode:
      print("timeout")
      self.ticks += 1
      if self.ticks % self.maxticks == 0:
        self.onduration()
      self.repaint()

  def togglemode(self):
    self.slidemode = not self.slidemode
    self.repaint()

  def togglequery(self):
    self.querymode = not self.querymode
    self.repaint()

  def paintEvent(self, e):
    qp = QtGui.QPainter()
    qp.begin(self)
    qp.drawPixmap(self.rect(),self.pixmap,self.pixmap.rect())
    green = QtGui.QColor(100,255,160,255)
    if self.slidemode:
      qp.fillRect(0,0,100,60,QtGui.QColor(0,0,0,64))
      qp.setFont(QtGui.QFont("Arial", 24, QtGui.QFont.Bold));
      qp.setPen(green)
      qfm = qp.fontMetrics()
      s = str(self.picptr + 1)
      bb = qfm.boundingRect(s)
      qp.drawText(80-bb.width(),40,s)
      qp.setBrush(green)
      w = (self.ticks/self.maxticks*80)%80
      qp.drawRect(10,50,w,7)
    if self.querymode:
      qp.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Normal));
      qp.setPen(green)
      s = self.piclist[self.picptr]
      qp.drawText(120,40,s)
    qp.end()

  def keyPressEvent(self, event):
    if event.key() == QtCore.Qt.Key_Space:
      self.togglemode()
    elif event.key() == QtCore.Qt.Key_Right:
      self.advance()
    elif event.key() == QtCore.Qt.Key_Left:
      self.retreat()
    elif event.key() == QtCore.Qt.Key_Question or event.key() == QtCore.Qt.Key_Slash:
      self.togglequery()
    event.accept()

# Create a Qt application
app = QtWidgets.QApplication(sys.argv)

# Create a Window
mywindow = W()

# Enter Qt application main loop
sys.exit(app.exec_())
