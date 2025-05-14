# ----------头文件----------
import sys
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QApplication, QWidget
import math
# ----------控件----------
class Corrugated_Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # ----------状态----------
        self.state = True                                                               # 控制展开/收缩
        # ----------颜色----------
        self.fill_circle = QColor(0, 0, 0)
        self.fill_background = QColor(255, 255, 255)
        self.fill_color = self.fill_circle if self.state else self.fill_background      # 当前填充色，默认为黑色
        # ----------尺寸----------
        self.min_radius = 0                                                             # 最小半径（收缩状态）
        self.max_radius = math.hypot(self.width(), self.height())                       # 最大半径（对角线长度）
        self.radius = 0                                                                 # 当前半径
        # ----------窗口点击位置----------
        self.mouse_point = None                                                         # 记录点击位置
        self.init_animation()                                                           # 初始化动画系统

    def set_fill_color(self, *color):
        print(type(color))
        """设置填充颜色（支持单/双参数）"""
        # 参数数量验证
        if len(color) < 1 or len(color) > 2:
            raise ValueError("参数数量错误，支持1-2个颜色参数")
        color1 = color[0]                                                               # 处理第一个颜色
        if isinstance(color1, QColor):
            self.fill_color = color1
        elif isinstance(color1, (tuple, list)):
            if len(color1) in (3, 4):
                self.fill_color = QColor(*color1)
            else:
                raise ValueError("颜色元组需要3或4个元素")
        elif isinstance(color1, str):
            self.fill_color = QColor(color1)
        else:
            raise ValueError(f"无效的颜色格式: {type(color1)}")
        if len(color) == 2:                                                             # 处理第二个颜色
            color2 = color[1]
            if isinstance(color2, QColor):
                self.fill_background = color2
            elif isinstance(color2, (tuple, list)):
                if len(color2) in (3, 4):
                    self.fill_background = QColor(*color2)
                else:
                    raise ValueError("颜色元组需要3或4个元素")
            elif isinstance(color2, str):
                self.fill_background = QColor(color2)
            else:
                raise ValueError(f"无效的颜色格式: {type(color2)}")

        self.update()

    def resizeEvent(self, event):
        """窗口尺寸改变事件处理"""
        self.max_radius = math.hypot(self.width(), self.height())                       # 重新计算最大半径
        # print(f"半径为{self.max_radius}")
        super().resizeEvent(event)

    def init_animation(self):
        """初始化动画属性"""
        self.animation = QPropertyAnimation(self, b'radius_point')                      # 绑定自定义属性
        self.animation.setDuration(600)                                                 # 设定动画时间
        self.animation.setEasingCurve(QEasingCurve.OutQuad)                             # 设定动画方式

    @pyqtProperty(float)                                                                # getter方法
    def radius_point(self):
        return self.radius
    @radius_point.setter                                                                # setter方法
    def radius_point(self, value):
        self.radius = value
        self.update()

    def paintEvent(self, event):
        """自定义绘制事件"""
        if self.mouse_point is not None:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(Qt.NoPen)

            # 现在不依赖self.state来决定涂刷颜色
            painter.setBrush(self.fill_color)

            # 执行涟漪效果的绘制
            painter.drawEllipse(self.mouse_point, self.radius, self.radius)
        else:
            pass
            # print(self.mouse_point)

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
    widget.set_fill_color("#FF0000", "#FFFFFF")        # 同时设置两个颜色
    sys.exit(app.exec_())