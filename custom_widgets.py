from PyQt5.QtWidgets import QScrollArea, QLabel
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QRect


class ScrollAreaWithDrag(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.image_label = QLabel()
        self.setWidget(self.image_label)

        self.mouse_press_pos = None
        self.scroll_bar_value_on_press = None

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.mouse_press_pos = event.pos()
            self.scroll_bar_value_on_press = (
                self.horizontalScrollBar().value(),
                self.verticalScrollBar().value(),
            )
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.mouse_press_pos:
            diff = event.pos() - self.mouse_press_pos
            h_scroll_value, v_scroll_value = self.scroll_bar_value_on_press
            self.horizontalScrollBar().setValue(h_scroll_value - diff.x())
            self.verticalScrollBar().setValue(v_scroll_value - diff.y())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.mouse_press_pos = None
        super().mouseReleaseEvent(event)


class CustomLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.crop_start = None
        self.crop_end = None

    def set_crop_coordinates(self, start, end):
        self.crop_start = start
        self.crop_end = end
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.crop_start and self.crop_end:
            painter = QPainter(self)
            rect = QRect(self.crop_start, self.crop_end)
            painter.setPen(QPen(Qt.red, 2))
            painter.drawRect(rect)
            painter.end()
