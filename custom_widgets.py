from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class TempPopup(QFrame):
    def __init__(self, parent=None):
        super(TempPopup, self).__init__(parent)
        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.hide)

        # Set the style for the frame
        self.setStyleSheet(
            "border: 2px solid black;"  # Border
            "background-color: white;"  # Background color
            "border-radius: 5px;"  # Rounded corners
        )

        self.layout = QVBoxLayout(self)
        self.message_label = QLabel(self)
        self.message_label.setStyleSheet(
            "font-size: 18px; padding: 2px 4px;" "border: None;"
        )
        self.layout.addWidget(self.message_label)

    def show_message(self, message, duration=2000):
        self.message_label.setText(message)
        self.adjustSize()  # Adjust to fit the text

        if self.parent():
            parent_widget = (
                self.parent().image_label
            )  # Referencing the image_label in parent
            global_position = parent_widget.mapToGlobal(QPoint(0, 0))
            # Calculate the position relative to the global coordinates of the image_label
            x_pos = global_position.x() + (parent_widget.width() - self.width()) / 2
            y_pos = global_position.y()  # Positioning at the top of image_label
            self.move(x_pos, y_pos)
        self.show()
        self.timer.start(duration)


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
