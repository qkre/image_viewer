import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("untitled.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        with open("stylesheet_untitled.qss", "r") as f:
            style_sheet = f.read()

        self.pushButton1.setStyleSheet(style_sheet)
        self.pushButton2.setStyleSheet(style_sheet)
        self.pushButton3.setStyleSheet(style_sheet)
        self.pushButton4.setStyleSheet(style_sheet)
        self.pushButton5.setStyleSheet(style_sheet)
        self.pushButton6.setStyleSheet(style_sheet)
        self.pushButton7.setStyleSheet(style_sheet)
        self.pushButton8.setStyleSheet(style_sheet)
        self.pushButton9.setStyleSheet(style_sheet)
        self.pushButton10.setStyleSheet(style_sheet)
        self.pushButton11.setStyleSheet(style_sheet)
        self.pushButton12.setStyleSheet(style_sheet)
        self.pushButton13.setStyleSheet(style_sheet)
        self.groupBox.setStyleSheet(style_sheet)
        self.groupBox_2.setStyleSheet(style_sheet)
        self.groupBox_3.setStyleSheet(style_sheet)
        self.groupBox_4.setStyleSheet(style_sheet)
        self.groupBox_5.setStyleSheet(style_sheet)
        self.groupBox_6.setStyleSheet(style_sheet)
        self.groupBox_7.setStyleSheet(style_sheet)
        self.groupBox_8.setStyleSheet(style_sheet)
        self.groupBox_9.setStyleSheet(style_sheet)
        self.groupBox_10.setStyleSheet(style_sheet)
        self.groupBox_11.setStyleSheet(style_sheet)
        self.groupBox_12.setStyleSheet(style_sheet)
        self.groupBox_13.setStyleSheet(style_sheet)
        self.tabWidget.setStyleSheet(style_sheet)
        self.frame.setStyleSheet(style_sheet)

        self.pushButton1.clicked.connect(self.pushButton)

        self.image_label = QLabel(self)
        self.image_label.setGeometry(20, 20, 550, 460)  # 좌표와 크기 설정
        # 불러온 이미지의 크기 고정
        self.image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.image_label.setFixedSize(550, 460)
        self.image_label.setAlignment(Qt.AlignCenter)

        # 이미지 로드 및 표시
        image = self.load_image()
        self.original_image = image  # 원본 이미지 저장
        self.display_image(image)

    def load_image(self):
        image_path = "images/image.jfif"  # 이미지 경로 설정
        image = cv2.imread(image_path)

        return image

    # 이미지를 PyQt의 라벨에 표시
    def display_image(self, image):
        height, width, channel = image.shape
        bytes_per_line = channel * width
        q_image = QImage(
            image.data, width, height, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)

    def pushButton(self):
        image = self.load_image()  # 이미지 로드

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 이미지를 그레이스케일로 변환

        # 변환된 이미지를 PyQt의 라벨에 표시
        height, width = gray_image.shape
        bytes_per_line = width
        q_image = QImage(
            gray_image.data, width, height, bytes_per_line, QImage.Format_Grayscale8
        )
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
