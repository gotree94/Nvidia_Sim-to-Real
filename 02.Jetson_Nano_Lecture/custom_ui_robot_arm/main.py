"""
Entry point for the Custom UI Robot Arm Simulator.

Usage:
    pip install -r requirements.txt
    python main.py
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel,
    QRadioButton, QButtonGroup, QDialogButtonBox,
)
from PyQt5.QtGui import QFont, QPalette, QColor
from app import MainWindow
from config import PRESET_POSITIONS, PRESET_NAMES


class PoseSelectionDialog(QDialog):
    """Startup dialog to choose initial robot pose."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Initial Pose")
        self.setFixedSize(380, 220)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        title = QLabel("로봇 초기 자세를 선택하세요")
        title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        layout.addWidget(title)

        desc = QLabel(
            "시뮬레이션 시작 시 로봇팔의 초기 자세를 선택합니다.\n"
            "실행 후 Backspace 키로 언제든지 재설정할 수 있습니다."
        )
        desc.setFont(QFont("Segoe UI", 9))
        desc.setStyleSheet("color: #999;")
        layout.addWidget(desc)

        self.button_group = QButtonGroup(self)
        for i, name in enumerate(PRESET_NAMES):
            rb = QRadioButton(name)
            rb.setFont(QFont("Consolas", 10))
            if i == 0:
                rb.setChecked(True)
            self.button_group.addButton(rb, i)
            layout.addWidget(rb)

        layout.addStretch()

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        # Dark styling
        self.setStyleSheet("""
            QDialog { background-color: #1e1e1e; color: #d4d4d4; }
            QLabel { color: #d4d4d4; }
            QRadioButton { color: #d4d4d4; spacing: 6px; }
            QRadioButton::indicator {
                width: 14px; height: 14px;
            }
        """)

    def selected_pose(self):
        idx = self.button_group.checkedId()
        name = PRESET_NAMES[idx]
        return name, PRESET_POSITIONS[name].copy()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Custom UI Robot Arm Simulator")
    app.setFont(QFont("Segoe UI", 9))

    # Dark palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(30, 30, 30))
    palette.setColor(QPalette.WindowText, QColor(212, 212, 212))
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(37, 37, 37))
    palette.setColor(QPalette.ToolTipBase, QColor(37, 37, 37))
    palette.setColor(QPalette.ToolTipText, QColor(212, 212, 212))
    palette.setColor(QPalette.Text, QColor(212, 212, 212))
    palette.setColor(QPalette.Button, QColor(37, 37, 37))
    palette.setColor(QPalette.ButtonText, QColor(212, 212, 212))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Highlight, QColor(14, 99, 156))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)

    # Pose selection dialog
    dialog = PoseSelectionDialog()
    if dialog.exec_() != QDialog.Accepted:
        return  # user cancelled → don't start

    pose_name, initial_pose = dialog.selected_pose()
    window = MainWindow(initial_pose=initial_pose, pose_name=pose_name)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
