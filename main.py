# ----------头文件----------
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRectF, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtWidgets import QApplication, QWidget

import math
# ----------控件----------
class Corrugated_Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # ----------状态----------
        self.state = True
        # ----------颜色----------
        self.fill_black = QColor(0, 0, 0)
        self.fill_white = QColor(255, 255, 255)
        self.fill_color = QColor(0, 0, 0)
        # ----------尺寸----------
        self.min_radius = 0
        self.max_radius = math.hypot(self.width(), self.height())
        self.radius = 0
        # ----------圆角尺寸----------
        self.btn_radius = 10
        # ----------窗口点击位置----------
        self.mouse_point = None
        self.init_animation()

    def resizeEvent(self, event):
        self.max_radius = math.hypot(self.width(), self.height())
        super().resizeEvent(event)

    def init_animation(self):
        self.animation = QPropertyAnimation(self, b'radius_point')
        self.animation.setDuration(450)
        self.animation.setEasingCurve(QEasingCurve.OutQuad)

    def set_fill_color(self, fill_color):
        self.fill_color = fill_color
        self.update()

    @pyqtProperty(float)
    def radius_point(self):
        return self.radius
    @radius_point.setter
    def radius_point(self, value):
        self.radius = value
        self.update()

    def paintEvent(self, event):
        if self.mouse_point is not None:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(Qt.NoPen)

            # 现在不依赖self.state来决定涂刷颜色
            painter.setBrush(self.fill_color)

            # 执行涟漪效果的绘制
            painter.drawEllipse(self.mouse_point, self.radius, self.radius)
        else:
            print(self.mouse_point)

    def mousePressEvent(self, event):
        self.mouse_point = event.pos()
        self.animation.stop()
        self.animation.setStartValue(self.min_radius if self.state else self.max_radius)
        self.animation.setEndValue(self.max_radius if self.state else self.min_radius)
        self.animation.start()
        self.state = not self.state

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Corrugated_Widget()
    widget.show()
    sys.exit(app.exec_())