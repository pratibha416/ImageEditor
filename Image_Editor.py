import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QHBoxLayout, QInputDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PIL import Image, ImageEnhance
import numpy as np

class ImageEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Editor with PyQt5 & Pillow")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        # display the image
        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label)

        # Buttons for basic image operations
        self.buttons_layout = QHBoxLayout()
        self.open_button = QPushButton("Open Image")
        self.resize_button = QPushButton("Resize Image")
        self.rotate_button = QPushButton("Rotate Image")
        self.save_button = QPushButton("Save Image")
        self.grayscale_button = QPushButton("Convert to Grayscale")
        self.brightness_button = QPushButton("Adjust Brightness")
        self.contrast_button = QPushButton("Adjust Contrast")
        self.flip_button = QPushButton("Flip Image")

        self.buttons_layout.addWidget(self.open_button)
        self.buttons_layout.addWidget(self.resize_button)
        self.buttons_layout.addWidget(self.rotate_button)
        self.buttons_layout.addWidget(self.grayscale_button)
        self.buttons_layout.addWidget(self.brightness_button)
        self.buttons_layout.addWidget(self.contrast_button)
        self.buttons_layout.addWidget(self.flip_button)
        self.buttons_layout.addWidget(self.save_button)

        self.layout.addLayout(self.buttons_layout)
        self.setLayout(self.layout)

        # Initialize image variable
        self.image = None

        # Connecting buttons to their respective functions
        self.open_button.clicked.connect(self.open_image)
        self.resize_button.clicked.connect(self.resize_image)
        self.rotate_button.clicked.connect(self.rotate_image)
        self.save_button.clicked.connect(self.save_image)
        self.grayscale_button.clicked.connect(self.convert_to_grayscale)
        self.brightness_button.clicked.connect(self.adjust_brightness)
        self.contrast_button.clicked.connect(self.adjust_contrast)
        self.flip_button.clicked.connect(self.flip_image)

    def open_image(self):
        """ Open an image file """
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.xpm *.jpg *.bmp)")
        if file_name:
            self.image = Image.open(file_name)  # Open the image using Pillow
            self.display_image()

    def display_image(self):
        """ Display the image in the QLabel """
        if self.image:
            # Convert the Pillow image to QImage
            image_array = np.array(self.image)  # Convert the Pillow image to a numpy array

            if len(image_array.shape) == 2:  # Grayscale image
                height, width = image_array.shape
                bytes_per_line = width
                qt_image = QImage(image_array.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
            elif len(image_array.shape) == 3 and image_array.shape[2] == 3:  
                height, width, _ = image_array.shape
                bytes_per_line = 3 * width
                qt_image = QImage(image_array.data, width, height, bytes_per_line, QImage.Format_RGB888)
            elif len(image_array.shape) == 3 and image_array.shape[2] == 4: 
                height, width, _ = image_array.shape
                bytes_per_line = 4 * width
                qt_image = QImage(image_array.data, width, height, bytes_per_line, QImage.Format_RGBA8888)
            else:
                raise ValueError("Unsupported image mode")

            # Create a QPixmap from QImage
            pixmap = QPixmap.fromImage(qt_image)
            self.image_label.setPixmap(pixmap)
            self.image_label.setAlignment(Qt.AlignCenter)  # Center the image

    def resize_image(self):
        """ Resize the image to half of its current size """
        if self.image:
            width, height = self.image.size
            new_width = width // 2
            new_height = height // 2
            self.image = self.image.resize((new_width, new_height))  # Resize using Pillow
            self.display_image()  # Update the displayed image

    def rotate_image(self):
        """ Rotate the image 90 degrees """
        if self.image:
            self.image = self.image.rotate(90, expand=True)  # Rotate using Pillow
            self.display_image()  # Update the displayed image

    def save_image(self):
        """ Save the current image to a file """
        if self.image:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.xpm *.jpg *.bmp)")
            if file_name:
                self.image.save(file_name)  # Save the image using Pillow

    def convert_to_grayscale(self):
        """ Convert the image to grayscale """
        if self.image:
            self.image = self.image.convert("L")  # Convert to grayscale using Pillow
            self.display_image()

    def adjust_brightness(self):
        """ Adjust the brightness of the image """
        if self.image:
            enhancer = ImageEnhance.Brightness(self.image)
            factor, ok = QInputDialog.getDouble(self, "Brightness", "Enter a brightness factor:", 1.0, 0.0, 10.0, 1)
            if ok:
                self.image = enhancer.enhance(factor)
                self.display_image()

    def adjust_contrast(self):
        """ Adjust the contrast of the image """
        if self.image:
            enhancer = ImageEnhance.Contrast(self.image)
            factor, ok = QInputDialog.getDouble(self, "Contrast", "Enter a contrast factor:", 1.0, 0.0, 10.0, 1)
            if ok:
                self.image = enhancer.enhance(factor)
                self.display_image()

    def flip_image(self):
        """ Flip the image horizontally or vertically """
        if self.image:
            flip_option, ok = QInputDialog.getItem(self, "Flip Image", "Choose flip direction:", ["Horizontal", "Vertical"], 0, False)
            if ok:
                if flip_option == "Horizontal":
                    self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
                elif flip_option == "Vertical":
                    self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
                self.display_image()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = ImageEditor()
    editor.show()  # Show the GUI window
    sys.exit(app.exec_())  