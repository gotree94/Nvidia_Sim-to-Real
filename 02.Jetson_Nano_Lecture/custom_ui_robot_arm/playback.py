"""
HDF5 episode playback dialog.

Loads a recorded HDF5 file and replays episodes frame-by-frame:
- Timeline slider for scrubbing
- Play / Pause / Step Forward / Step Backward
- Speed slider
- Displays current episode / frame info
"""

import os
import numpy as np
import h5py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QSlider, QPushButton, QFileDialog, QGroupBox,
    QMessageBox, QWidget,
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from config import NUM_JOINTS, GRIPPER_DEFAULT


class PlaybackDialog(QDialog):
    """Dialog for loading and replaying HDF5 demonstration episodes."""

    def __init__(self, viewer, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Episode Playback")
        self.setMinimumSize(600, 300)

        self.viewer = viewer  # RobotViewer instance
        self._data = {}       # episode_id -> {joints, ...}
        self._episode_keys = []
        self._current_ep = 0
        self._current_frame = 0
        self._playing = False
        self._total_episodes = 0

        self._build_ui()
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._advance_frame)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)

        font = QFont("Consolas", 10)
        bf = QFont("Segoe UI", 11, QFont.Bold)

        # ── File controls ───────────────────────
        file_row = QHBoxLayout()
        self.file_label = QLabel("No file loaded")
        self.file_label.setFont(font)
        self.load_btn = QPushButton("Load HDF5")
        self.load_btn.clicked.connect(self._load_file)
        file_row.addWidget(self.file_label, 1)
        file_row.addWidget(self.load_btn)
        layout.addLayout(file_row)

        # ── Episode / Frame info ────────────────
        info_group = QGroupBox("Info")
        info_group.setFont(bf)
        info_layout = QVBoxLayout(info_group)

        self.ep_label = QLabel("Episode: -- / --")
        self.ep_label.setFont(font)
        self.frame_label = QLabel("Frame: -- / --")
        self.frame_label.setFont(font)
        info_layout.addWidget(self.ep_label)
        info_layout.addWidget(self.frame_label)
        layout.addWidget(info_group)

        # ── Timeline slider ─────────────────────
        timeline_group = QGroupBox("Timeline")
        timeline_group.setFont(bf)
        tl_layout = QVBoxLayout(timeline_group)

        self.timeline = QSlider(Qt.Horizontal)
        self.timeline.setRange(0, 0)
        self.timeline.setTickPosition(QSlider.TicksBelow)
        self.timeline.setTickInterval(10)
        self.timeline.valueChanged.connect(self._on_seek)

        self.timeline_time = QLabel("0:00 / 0:00")
        self.timeline_time.setFont(font)
        self.timeline_time.setAlignment(Qt.AlignCenter)

        tl_layout.addWidget(self.timeline)
        tl_layout.addWidget(self.timeline_time)
        layout.addWidget(timeline_group)

        # ── Playback speed ──────────────────────
        speed_row = QHBoxLayout()
        speed_row.addWidget(QLabel("Speed:"))
        self.play_speed = QSlider(Qt.Horizontal)
        self.play_speed.setRange(1, 30)  # 0.1x .. 3.0x
        self.play_speed.setValue(10)
        self.play_speed.setTickPosition(QSlider.TicksBelow)
        self.play_speed.setTickInterval(5)
        self.speed_label = QLabel("1.0x")
        self.speed_label.setFont(QFont("Consolas", 10, QFont.Bold))
        self.speed_label.setFixedWidth(40)
        self.speed_label.setAlignment(Qt.AlignCenter)
        self.play_speed.valueChanged.connect(
            lambda v: self.speed_label.setText(f"{v/10:.1f}x"))
        speed_row.addWidget(self.play_speed)
        speed_row.addWidget(self.speed_label)
        layout.addLayout(speed_row)

        # ── Transport controls ──────────────────
        btn_row = QHBoxLayout()

        self.prev_ep_btn = QPushButton("\u23ee Episode")
        self.prev_ep_btn.clicked.connect(self._prev_episode)

        self.step_bwd_btn = QPushButton("\u23f4 Step \u2190")
        self.step_bwd_btn.clicked.connect(self._step_backward)

        self.play_btn = QPushButton("\u25b6 Play")
        self.play_btn.setStyleSheet(
            "QPushButton { background: #0e639c; color: white; "
            "font-weight: bold; padding: 6px 16px; border-radius: 3px; }"
            "QPushButton:hover { background: #1177bb; }")
        self.play_btn.clicked.connect(self._toggle_play)

        self.step_fwd_btn = QPushButton("Step \u2192 \u23f5")
        self.step_fwd_btn.clicked.connect(self._step_forward)

        self.next_ep_btn = QPushButton("Episode \u23ed")
        self.next_ep_btn.clicked.connect(self._next_episode)

        btn_row.addWidget(self.prev_ep_btn)
        btn_row.addWidget(self.step_bwd_btn)
        btn_row.addWidget(self.play_btn)
        btn_row.addWidget(self.step_fwd_btn)
        btn_row.addWidget(self.next_ep_btn)
        layout.addLayout(btn_row)

        # ── Ep navigation ───────────────────────
        nav_row = QHBoxLayout()
        self.ep_slider = QSlider(Qt.Horizontal)
        self.ep_slider.setRange(0, 0)
        self.ep_slider.setTickPosition(QSlider.TicksBelow)
        self.ep_slider.valueChanged.connect(self._on_episode_seek)

        nav_row.addWidget(QLabel("Episode:"))
        nav_row.addWidget(self.ep_slider)
        layout.addLayout(nav_row)

        # ── Joint values display ────────────────
        joint_row = QHBoxLayout()
        self.joint_display = QLabel("")
        self.joint_display.setFont(QFont("Consolas", 8))
        joint_row.addWidget(self.joint_display)
        layout.addLayout(joint_row)

        # ── Close button ────────────────────────
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self._safe_close)
        layout.addWidget(self.close_btn)

        # dark styling
        self.setStyleSheet("""
            QDialog { background: #1e1e1e; color: #d4d4d4; }
            QGroupBox {
                background: #252526; border: 1px solid #3c3c3c;
                border-radius: 4px; margin-top: 10px; padding-top: 14px;
                font-weight: bold; color: #ccc;
            }
            QGroupBox::title {
                subcontrol-origin: margin; left: 8px; padding: 0 4px;
            }
            QLabel { color: #d4d4d4; }
            QSlider::groove:horizontal {
                height: 6px; background: #3c3c3c; border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #007acc; width: 14px; height: 14px;
                margin: -4px 0; border-radius: 7px;
            }
            QSlider::sub-page:horizontal {
                background: #0e639c; border-radius: 3px;
            }
            QPushButton {
                background: #0e639c; color: white; border: none;
                padding: 5px 10px; border-radius: 3px; font-weight: bold;
            }
            QPushButton:hover { background: #1177bb; }
            QPushButton:pressed { background: #094771; }
        """)

    # ── File loading ────────────────────────────

    def _load_file(self):
        fp, _ = QFileDialog.getOpenFileName(
            self, "Load HDF5", os.path.expanduser("~"),
            "HDF5 Files (*.hdf5 *.h5);;All Files (*)")
        if not fp:
            return
        try:
            self._parse_hdf5(fp)
            self.file_label.setText(os.path.basename(fp))
            self._show_episode(0)
        except Exception as e:
            QMessageBox.critical(self, "Load Error", str(e))

    def _parse_hdf5(self, path):
        """Load all episodes from an HDF5 file into memory."""
        self._data.clear()
        with h5py.File(path, "r") as f:
            grp = f.get("data", f)
            keys = sorted([k for k in grp.keys() if k.startswith("demo_")],
                          key=lambda x: int(x.split("_")[1]))
            self._episode_keys = keys
            self._total_episodes = len(keys)

            for ep_key in keys:
                demo = grp[ep_key]
                # load joint positions
                jp = demo["states/articulation/robot/joint_position"][()]
                # shape (T, 9) -> (T, 7)  (slice off gripper/dummy dims)
                joints = np.asarray(jp[:, :7], dtype=np.float64)
                self._data[ep_key] = {"joints": joints}

        self.ep_slider.setRange(0, max(0, self._total_episodes - 1))
        self.ep_slider.setValue(0)
        self._current_ep = 0

    # ── Episode navigation ─────────────────────

    def _show_episode(self, idx):
        if not self._episode_keys:
            return
        idx = max(0, min(idx, self._total_episodes - 1))
        self._current_ep = idx
        ep_key = self._episode_keys[idx]
        joints = self._data[ep_key]["joints"]
        T = joints.shape[0]

        self.timeline.setRange(0, max(0, T - 1))
        self.timeline.setValue(0)
        self._current_frame = 0
        self.ep_slider.blockSignals(True)
        self.ep_slider.setValue(idx)
        self.ep_slider.blockSignals(False)

        self.ep_label.setText(
            f"Episode: {idx + 1} / {self._total_episodes}")
        self._update_display()

    def _on_episode_seek(self, idx):
        self._stop_play()
        self._show_episode(idx)

    def _prev_episode(self):
        self._stop_play()
        self._show_episode(self._current_ep - 1)

    def _next_episode(self):
        self._stop_play()
        self._show_episode(self._current_ep + 1)

    # ── Frame navigation ───────────────────────

    def _on_seek(self, frame):
        self._current_frame = frame
        self._update_display()

    def _step_forward(self):
        if not self._episode_keys:
            return
        ep_key = self._episode_keys[self._current_ep]
        max_f = self._data[ep_key]["joints"].shape[0] - 1
        self._current_frame = min(self._current_frame + 1, max_f)
        self.timeline.setValue(self._current_frame)
        self._update_display()

    def _step_backward(self):
        if not self._episode_keys:
            return
        self._current_frame = max(self._current_frame - 1, 0)
        self.timeline.setValue(self._current_frame)
        self._update_display()

    # ── Play/Pause ─────────────────────────────

    def _toggle_play(self):
        if not self._episode_keys:
            return
        if self._playing:
            self._stop_play()
        else:
            self._start_play()

    def _start_play(self):
        self._playing = True
        self.play_btn.setText("\u23f8 Pause")
        self.play_btn.setStyleSheet(
            "QPushButton { background: #5a1a1a; color: #ff6666; "
            "font-weight: bold; padding: 6px 16px; border-radius: 3px; }")
        # Timer interval based on speed: speed=10 -> 1.0x -> 30fps
        speed = self.play_speed.value() / 10.0
        interval = max(16, int(1000.0 / (30.0 * speed)))
        self._timer.start(interval)

    def _stop_play(self):
        self._playing = False
        self._timer.stop()
        self.play_btn.setText("\u25b6 Play")
        self.play_btn.setStyleSheet(
            "QPushButton { background: #0e639c; color: white; "
            "font-weight: bold; padding: 6px 16px; border-radius: 3px;"
            "} QPushButton:hover { background: #1177bb; }")

    def _advance_frame(self):
        """Called by timer during playback."""
        if not self._episode_keys:
            self._stop_play()
            return
        ep_key = self._episode_keys[self._current_ep]
        max_f = self._data[ep_key]["joints"].shape[0] - 1

        if self._current_frame >= max_f:
            # Auto-advance to next episode
            if self._current_ep < self._total_episodes - 1:
                self._show_episode(self._current_ep + 1)
            else:
                self._stop_play()
            return

        self._current_frame += 1
        self.timeline.setValue(self._current_frame)
        self._update_display()

    # ── Display update ─────────────────────────

    def _update_display(self):
        if not self._episode_keys:
            return
        ep_key = self._episode_keys[self._current_ep]
        joints = self._data[ep_key]["joints"]
        T = joints.shape[0]
        f = min(self._current_frame, T - 1)

        self.frame_label.setText(
            f"Frame: {f + 1} / {T}")
        self.timeline_time.setText(
            f"{f // 30}:{f % 30:02d} / {T // 30}:{T % 30:02d}")

        # Update viewer
        q = joints[f]
        self.viewer.set_joint_angles(q)
        self.viewer.set_gripper(GRIPPER_DEFAULT)
        self.viewer.update()

        # Display joint values
        vals = "  ".join(f"J{i+1}={q[i]:+.3f}" for i in range(NUM_JOINTS))
        self.joint_display.setText(vals)

    # ── Cleanup ────────────────────────────────

    def _safe_close(self):
        self._stop_play()
        self.accept()

    def closeEvent(self, event):
        self._stop_play()
        super().closeEvent(event)
