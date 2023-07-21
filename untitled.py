import sys
import cv2
import numpy as np
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

        self.apply_stylesheet(style_sheet)

        # 탭 1
        self.pushButton1.setText("Upload Image")
        self.pushButton1.clicked.connect(self.upload_image)

        self.pushButton2.setText("Convert to Gray Scale")
        self.pushButton2.clicked.connect(self.cvt_gray_scale)

        self.pushButton3.setText("Convert to HSV")
        self.pushButton3.clicked.connect(self.cvt_hsv)

        # 탭 2
        self.pushButton5.setText("Convert to Lab Image")
        self.pushButton5.clicked.connect(self.cvt_lab_image)

        self.pushButton6.setText("Convert to Invert Image")
        self.pushButton6.clicked.connect(self.cvt_invert_image)
        
        self.pushButton7.setText("Convert to GaussianBlur Image")
        self.pushButton7.clicked.connect(self.cvt_GaussianBlur_image)

        self.pushButton8.setText("Convert to Sharpen Image")
        self.pushButton8.clicked.connect(self.cvt_sharpen_image)

        
        
        
        # 슬라이더 1
        self.groupBox_12.setTitle("Image Size")
        self.horizontalSlider1.setMinimum(50)
        self.horizontalSlider1.setMaximum(400)
        self.horizontalSlider1.setValue(100)
        self.horizontalSlider1.valueChanged.connect(self.on_slider_value_changed)

        # 이미지 영역
        self.image_label = QLabel(self.frame)  # image_label을 frame 위젯의 자식으로 설정
        self.image_label.setGeometry(0, 0, self.frame.width(), self.frame.height())

        # 불러온 이미지의 크기 고정
        self.image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.image_label.setAlignment(Qt.AlignCenter)

        # 이미지 변환 상태 여부 저장하는 변수
        self.is_image_cvt = False

    def apply_stylesheet(self, style_sheet):
        widgets = [self.tabWidget, self.frame, self.groupBox_12, self.groupBox_13] + [
            getattr(self, f"pushButton{i}") for i in range(1, 14)
        ]

        for widget in widgets:
            widget.setStyleSheet(style_sheet)

    # 이미지를 PyQt의 라벨에 표시
    def display_image(self, image):
        height, width, channel = image.shape
        bytes_per_line = channel * width
        q_image = QImage(
            image.data, width, height, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)

    def upload_image(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Select Image")
        if file_path:
            self.file_path = file_path
            original_image = cv2.imread(self.file_path)

            # 이미지 크기 조정
            max_width = 551
            max_height = 461
            self.original_image = self.resize_image(
                original_image, max_width, max_height
            )

            self.display_image(self.original_image)

    def resize_image(self, image, max_width, max_height):
        height, width, _ = image.shape
        aspect_ratio = width / height

        if width > max_width:
            width = max_width
            height = int(width / aspect_ratio)

        if height > max_height:
            height = max_height
            width = int(height * aspect_ratio)

        resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
        return resized_image

    def cvt_gray_scale(self):
        image = self.original_image

        # 이미지 변환 상태 여부에 따라 처리
        if self.is_image_cvt:
            # 이미 변환된 상태일 때는 원본 이미지를 표시
            self.display_image(self.original_image)
            self.pushButton2.setText("Convert to Gray Scale")  # 버튼 텍스트 변경
            self.is_image_cvt = False
        else:
            # 아직 변환되지 않은 상태일 때는 그레이스케일로 변환된 이미지를 표시
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            height, width = gray_image.shape
            bytes_per_line = width
            q_image = QImage(
                gray_image.data, width, height, bytes_per_line, QImage.Format_Grayscale8
            )
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap)
            self.pushButton2.setText("Restore Original")  # 버튼 텍스트 변경
            self.is_image_cvt = True

    def cvt_hsv(self):
        image = self.original_image

        # 이미지 변환 상태 여부에 따라 처리
        if self.is_image_cvt:
            # 이미 변환된 상태일 때는 원본 이미지를 표시
            self.display_image(self.original_image)
            self.pushButton3.setText("Convert to HSV")  # 버튼 텍스트 변경
            self.is_image_cvt = False
        else:
            # 아직 변환되지 않은 상태일 때는 HSV로 변환된 이미지를 표시
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            height, width, channel = hsv_image.shape
            bytes_per_line = channel * width
            q_image = QImage(
                hsv_image.data, width, height, bytes_per_line, QImage.Format_RGB888
            ).rgbSwapped()
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap)
            self.pushButton3.setText("Restore Original")  # 버튼 텍스트 변경
            self.is_image_cvt = True

    def on_slider_value_changed(self):
        # Slider1의 현재 값 가져오기
        scale_value = self.horizontalSlider1.value()

        # 현재 슬라이더 값으로 이미지 크기 조정
        scaled_image = self.scale_image(self.original_image, scale_value)

        # 이미지 라벨에 조정된 이미지 표시
        self.display_image(scaled_image)

    def scale_image(self, image, scale_value):
        # 이미지 크기 조정
        height, width, _ = image.shape
        new_height = int(height * scale_value / 100)
        new_width = int(width * scale_value / 100)

        scaled_image = cv2.resize(image, (new_width, new_height))

        return scaled_image
    
    def cvt_lab_image(self):
        image = self.original_image

        # 이미지 변환 상태 여부에 따라 처리
        if self.is_image_cvt:
            # 이미 변환된 상태일 때는 원본 이미지를 표시
            self.display_image(self.original_image)
            self.pushButton5.setText("Convert to Lab Image")  # 버튼 텍스트 변경
            self.is_image_cvt = False
        else:
            # 아직 변환되지 않은 상태일 때는 이미지 밝기 강조, 녹색을 마젠타 색, 파랑색을 노랑색으로 반전 처리로 변환된 이미지를 표시
            lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            height, width, channel =  lab_image.shape
            bytes_per_line = channel * width
            q_image = QImage(
            lab_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap)
            self.pushButton5.setText("Restore Original")  # 버튼 텍스트 변경
            self.is_image_cvt = True
    
    def cvt_invert_image(self):
        image = self.original_image

        # 이미지 변환 상태 여부에 따라 처리
        if self.is_image_cvt:
            # 이미 변환된 상태일 때는 원본 이미지를 표시
            self.display_image(self.original_image)
            self.pushButton6.setText("Convert to Invert Image")  # 버튼 텍스트 변경
            self.is_image_cvt = False
        else:
            # 이미지 전체 색상 반전로 변환된 이미지를 표시
            invert_image = cv2.bitwise_not(image) 
            # 변환된 이미지를 PyQt의 라벨에 표시
            height, width, channel = invert_image.shape
            bytes_per_line = channel * width
            q_image = QImage(
                invert_image.data, width, height, bytes_per_line, QImage.Format_RGB888
            )
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap)  
            self.pushButton6.setText("Restore Original")  # 버튼 텍스트 변경
            self.is_image_cvt = True

    def cvt_GaussianBlur_image(self):
        image = self.original_image

        # 이미지 변환 상태 여부에 따라 처리
        if self.is_image_cvt:
            # 이미 변환된 상태일 때는 원본 이미지를 표시
            self.display_image(self.original_image)
            self.pushButton7.setText("Convert to GaussianBlur Image")  # 버튼 텍스트 변경
            self.is_image_cvt = False
        else:
            # 아직 변환되지 않은 상태일 때는 가우시안 블러로 변환된 이미지를 표시
            blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
            height, width, channel = blurred_image.shape
            bytes_per_line = channel * width
            q_image = QImage(
                blurred_image.data, width, height, bytes_per_line, QImage.Format_RGB888
            )
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap)
            self.pushButton7.setText("Restore Original")  # 버튼 텍스트 변경
            self.is_image_cvt = True

    def cvt_sharpen_image(self):
        image = self.original_image

        # 이미지 변환 상태 여부에 따라 처리
        if self.is_image_cvt:
            # 이미 변환된 상태일 때는 원본 이미지를 표시
            self.display_image(self.original_image)
            self.pushButton8.setText("Convert to Sharpen Image")  # 버튼 텍스트 변경
            self.is_image_cvt = False
        else:
            # 아직 변환되지 않은 상태일 때는 샤프닝 필터를 적용한 이미지를 표시
            sharpen_kernel = np.array([[-1, -1, -1],
                                       [-1,  9, -1],
                                       [-1, -1, -1]])
            sharpened_image = cv2.filter2D(image, -1, sharpen_kernel)

            # 이미지 라벨에 조정된 이미지 표시
            self.display_image(sharpened_image)
            self.pushButton8.setText("Restore Original")  # 버튼 텍스트 변경
            self.is_image_cvt = True
    
    
        
    
    


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
