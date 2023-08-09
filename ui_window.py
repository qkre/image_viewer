import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import uic
from custom_widgets import ScrollAreaWithDrag, CustomLabel

form_class = uic.loadUiType("layout.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        with open("stylesheet.qss", "r") as f:
            style_sheet = f.read()

        self.apply_stylesheet(style_sheet)

        # 탭 1
        self.pushButton1.setText("Upload Image")
        self.pushButton1.clicked.connect(self.upload_image)

        self.pushButton2.setText("Convert to Gray Scale")
        self.pushButton2.clicked.connect(self.cvt_gray_scale)

        self.pushButton3.setText("Convert to HSV")
        self.pushButton3.clicked.connect(self.cvt_hsv)

        # Create pushButton4 for cropping
        self.pushButton4.setText("Crop Image")
        self.pushButton4.clicked.connect(self.start_crop_mode)

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
        self.scroll_area = ScrollAreaWithDrag(self.frame)
        self.scroll_area.setGeometry(0, 0, self.frame.width(), self.frame.height())
        self.image_label = CustomLabel()  # 변경된 부분
        self.scroll_area.setWidget(self.image_label)

        self.image_label.setAlignment(Qt.AlignCenter)

        # 이미지 변환 상태 여부 저장하는 변수
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

    def start_crop_mode(self):
        self.is_crop_mode = True
        self.image_label.mousePressEvent = self.crop_start_event
        self.image_label.mouseReleaseEvent = self.crop_end_event
        self.pushButton4.setStyleSheet("background-color: black;")

    def crop_start_event(self, event):
        self.crop_start = event.pos()
        self.image_label.mouseMoveEvent = self.crop_move_event

    def crop_move_event(self, event):
        self.crop_end = event.pos()
        self.image_label.set_crop_coordinates(self.crop_start, self.crop_end)

    def crop_end_event(self, event):
        self.crop_end = event.pos()
        self.perform_crop()

        # Reset cropping mode and positions
        self.is_crop_mode = False
        self.crop_start = None
        self.crop_end = None
        self.image_label.mousePressEvent = None
        self.image_label.mouseReleaseEvent = None
        self.image_label.set_crop_coordinates(None, None)  # Reset crop coordinates
        self.pushButton4.setStyleSheet("background-color: white;")

    def perform_crop(self):
        if not self.crop_start or not self.crop_end:
            return

        pixmap = self.image_label.pixmap()

        # Calculate the position of the pixmap within the QLabel
        pixmap_x = (self.image_label.width() - pixmap.width()) // 2
        pixmap_y = (self.image_label.height() - pixmap.height()) // 2

        # Adjust the crop coordinates based on the pixmap's position
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

        # Convert QPixmap to OpenCV format for further processing
        ptr = cropped_pixmap.toImage().convertToFormat(QImage.Format_RGB888).bits()
        ptr.setsize(cropped_pixmap.height() * cropped_pixmap.width() * 3)
        cropped_image_arr = np.frombuffer(ptr, np.uint8).reshape(
            cropped_pixmap.height(), cropped_pixmap.width(), 3
        )

        print("Cropped Image Shape:", cropped_image_arr.shape)
        print("Cropped Image Dtype:", cropped_image_arr.dtype)

        # Update both original and resized images
        self.original_image = cropped_image_arr  # Already in RGB format
        self.resized_image = self.original_image.copy()

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
        )
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)
        self.scroll_area.ensureVisible(0, 0)

    def upload_image(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Select Image")
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
        # 이미지 크기 조정
        height, width, _ = image.shape
        new_height = int(height * scale_value / 100)
        new_width = int(width * scale_value / 100)

        scaled_image = cv2.resize(image, (new_width, new_height))

        return scaled_image

    def cvt_gray_scale(self):
        pixmap = self.image_label.pixmap()
        if pixmap is not None:
            if self.is_grayScale:
                # 이미 변환된 상태일 때는 원본 이미지로 돌아감
                self.display_image(self.resized_image)
                self.pushButton2.setText("Convert to Gray Scale")
            else:
                # 아직 변환되지 않은 상태일 때는 현재 화면에 보여지는 이미지를 그레이스케일로 변환
                image = pixmap.toImage()
                gray_image = image.convertToFormat(QImage.Format_Grayscale8)
                pixmap = QPixmap.fromImage(gray_image)
                self.image_label.setPixmap(pixmap)
                self.pushButton2.setText("Restore Original")

            self.is_grayScale = not self.is_grayScale

    def cvt_hsv(self):
        pixmap = self.image_label.pixmap()
        if pixmap is not None:
            if self.is_hsv:
                # 이미 변환된 상태일 때는 원본 이미지로 돌아감
                self.display_image(self.resized_image)
                self.pushButton3.setText("Convert to HSV")
            else:
                # Convert QImage to numpy array (OpenCV format)
                ptr = pixmap.toImage().bits()
                ptr.setsize(pixmap.height() * pixmap.width() * 4)
                image_arr = np.frombuffer(ptr, np.uint8).reshape(
                    pixmap.height(), pixmap.width(), 4
                )

                # Convert the image to HSV using OpenCV
                hsv_image_arr = cv2.cvtColor(image_arr[:, :, :3], cv2.COLOR_BGR2HSV)

                # Convert the numpy array back to QImage
                height, width, channel = hsv_image_arr.shape
                bytesPerLine = 3 * width
                qImg = QImage(
                    hsv_image_arr.data,
                    width,
                    height,
                    bytesPerLine,
                    QImage.Format_RGB888,
                )

                # Set the converted image to the label
                self.image_label.setPixmap(QPixmap.fromImage(qImg))
                self.pushButton3.setText("Restore Original")

            self.is_hsv = not self.is_hsv

    def cvt_lab_image(self):
        image = self.resized_image

        pixmap = self.image_label.pixmap()
        if pixmap is not None:
            # 이미지 변환 상태 여부에 따라 처리
            if self.is_lab:
                # 이미 변환된 상태일 때는 원본 이미지를 표시
                self.display_image(self.resized_image)
                self.pushButton5.setText("Convert to Lab Image")  # 버튼 텍스트 변경
                self.is_lab = False
            else:
                # 아직 변환되지 않은 상태일 때는 이미지 밝기 강조, 녹색을 마젠타 색, 파랑색을 노랑색으로 반전 처리로 변환된 이미지를 표시
                lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
                height, width, channel = lab_image.shape
                bytes_per_line = channel * width
                q_image = QImage(
                    lab_image.data, width, height, bytes_per_line, QImage.Format_RGB888
                )
                pixmap = QPixmap.fromImage(q_image)
                self.image_label.setPixmap(pixmap)
                self.pushButton5.setText("Restore Original")  # 버튼 텍스트 변경
                self.is_lab = True

    def cvt_invert_image(self):
        image = self.resized_image

        pixmap = self.image_label.pixmap()
        if pixmap is not None:
            # 이미지 변환 상태 여부에 따라 처리
            if self.is_invert:
                # 이미 변환된 상태일 때는 원본 이미지를 표시
                self.display_image(self.resized_image)
                self.pushButton6.setText("Convert to Invert Image")  # 버튼 텍스트 변경
                self.is_invert = False
            else:
                # 이미지 전체 색상 반전로 변환된 이미지를 표시
                invert_image = cv2.bitwise_not(image)
                # 변환된 이미지를 PyQt의 라벨에 표시
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
                self.pushButton6.setText("Restore Original")  # 버튼 텍스트 변경
                self.is_invert = True

    def cvt_GaussianBlur_image(self):
        image = self.resized_image

        pixmap = self.image_label.pixmap()
        if pixmap is not None:
            # 이미지 변환 상태 여부에 따라 처리
            if self.is_blur:
                # 이미 변환된 상태일 때는 원본 이미지를 표시
                self.display_image(self.resized_image)
                self.pushButton7.setText("Convert to GaussianBlur Image")  # 버튼 텍스트 변경
                self.is_blur = False
            else:
                # 아직 변환되지 않은 상태일 때는 가우시안 블러로 변환된 이미지를 표시
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
                self.pushButton7.setText("Restore Original")  # 버튼 텍스트 변경
                self.is_blur = True

    def cvt_sharpen_image(self):
        image = self.resized_image

        pixmap = self.image_label.pixmap()
        if pixmap is not None:
            # 이미지 변환 상태 여부에 따라 처리
            if self.is_sharpen:
                # 이미 변환된 상태일 때는 원본 이미지를 표시
                self.display_image(self.resized_image)
                self.pushButton8.setText("Convert to Sharpen Image")  # 버튼 텍스트 변경
                self.is_sharpen = False
            else:
                # 아직 변환되지 않은 상태일 때는 샤프닝 필터를 적용한 이미지를 표시
                sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
                sharpened_image = cv2.filter2D(image, -1, sharpen_kernel)

                # 이미지 라벨에 조정된 이미지 표시
                self.display_image(sharpened_image)
                self.pushButton8.setText("Restore Original")  # 버튼 텍스트 변경
                self.is_sharpen = True
