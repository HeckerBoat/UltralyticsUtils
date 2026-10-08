from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QPushButton, QLineEdit, QFileDialog, QComboBox, QTextEdit,
                               QMessageBox)
from PySide6.QtCore import Qt
import sys
import os
import subprocess

class SegmentationVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("分割掩码可视化工具")
        self.setGeometry(100, 100, 600, 400)
        
        # 主窗口部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 主布局
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # 数据集路径
        self.dataset_layout = QHBoxLayout()
        self.dataset_label = QLabel("数据集路径:")
        self.dataset_input = QLineEdit()
        self.dataset_input.setPlaceholderText("选择包含images和labels文件夹的目录")
        self.dataset_button = QPushButton("浏览")
        self.dataset_button.clicked.connect(self.browse_dataset)
        
        self.dataset_layout.addWidget(self.dataset_label)
        self.dataset_layout.addWidget(self.dataset_input)
        self.dataset_layout.addWidget(self.dataset_button)
        
        # 类别文件路径
        self.cls_layout = QHBoxLayout()
        self.cls_label = QLabel("类别文件:")
        self.cls_input = QLineEdit()
        self.cls_input.setPlaceholderText("选择classes.txt文件")
        self.cls_button = QPushButton("浏览")
        self.cls_button.clicked.connect(self.browse_cls)
        
        self.cls_layout.addWidget(self.cls_label)
        self.cls_layout.addWidget(self.cls_input)
        self.cls_layout.addWidget(self.cls_button)
        
        # 背景选择
        self.bg_layout = QHBoxLayout()
        self.bg_label = QLabel("背景类型:")
        self.bg_combo = QComboBox()
        self.bg_combo.addItems(["black", "img"])
        
        self.bg_layout.addWidget(self.bg_label)
        self.bg_layout.addWidget(self.bg_combo)
        
        # 运行按钮
        self.run_button = QPushButton("运行")
        self.run_button.clicked.connect(self.run_visualization)
        
        # 输出日志
        self.log_label = QLabel("运行日志:")
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        
        # 添加所有部件到主布局
        self.main_layout.addLayout(self.dataset_layout)
        self.main_layout.addLayout(self.cls_layout)
        self.main_layout.addLayout(self.bg_layout)
        self.main_layout.addWidget(self.run_button)
        self.main_layout.addWidget(self.log_label)
        self.main_layout.addWidget(self.log_text)
    
    def browse_dataset(self):
        directory = QFileDialog.getExistingDirectory(self, "选择数据集目录")
        if directory:
            self.dataset_input.setText(directory)
    
    def browse_cls(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择类别文件", "", "Text Files (*.txt)")
        if file_path:
            self.cls_input.setText(file_path)
    
    def run_visualization(self):
        # 获取参数
        dataset_dir = self.dataset_input.text()
        cls_path = self.cls_input.text()
        bg_choice = self.bg_combo.currentText()
        
        # 验证参数
        if not dataset_dir:
            QMessageBox.warning(self, "警告", "请选择数据集路径")
            return
        
        if not cls_path:
            QMessageBox.warning(self, "警告", "请选择类别文件")
            return
        
        if not os.path.exists(dataset_dir):
            QMessageBox.warning(self, "警告", "数据集路径不存在")
            return
        
        if not os.path.exists(cls_path):
            QMessageBox.warning(self, "警告", "类别文件不存在")
            return
        
        # 构建命令
        command = [
            "python", "backend/plot_seg_visual.py",
            "--img_path", dataset_dir,
            "--cls_path", cls_path,
            "--bg_ground", bg_choice
        ]
        
        # 清空日志
        self.log_text.clear()
        self.log_text.append("开始运行...")
        self.log_text.append(f"命令: {' '.join(command)}")
        
        try:
            # 设置工作目录为项目根目录
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            # 运行命令
            result = subprocess.run(command, capture_output=True, text=True, cwd=project_root)
            
            # 显示输出
            if result.stdout:
                self.log_text.append("\n输出:")
                self.log_text.append(result.stdout)
            
            if result.stderr:
                self.log_text.append("\n错误:")
                self.log_text.append(result.stderr)
            
            if result.returncode == 0:
                self.log_text.append("\n运行成功！")
                QMessageBox.information(self, "成功", "分割掩码可视化完成")
            else:
                self.log_text.append(f"\n运行失败，返回码: {result.returncode}")
                QMessageBox.critical(self, "失败", "运行失败，请查看日志")
        
        except Exception as e:
            self.log_text.append(f"\n异常: {str(e)}")
            QMessageBox.critical(self, "异常", f"运行时发生异常: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SegmentationVisualizer()
    window.show()
    sys.exit(app.exec())
