import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import uic
from custom_widgets import *

form_class = uic.loadUiType("layout.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 스타일시트 로드 및 적용
        with open("stylesheet.qss", "r") as f:
            style_sheet = f.read()
        self.apply_stylesheet(style_sheet)

        self.popUP = TempPopup(self)

        # 탭 1
        # 이미지 업로드 버튼 설정
        self.pushButton1.setText("Upload Image")
        self.pushButton1.clicked.connect(self.upload_image)

        # 그레이 스케일 변환 버튼 설정
        self.pushButton2.setText("Convert to Gray Scale")
        self.pushButton2.clicked.connect(self.cvt_gray_scale)

        # HSV 변환 버튼 설정
        self.pushButton3.setText("Convert to HSV")
        self.pushButton3.clicked.connect(self.cvt_hsv)

        # 이미지 자르기 버튼 설정
        self.pushButton4.setText("Crop Image")
        self.pushButton4.clicked.connect(self.start_crop_mode)

        # H, S, V 조절 토글 버튼 설정
        self.pushButton4_2.clicked.connect(self.toggle_h_adjustment)
        self.pushButton4_3.clicked.connect(self.toggle_s_adjustment)
        self.pushButton4_4.clicked.connect(self.toggle_v_adjustment)

        # 탭 2
        # Lab 이미지 변환 버튼 설정
        self.pushButton5.setText("Convert to Lab Image")
        self.pushButton5.clicked.connect(self.cvt_lab_image)

        # 반전 이미지 변환 버튼 설정
        self.pushButton6.setText("Convert to Invert Image")
        self.pushButton6.clicked.connect(self.cvt_invert_image)

        # 가우시안 블러 이미지 변환 버튼 설정
        self.pushButton7.setText("Convert to GaussianBlur Image")
        self.pushButton7.clicked.connect(self.cvt_GaussianBlur_image)

        # 샤프닝 이미지 변환 버튼 설정
        self.pushButton8.setText("Convert to Sharpen Image")
        self.pushButton8.clicked.connect(self.cvt_sharpen_image)

        # 슬라이더 1
        # 이미지 크기 조정 슬라이더 설정
        self.groupBox_12.setTitle("Image Size")
        self.horizontalSlider1.setMinimum(50)
        self.horizontalSlider1.setMaximum(400)
        self.horizontalSlider1.setValue(100)
        self.horizontalSlider1.valueChanged.connect(self.on_slider_value_changed)

        # 슬라이더 2
        # HSV 조절 슬라이더 설정
        self.groupBox_13.setTitle("HSV scale")
        self.horizontalSlider2.valueChanged.connect(self.on_slider2_value_changed)

        # 이미지 표시 영역 설정
        self.scroll_area = ScrollAreaWithDrag(self.frame)
        self.scroll_area.setGeometry(0, 0, self.frame.width(), self.frame.height())
        self.image_label = CustomLabel()  # 변경된 부분
        self.scroll_area.setWidget(self.image_label)

        self.image_label.setAlignment(Qt.AlignCenter)

        # 이미지 변환 상태를 저장하는 변수 초기화
        self.is_image_cvt = False
        self.is_grayScale = False
        self.is_hsv = False
        self.is_lab = False
        self.is_invert = False
        self.is_blur = False
        self.is_sharpen = False
        self.is_crop_mode = False
        self.crop_start = None
        self.crop_end = None
        self.crop_rectangle = None
        self.is_h_adjuseted = False
        self.is_s_adjuseted = False
        self.is_v_adjuseted = False

    def start_crop_mode(self):
        # 자르기 모드 시작
        self.is_crop_mode = True
        self.image_label.mousePressEvent = self.crop_start_event
        self.image_label.mouseReleaseEvent = self.crop_end_event
        self.pushButton4.setStyleSheet("background-color: black;")

    def crop_start_event(self, event):
        # 자르기 시작 좌표 설정
        self.crop_start = event.pos()
        self.image_label.mouseMoveEvent = self.crop_move_event

    def crop_move_event(self, event):
        # 마우스를 움직일 때 자르기 끝 좌표 설정
        self.crop_end = event.pos()
        self.image_label.set_crop_coordinates(self.crop_start, self.crop_end)

    def crop_end_event(self, event):
        # 자르기 종료 이벤트
        self.crop_end = event.pos()
        self.perform_crop()

        # 자르기 모드 및 좌표 초기화
        self.is_crop_mode = False
        self.crop_start = None
        self.crop_end = None
        self.image_label.mousePressEvent = None
        self.image_label.mouseReleaseEvent = None
        self.image_label.set_crop_coordinates(None, None)  # 자르기 좌표 초기화
        self.pushButton4.setStyleSheet("background-color: white;")

    def perform_crop(self):
        # 이미지 자르기 수행
        if not self.crop_start or not self.crop_end:
            return

        pixmap = self.image_label.pixmap()

        # QPixmap 내에서의 이미지 위치 계산
        pixmap_x = (self.image_label.width() - pixmap.width()) // 2
        pixmap_y = (self.image_label.height() - pixmap.height()) // 2

        # 자르기 좌표 조정
        adjusted_crop_start_x = self.crop_start.x() - pixmap_x
        adjusted_crop_start_y = self.crop_start.y() - pixmap_y
        adjusted_crop_end_x = self.crop_end.x() - pixmap_x
        adjusted_crop_end_y = self.crop_end.y() - pixmap_y

        cropped_pixmap = pixmap.copy(
            adjusted_crop_start_x,
            adjusted_crop_start_y,
            adjusted_crop_end_x - adjusted_crop_start_x,
            adjusted_crop_end_y - adjusted_crop_start_y,
        )
        self.image_label.setPixmap(cropped_pixmap)

        # QPixmap을 OpenCV 형식으로 변환
        ptr = cropped_pixmap.toImage().convertToFormat(QImage.Format_RGB888).bits()
        ptr.setsize(cropped_pixmap.height() * cropped_pixmap.width() * 3)
        cropped_image_arr = np.frombuffer(ptr, np.uint8).reshape(
            cropped_pixmap.height(), cropped_pixmap.width(), 3
        )

        print("자른 이미지의 크기:", cropped_image_arr.shape)
        print("자른 이미지의 데이터 타입:", cropped_image_arr.dtype)

        # 원본 및 크기 조정된 이미지 업데이트
        self.original_image = cropped_image_arr  # RGB 형식
        self.resized_image = self.original_image.copy()

    def apply_stylesheet(self, style_sheet):
        # 스타일시트 적용
        widgets = [self.tabWidget, self.frame, self.groupBox_12, self.groupBox_13] + [
            getattr(self, f"pushButton{i}") for i in range(1, 14)
        ]

        for widget in widgets:
            widget.setStyleSheet(style_sheet)

    def display_image(self, image):
        # 이미지를 PyQt의 라벨에 표시
        height, width, channel = image.shape
        bytes_per_line = channel * width
        q_image = QImage(
            image.data, width, height, bytes_per_line, QImage.Format_RGB888
        )
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)
        self.scroll_area.ensureVisible(0, 0)

    def upload_image(self):
        # 이미지 업로드
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "이미지 선택")
        if file_path:
            self.file_path = file_path
            original_image = cv2.imread(self.file_path)
            original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
            self.original_image = original_image.copy()

            # 이미지 크기 조정
            max_width = 551
            max_height = 461

            self.resized_image = self.resize_image(
                original_image, max_width, max_height
            )

            self.display_image(self.resized_image)

    def resize_image(self, image, max_width, max_height):
        # 이미지 크기 조정
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

    def on_slider_value_changed(self):
        # 슬라이더1의 값 변경 이벤트
        scale_value = self.horizontalSlider1.value()
        self.groupBox_12.setTitle(f"Image Size: {scale_value}%")

        # 크기 조정된 이미지 기준으로 크기 조절
        scaled_image = self.scale_image(self.resized_image, scale_value)

        # 현재 표시되는 이미지의 변환 상태에 따라 변환 적용
        if self.is_grayScale:
            scaled_image = cv2.cvtColor(scaled_image, cv2.COLOR_RGB2GRAY)
            scaled_image = cv2.cvtColor(scaled_image, cv2.COLOR_GRAY2RGB)

        if self.is_hsv:
            scaled_image = cv2.cvtColor(scaled_image, cv2.COLOR_RGB2HSV)

        # 변환된 이미지 라벨에 표시
        self.display_image(scaled_image)
        # Slider1의 현재 값 가져오기
        scale_value = self.horizontalSlider1.value()

        # self.resized_image를 기준으로 크기 조정
        scaled_image = self.scale_image(self.resized_image, scale_value)

        # 현재 표시되는 이미지의 변환 상태에 따라 변환 적용
        if self.is_grayScale:
            scaled_image = cv2.cvtColor(scaled_image, cv2.COLOR_RGB2GRAY)
            scaled_image = cv2.cvtColor(scaled_image, cv2.COLOR_GRAY2RGB)

        if self.is_hsv:
            scaled_image = cv2.cvtColor(scaled_image, cv2.COLOR_RGB2HSV)

        # 이미지 라벨에 조정된 이미지 표시
        self.display_image(scaled_image)

    def scale_image(self, image, scale_value):
        # 이미지 크기 조정 함수
        height, width, _ = image.shape
        new_height = int(height * scale_value / 100)
        new_width = int(width * scale_value / 100)

        scaled_image = cv2.resize(image, (new_width, new_height))

        return scaled_image

    def cvt_gray_scale(self):
        # 이미지를 그레이스케일로 변환
        pixmap = self.image_label.pixmap()

        if pixmap is not None:
            if self.is_grayScale:
                # 이미 그레이스케일로 변환된 경우 원본 이미지로 복원
                self.display_image(self.resized_image)
                self.pushButton2.setText("Convert to Gray Scale")
            else:
                # 그레이스케일로 이미지 변환
                self.popUP.show_message("Convert to Gray Scale", 1000)
                image = pixmap.toImage()
                gray_image = image.convertToFormat(QImage.Format_Grayscale8)
                pixmap = QPixmap.fromImage(gray_image)
                self.image_label.setPixmap(pixmap)
                self.pushButton2.setText("Restore Original")

            self.is_grayScale = not self.is_grayScale

    def cvt_hsv(self):
        # 이미지를 HSV 색공간으로 변환
        pixmap = self.image_label.pixmap()
        if pixmap is not None:
            if self.is_hsv:
                # 이미 HSV로 변환된 경우 원본 이미지로 복원
                self.display_image(self.resized_image)
                self.pushButton3.setText("Convert to HSV")
            else:
                # 이미지를 HSV로 변환
                self.popUP.show_message("Convert to HSV", 1000)
                ptr = pixmap.toImage().bits()
                ptr.setsize(pixmap.height() * pixmap.width() * 4)
                image_arr = np.frombuffer(ptr, np.uint8).reshape(
                    pixmap.height(), pixmap.width(), 4
                )
                hsv_image_arr = cv2.cvtColor(image_arr[:, :, :3], cv2.COLOR_BGR2HSV)
                height, width, channel = hsv_image_arr.shape
                bytesPerLine = 3 * width
                qImg = QImage(
                    hsv_image_arr.data,
                    width,
                    height,
                    bytesPerLine,
                    QImage.Format_RGB888,
                )
                self.image_label.setPixmap(QPixmap.fromImage(qImg))
                self.pushButton3.setText("Restore Original")

            self.is_hsv = not self.is_hsv

    def cvt_lab_image(self):
        # 이미지를 LAB 색공간으로 변환하는 함수
        image = self.resized_image
        pixmap = self.image_label.pixmap()
        if pixmap is not None:
            if self.is_lab:
                # 이미 LAB로 변환된 경우 원본 이미지로 복원
                self.display_image(self.resized_image)
                self.pushButton5.setText("Convert to Lab Image")
                self.is_lab = False
            else:
                # 이미지를 LAB로 변환
                self.popUP.show_message("Convert to Lab Image", 1000)
                lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
                height, width, channel = lab_image.shape
                bytes_per_line = channel * width
                q_image = QImage(
                    lab_image.data, width, height, bytes_per_line, QImage.Format_RGB888
                )
                pixmap = QPixmap.fromImage(q_image)
                self.image_label.setPixmap(pixmap)
                self.pushButton5.setText("Restore Original")
                self.is_lab = True

    def cvt_invert_image(self):
        # 이미지의 색상을 반전시키는 함수
        image = self.resized_image
        pixmap = self.image_label.pixmap()
        if pixmap is not None:
            if self.is_invert:
                # 이미 색상이 반전된 경우 원본 이미지로 복원
                self.display_image(self.resized_image)
                self.pushButton6.setText("Convert to Invert Image")
                self.is_invert = False
            else:
                # 이미지 색상 반전
                self.popUP.show_message("Convert to Invert Image", 1000)
                invert_image = cv2.bitwise_not(image)
                height, width, channel = invert_image.shape
                bytes_per_line = channel * width
                q_image = QImage(
                    invert_image.data,
                    width,
                    height,
                    bytes_per_line,
                    QImage.Format_RGB888,
                )
                pixmap = QPixmap.fromImage(q_image)
                self.image_label.setPixmap(pixmap)
                self.pushButton6.setText("Restore Original")
                self.is_invert = True

    def cvt_GaussianBlur_image(self):
        # 이미지에 가우시안 블러 효과를 적용하는 함수
        image = self.resized_image
        pixmap = self.image_label.pixmap()
        if pixmap is not None:
            if self.is_blur:
                # 이미 블러 효과가 적용된 경우 원본 이미지로 복원
                self.display_image(self.resized_image)
                self.pushButton7.setText("Convert to GaussianBlur Image")
                self.is_blur = False
            else:
                # 이미지에 가우시안 블러 효과 적용
                self.pushButton8.setText("Convert to GaussianBlur Image")
                blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
                height, width, channel = blurred_image.shape
                bytes_per_line = channel * width
                q_image = QImage(
                    blurred_image.data,
                    width,
                    height,
                    bytes_per_line,
                    QImage.Format_RGB888,
                )
                pixmap = QPixmap.fromImage(q_image)
                self.image_label.setPixmap(pixmap)
                self.pushButton7.setText("Restore Original")
                self.is_blur = True

    def cvt_sharpen_image(self):
        # 이미지를 더욱 선명하게 만드는 함수 (샤프닝)
        image = self.resized_image
        pixmap = self.image_label.pixmap()
        if pixmap is not None:
            if self.is_sharpen:
                # 이미 샤프닝이 적용된 경우 원본 이미지로 복원
                self.display_image(self.resized_image)
                self.pushButton8.setText("Convert to Sharpen Image")
                self.is_sharpen = False
            else:
                # 이미지에 샤프닝 효과 적용
                self.popUP.show_message("Convert to Sharpen Image", 1000)
                sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
                sharpened_image = cv2.filter2D(image, -1, sharpen_kernel)
                self.display_image(sharpened_image)
                self.pushButton8.setText("Restore Original")
                self.is_sharpen = True

    def on_slider2_value_changed(self):
        # 슬라이더의 값이 변경될 때 호출되는 함수 (H, S, V 조절에 사용)
        hsv_scale_value = self.horizontalSlider2.value()
        self.groupBox_13.setTitle(f"HSV scale: {hsv_scale_value}")
        if self.is_h_adjuseted:
            self.cvt_h_based_on_slider()
        if self.is_s_adjuseted:
            self.cvt_s_based_on_slider()
        if self.is_v_adjuseted:
            self.cvt_v_based_on_slider()

    def toggle_h_adjustment(self):
        # H(색조) 조절 모드를 토글하는 함수
        self.is_h_adjuseted = not self.is_h_adjuseted
        if self.is_h_adjuseted:
            self.popUP.show_message("Convert to H Scale", 1000)
            self.pushButton4_2.setStyleSheet("background-color: lightgreen;")
            self.is_s_adjuseted = False
            self.pushButton4_3.setStyleSheet("")  # 기본 스타일로 복귀
            self.is_v_adjuseted = False
            self.pushButton4_4.setStyleSheet("")  # 기본 스타일로 복귀
        else:
            self.pushButton4_2.setStyleSheet("")
            self.display_image(self.resized_image)

    def toggle_s_adjustment(self):
        # S(채도) 조절 모드를 토글하는 함수
        self.is_s_adjuseted = not self.is_s_adjuseted
        if self.is_s_adjuseted:
            self.popUP.show_message("Convert to S Scale", 1000)
            self.pushButton4_3.setStyleSheet("background-color: lightgreen;")
            self.is_h_adjuseted = False
            self.pushButton4_2.setStyleSheet("")
            self.is_v_adjuseted = False
            self.pushButton4_4.setStyleSheet("")
        else:
            self.pushButton4_3.setStyleSheet("")
            self.display_image(self.resized_image)

    def toggle_v_adjustment(self):
        # V(밝기) 조절 모드를 토글하는 함수
        self.is_v_adjuseted = not self.is_v_adjuseted
        if self.is_v_adjuseted:
            self.popUP.show_message("Convert to V Scale", 1000)
            self.pushButton4_4.setStyleSheet("background-color: lightgreen;")
            self.is_h_adjuseted = False
            self.pushButton4_2.setStyleSheet("")
            self.is_s_adjuseted = False
            self.pushButton4_3.setStyleSheet("")
        else:
            self.pushButton4_4.setStyleSheet("")
            self.display_image(self.resized_image)

    def get_slider_value(self):
        # 현재 슬라이더의 값을 반환하는 함수
        return self.horizontalSlider2.value()

    def cvt_h_based_on_slider(self):
        # 슬라이더의 값에 따라 이미지의 H(색조)를 조절하는 함수
        if self.is_h_adjuseted:
            value = self.get_slider_value()
            hsv_image = cv2.cvtColor(self.resized_image, cv2.COLOR_RGB2HSV)
            h_channel = hsv_image[:, :, 0]
            adjusted_h_channel = np.mod(h_channel + value, 180)
            hsv_image[:, :, 0] = adjusted_h_channel
            rgb_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB)
            self.display_image(rgb_image)

    def cvt_s_based_on_slider(self):
        # 슬라이더의 값에 따라 이미지의 S(채도)를 조절하는 함수
        if self.is_s_adjuseted:
            s_value = self.horizontalSlider2.value()
            hsv_image = cv2.cvtColor(self.resized_image, cv2.COLOR_RGB2HSV)
            hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] + s_value, 0, 255)
            rgb_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB)
            self.display_image(rgb_image)

    def cvt_v_based_on_slider(self):
        # 슬라이더의 값에 따라 이미지의 V(밝기)를 조절하는 함수
        if self.is_v_adjuseted:
            v_value = self.horizontalSlider2.value()
            hsv_image = cv2.cvtColor(self.resized_image, cv2.COLOR_RGB2HSV)
            hsv_image[:, :, 2] = np.clip(hsv_image[:, :, 2] + v_value, 0, 255)
            rgb_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB)
            self.display_image(rgb_image)
