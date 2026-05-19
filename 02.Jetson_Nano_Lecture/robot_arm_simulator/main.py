#!/usr/bin/env python3
"""
Synthetic Manipulation Motion Generation - Robot Arm Simulator
=============================================================

A desktop application for demonstrating and recording robot arm
manipulation tasks. Generates HDF5 datasets compatible with
Isaac Lab Mimic for synthetic motion trajectory generation.

Controls:
  Keyboard:
    W/S    - Joint 1 (base rotation)
    A/D    - Joint 2
    Q/E    - Joint 3
    Z/X    - Joint 4
    T/G    - Joint 5
    C/V    - Joint 6
    F/H    - Joint 7
    K      - Gripper toggle (open/close)
    M      - Toggle IK Control Mode
    Space  - Start/stop recording
    1/2/3  - Toggle subtask signals (grasp_1, grasp_2, stack_1)
    R      - Reset to home position
    Ctrl+S - Save HDF5

  Mouse (Normal Mode):
    Left drag   - Rotate 3D view
    Scroll wheel - Zoom in/out

  Mouse (IK Control Mode — press M to toggle):
    Left drag   - Move robot end-effector (IK solved automatically)
    Scroll wheel - Adjust Z height of control plane

  IK Control Mode:
    The robot arm's end-effector follows the mouse cursor in 3D space.
    Inverse kinematics solves joint angles in real-time.
    Use the Z slider (or scroll) to change height.
    Record demonstrations by pressing Space while dragging.

Usage:
    python main.py
"""

import sys
import os
import numpy as np

# ──────────────────────────────────────────────
# PyQt5 Application
# ──────────────────────────────────────────────
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from robot_viewer import Robot3DViewer
from main_window import MainWindow
from recorder import DemonstrationRecorder


def main():
    # Enable high-DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("Synthetic Manipulation - Robot Arm Simulator")
    app.setOrganizationName("SMMG")

    # Set app style
    app.setStyle("Fusion")

    # Dark stylesheet
    app.setStyleSheet("""
        QMainWindow, QWidget {
            background-color: #1e1e2e;
            color: #cdd6f4;
        }
        QGroupBox {
            border: 1px solid #45475a;
            border-radius: 4px;
            margin-top: 10px;
            font-weight: bold;
            padding-top: 14px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }
        QSlider::groove:horizontal {
            height: 6px;
            background: #45475a;
            border-radius: 3px;
        }
        QSlider::handle:horizontal {
            background: #89b4fa;
            width: 14px;
            height: 14px;
            margin: -4px 0;
            border-radius: 7px;
        }
        QSlider::sub-page:horizontal {
            background: #89b4fa;
            border-radius: 3px;
        }
        QPushButton {
            background-color: #45475a;
            border: none;
            border-radius: 4px;
            padding: 6px 12px;
            color: #cdd6f4;
        }
        QPushButton:hover {
            background-color: #585b70;
        }
        QPushButton:checked {
            background-color: #f38ba8;
        }
        QTextEdit {
            background-color: #181825;
            border: 1px solid #45475a;
            border-radius: 4px;
            color: #a6adc8;
        }
        QStatusBar {
            background-color: #181825;
            color: #a6adc8;
        }
        QLabel {
            color: #cdd6f4;
        }
        QCheckBox {
            spacing: 8px;
        }
    """)

    # Initialize components
    viewer = Robot3DViewer()
    recorder = DemonstrationRecorder()
    window = MainWindow(viewer, recorder)

    # Update viewer with initial state
    viewer.update_robot(window.joint_angles, window.gripper_width)
    viewer.update_cubes(window.cube_positions, window.cube_orientations,
                        window.cube_attached)

    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
