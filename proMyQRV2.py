import os
import sys
import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QTextEdit, QComboBox, QRadioButton, QFileDialog, QLabel, QMessageBox
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from MyQR import myqr
import re

class QRCodeBatchGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        layout = QVBoxLayout()
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        # 创建输入组件
        self.links_input = QTextEdit()  # 使用QTextEdit代替QLineEdit
        self.links_input.setFixedSize(400, 100)  # 设置固定大小
        self.links_input.setPlaceholderText("请输入链接，用'@'分隔")

        self.level_box = QComboBox()
        self.level_box.addItems(['L', 'M', 'Q', 'H'])
        self.level_box.setCurrentIndex(1)

        # 样式按钮
        style_sheet = """
        QPushButton {
            background-color: #007BFF;
            color: white;
            padding: 10px 20px;
            font-size: 14px;
            border: none;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #0056b3;
        }
        """

        self.color_radio = QRadioButton("彩色二维码")
        self.color_radio.setChecked(True)

        self.select_button = QPushButton("选择背景图")
        self.select_button.setStyleSheet(style_sheet)
        self.select_button.clicked.connect(self.openFileNameDialog)
        self.selected_file_label = QLabel()
        self.selected_file_label.setAlignment(Qt.AlignCenter)

        self.generate_button = QPushButton("生成二维码")
        self.generate_button.setStyleSheet(style_sheet)
        self.generate_button.clicked.connect(self.batch_myqr_run)

        # 将组件添加到布局中
        layout.addWidget(QLabel("链接:"))
        layout.addWidget(self.links_input)
        layout.addWidget(QLabel("纠错级别:"))
        layout.addWidget(self.level_box)
        layout.addWidget(self.color_radio)
        layout.addWidget(self.select_button)
        layout.addWidget(self.selected_file_label)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.image_label)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setWindowTitle('批量二维码生成器')

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "选择背景图",
            "",
            "图片 (*.png *.jpeg *.jpg *.gif);;所有文件 (*)",
            options=options
        )
        if fileName:
            self.selected_file_label.setText(fileName)

    def batch_myqr_run(self):
        links_str = self.links_input.toPlainText()
        links = links_str.split('@')
        save_dir, _ = os.path.split(self.selected_file_label.text() or '')
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        last_image_path = None

        # 验证输入
        valid_links = []
        for link in links:
            if not link.strip():
                continue
            if self.validate_input(link):
                valid_links.append(link.strip())
            else:
                # 弹出提示，提示用户输入有误
                self.show_input_error()
                return

        for idx, link in enumerate(valid_links):
            if self.selected_file_label.text().endswith('.gif'):
                save_name = os.path.join(save_dir, f'{timestamp}_{idx}.gif')
            else:
                save_name = os.path.join(save_dir, f'{timestamp}_{idx}.png')

            try:
                myqr.run(
                    words=link,
                    version=10,
                    level=self.level_box.currentText(),
                    picture=self.selected_file_label.text() or False,
                    colorized=self.color_radio.isChecked(),
                    contrast=1.0,
                    brightness=1.2,
                    save_name=save_name
                )
                last_image_path = save_name
                print(f"二维码已保存至 {save_name}")
            except Exception as e:
                print(f"生成二维码失败 {link}: {e}")

        if last_image_path and os.path.exists(last_image_path):
            pixmap = QPixmap(last_image_path)
            self.image_label.setPixmap(pixmap.scaledToWidth(400))
            self.image_label.adjustSize()

    def validate_input(self, link):
        # 检查是否为有效的URL
        url_pattern = re.compile(r'^(https?:\/\/)?(([\da-z\.-]+)\.([a-z]{2,6})(:[0-9]{1,5})?)(\/[^ ]*)?$')
        return url_pattern.match(link.strip()) is not None

    def show_input_error(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("输入有误，请只输入英文或链接!")
        msg_box.setWindowTitle("输入错误")
        msg_box.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QRCodeBatchGenerator()
    ex.show()
    sys.exit(app.exec())