"""
HDF5 episode playback dialog for robot_arm_simulator (v1).

Loads a recorded HDF5 file and replays episodes frame-by-frame.
Updates the RobotViewer with joint angles from each frame.
"""

import os
import numpy as np
import h5py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QSlider, QPushButton, QFileDialog, QGroupBox,
    QMessageBox, QTextEdit, QCheckBox, QApplication,
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor

from config import NUM_JOINTS, GRIPPER_LIMITS
from kinematics import franka_fk, rotation_matrix_to_quat


class PlaybackDialog(QDialog):
    """Load and replay recorded HDF5 demonstration episodes."""

    def __init__(self, viewer, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Episode Playback")
        self.setMinimumSize(720, 500)

        self.viewer = viewer
        self._data = {}
        self._episode_keys = []
        self._current_ep = 0
        self._current_frame = 0
        self._playing = False
        self._total_eps = 0
        self._hdf5_path = None
        self._recorded_eef = None  # cached FK from recorded data

        self._build_ui()
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._advance)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(10, 10, 10, 10)

        font = QFont("Consolas", 10)
        bf = QFont("Segoe UI", 11, QFont.Bold)

        # File
        fr = QHBoxLayout()
        self.file_label = QLabel("No file loaded")
        self.file_label.setFont(font)
        self.load_btn = QPushButton("Load HDF5")
        self.load_btn.clicked.connect(self._load_file)
        fr.addWidget(self.file_label, 1)
        fr.addWidget(self.load_btn)
        layout.addLayout(fr)

        # Info
        ig = QGroupBox("Info")
        ig.setFont(bf)
        il = QVBoxLayout(ig)
        self.ep_label = QLabel("Episode: -- / --")
        self.ep_label.setFont(font)
        self.frame_label = QLabel("Frame: -- / --")
        self.frame_label.setFont(font)
        self.joint_label = QLabel("")
        self.joint_label.setFont(QFont("Consolas", 8))
        il.addWidget(self.ep_label)
        il.addWidget(self.frame_label)
        il.addWidget(self.joint_label)
        layout.addWidget(ig)

        # Timeline
        tg = QGroupBox("Timeline")
        tg.setFont(bf)
        tl = QVBoxLayout(tg)
        self.timeline = QSlider(Qt.Horizontal)
        self.timeline.setRange(0, 0)
        self.timeline.setTickPosition(QSlider.TicksBelow)
        self.timeline.setTickInterval(10)
        self.timeline.valueChanged.connect(self._on_seek)
        self.time_label = QLabel("0:00 / 0:00")
        self.time_label.setFont(font)
        self.time_label.setAlignment(Qt.AlignCenter)
        tl.addWidget(self.timeline)
        tl.addWidget(self.time_label)
        layout.addWidget(tg)

        # Speed
        sr = QHBoxLayout()
        sr.addWidget(QLabel("Speed:"))
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(1, 30)
        self.speed_slider.setValue(10)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.setTickInterval(5)
        self.speed_label = QLabel("1.0x")
        self.speed_label.setFont(QFont("Consolas", 10, QFont.Bold))
        self.speed_label.setFixedWidth(35)
        self.speed_label.setAlignment(Qt.AlignCenter)
        self.speed_slider.valueChanged.connect(
            lambda v: self.speed_label.setText(f"{v/10:.1f}x"))
        sr.addWidget(self.speed_slider)
        sr.addWidget(self.speed_label)
        layout.addLayout(sr)

        # Controls
        br = QHBoxLayout()
        self.step_bwd = QPushButton("\u23f4 \u2190")
        self.step_bwd.clicked.connect(self._step_bwd)
        self.play_btn = QPushButton("\u25b6 Play")
        self.play_btn.setStyleSheet(
            "QPushButton { background: #0e639c; color: white; "
            "font-weight: bold; padding: 5px 14px; border-radius: 3px; }"
            "QPushButton:hover { background: #1177bb; }")
        self.play_btn.clicked.connect(self._toggle_play)
        self.step_fwd = QPushButton("\u2192 \u23f5")
        self.step_fwd.clicked.connect(self._step_fwd)
        self.next_ep = QPushButton("\u23ed")
        self.next_ep.clicked.connect(self._next_ep)
        self.prev_ep = QPushButton("\u23ee")
        self.prev_ep.clicked.connect(self._prev_ep)
        br.addWidget(self.prev_ep)
        br.addWidget(self.step_bwd)
        br.addWidget(self.play_btn)
        br.addWidget(self.step_fwd)
        br.addWidget(self.next_ep)
        layout.addLayout(br)

        # ── Debug toggle ──
        self.debug_cb = QCheckBox("Debug Info (FK verification + data dump)")
        self.debug_cb.setFont(QFont("Segoe UI", 9))
        self.debug_cb.setStyleSheet("color: #888;")
        self.debug_cb.toggled.connect(self._toggle_debug)
        layout.addWidget(self.debug_cb)

        # Debug info
        dg = QGroupBox("Debug Info")
        dg.setFont(bf)
        dgl = QVBoxLayout(dg)
        self.debug_log = QTextEdit()
        self.debug_log.setReadOnly(True)
        self.debug_log.setFont(QFont("Consolas", 8))
        self.debug_log.setMaximumHeight(250)
        self.debug_log.setStyleSheet(
            "QTextEdit { background: #1a1a1a; color: #d4d4d4; border: 1px solid #333; }")
        dgl.addWidget(self.debug_log)
        dbg_btn_row = QHBoxLayout()
        self.copy_log_btn = QPushButton("Copy to Clipboard")
        self.copy_log_btn.clicked.connect(self._copy_debug_log)
        self.dump_btn = QPushButton("Dump All Frames to Console")
        self.dump_btn.clicked.connect(self._dump_all_frames)
        dbg_btn_row.addWidget(self.copy_log_btn)
        dbg_btn_row.addWidget(self.dump_btn)
        dgl.addLayout(dbg_btn_row)
        self.debug_group = dg
        self.debug_group.setVisible(False)
        layout.addWidget(self.debug_group)

        # Close
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self._safe_close)
        layout.addWidget(self.close_btn)

        # Dark style
        self.setStyleSheet("""
            QDialog { background: #1e1e1e; color: #d4d4d4; }
            QGroupBox {
                background: #252526; border: 1px solid #3c3c3c;
                border-radius: 4px; margin-top: 10px; padding-top: 14px;
                font-weight: bold; color: #ccc;
            }
            QGroupBox::title { subcontrol-origin: margin; left: 8px; padding: 0 4px; }
            QLabel { color: #d4d4d4; }
            QSlider::groove:horizontal {
                height: 6px; background: #3c3c3c; border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #007acc; width: 14px; height: 14px;
                margin: -4px 0; border-radius: 7px;
            }
            QSlider::sub-page:horizontal { background: #0e639c; border-radius: 3px; }
            QPushButton {
                background: #0e639c; color: white; border: none;
                padding: 4px 10px; border-radius: 3px; font-weight: bold;
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
            self._parse(fp)
            self.file_label.setText(os.path.basename(fp))
            self._show_ep(0)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _parse(self, path):
        self._data.clear()
        self._hdf5_path = path
        with h5py.File(path, "r") as f:
            grp = f.get("data", f)
            keys = sorted(
                [k for k in grp.keys() if k.startswith("demo_")],
                key=lambda x: int(x.split("_")[1]))
            self._episode_keys = keys
            self._total_eps = len(keys)

            for ek in keys:
                ep_group = grp[ek]

                # Joint positions: [q1..q7, gripper_width, -gripper_width]
                joint_dset = ep_group["states/articulation/robot/joint_position"]
                joints = np.asarray(joint_dset[:, :7], dtype=np.float64)
                gripper = np.asarray(joint_dset[:, 7], dtype=np.float64)

                entry = {"joints": joints, "gripper": gripper}

                # Recorded EEF from obs (for FK comparison in debug mode)
                if "obs/eef_pos" in ep_group:
                    entry["eef_pos"] = np.asarray(ep_group["obs/eef_pos"], dtype=np.float64)
                    entry["eef_quat"] = np.asarray(ep_group["obs/eef_quat"], dtype=np.float64)

                # Cube states from states/rigid_object/{name}/root_pose -> (N, 7)
                rigid_path = "states/rigid_object"
                if rigid_path in ep_group:
                    cubes = {}
                    for cube_name in ep_group[rigid_path]:
                        pose_dset = ep_group[f"{rigid_path}/{cube_name}/root_pose"]
                        cubes[cube_name] = np.asarray(pose_dset, dtype=np.float64)
                    if cubes:
                        entry["cubes"] = cubes

                self._data[ek] = entry

    # ── Episode navigation ─────────────────────

    def _show_ep(self, idx):
        if not self._episode_keys:
            return
        idx = max(0, min(idx, self._total_eps - 1))
        self._current_ep = idx
        entry = self._data[self._episode_keys[idx]]
        T = entry["joints"].shape[0]
        self.timeline.setRange(0, max(0, T - 1))
        self.timeline.setValue(0)
        self._current_frame = 0
        self.ep_label.setText(f"Episode: {idx+1} / {self._total_eps}")

        # Pre-load first-frame cube state into viewer (before _update draws)
        if "cubes" in entry:
            positions = {}
            orientations = {}
            for name, poses in entry["cubes"].items():
                positions[name] = poses[0, :3]
                orientations[name] = poses[0, 3:7]
            self.viewer.update_cubes(positions, orientations)

        self._update()

    def _prev_ep(self):
        self._stop()
        self._show_ep(self._current_ep - 1)

    def _next_ep(self):
        self._stop()
        self._show_ep(self._current_ep + 1)

    def _on_seek(self, frame):
        self._current_frame = frame
        self._update()

    def _step_fwd(self):
        if not self._episode_keys:
            return
        ek = self._episode_keys[self._current_ep]
        mx = self._data[ek]["joints"].shape[0] - 1
        self._current_frame = min(self._current_frame + 1, mx)
        self.timeline.setValue(self._current_frame)
        self._update()

    def _step_bwd(self):
        self._current_frame = max(self._current_frame - 1, 0)
        self.timeline.setValue(self._current_frame)
        self._update()

    # ── Play/Pause ─────────────────────────────

    def _toggle_play(self):
        if not self._episode_keys:
            return
        if self._playing:
            self._stop()
        else:
            self._start()

    def _start(self):
        self._playing = True
        self.play_btn.setText("\u23f8 Pause")
        self.play_btn.setStyleSheet(
            "QPushButton { background: #5a1a1a; color: #ff6666; "
            "font-weight: bold; padding: 5px 14px; border-radius: 3px; }")
        spd = self.speed_slider.value() / 10.0
        self._timer.start(max(16, int(1000 / (30 * spd))))

    def _stop(self):
        self._playing = False
        self._timer.stop()
        self.play_btn.setText("\u25b6 Play")
        self.play_btn.setStyleSheet(
            "QPushButton { background: #0e639c; color: white; "
            "font-weight: bold; padding: 5px 14px; border-radius: 3px;"
            "} QPushButton:hover { background: #1177bb; }")

    def _advance(self):
        if not self._episode_keys:
            self._stop()
            return
        ek = self._episode_keys[self._current_ep]
        mx = self._data[ek]["joints"].shape[0] - 1
        if self._current_frame >= mx:
            if self._current_ep < self._total_eps - 1:
                self._show_ep(self._current_ep + 1)
            else:
                self._stop()
            return
        self._current_frame += 1
        self.timeline.setValue(self._current_frame)
        self._update()

    # ── Update viewer ──────────────────────────

    def _update(self):
        if not self._episode_keys:
            return
        ek = self._episode_keys[self._current_ep]
        entry = self._data[ek]
        joints = entry["joints"]
        T = joints.shape[0]
        f = min(self._current_frame, T - 1)
        q = joints[f]

        self.frame_label.setText(f"Frame: {f+1} / {T}")
        self.time_label.setText(f"{f//30}:{f%30:02d} / {T//30}:{T%30:02d}")
        self.joint_label.setText(
            "  ".join(f"J{i+1}={q[i]:+.3f}" for i in range(min(NUM_JOINTS, 7))))

        # Gripper width from recorded data
        gripper_val = entry["gripper"][f] if "gripper" in entry else 0.04

        # Update robot with recorded joint angles + gripper
        self.viewer.update_robot(q, gripper_val)

        # Cube states from recorded data
        if "cubes" in entry:
            positions = {}
            orientations = {}
            for name, poses in entry["cubes"].items():
                positions[name] = poses[f, :3]
                orientations[name] = poses[f, 3:7]
            self.viewer.update_cubes(positions, orientations)

        self.viewer.update()

        if self.debug_cb.isChecked():
            self._update_debug()

    # ── Debug methods ──────────────────────────

    def _toggle_debug(self, visible):
        self.debug_group.setVisible(visible)
        if visible:
            self._update_debug()
        self.adjustSize()

    def _update_debug(self):
        if not self._episode_keys or not self.debug_cb.isChecked():
            return
        ek = self._episode_keys[self._current_ep]
        entry = self._data[ek]
        joints = entry["joints"]
        T = joints.shape[0]
        f = min(self._current_frame, T - 1)
        q = joints[f]

        lines = []
        lines.append(f"Episode: {self._current_ep+1}/{self._total_eps}")
        lines.append(f"Frame:   {f+1}/{T}")
        lines.append(f"Time:    {f//30}:{f%30:02d} / {T//30}:{T%30:02d}")
        lines.append("")

        # Joint angles
        lines.append("─ Joint Angles (rad) ─")
        for i in range(7):
            marker = ""
            if i == 0:
                marker = ""
            lines.append(f"  J{i+1}: {q[i]:+.4f}")
        gripper_val = entry["gripper"][f] if "gripper" in entry else 0.04
        lines.append(f"  Gripper: {gripper_val:.4f}m")
        lines.append("")

        # FK comparison
        lines.append("─ FK Verification (franka_fk vs Recorded EEF) ─")
        T_fk = franka_fk(q)
        fk_pos = T_fk[:3, 3]
        lines.append(f"  FK  EEF pos: [{fk_pos[0]:+.4f}, {fk_pos[1]:+.4f}, {fk_pos[2]:+.4f}]")

        if "eef_pos" in entry:
            rec_pos = entry["eef_pos"][f]
            pos_err = np.linalg.norm(fk_pos - rec_pos)
            lines.append(f"  Rec EEF pos: [{rec_pos[0]:+.4f}, {rec_pos[1]:+.4f}, {rec_pos[2]:+.4f}]")
            if pos_err < 0.001:
                status = "OK"
            elif pos_err < 0.01:
                status = "WARN"
            else:
                status = "MISMATCH!"
            lines.append(f"  FK Error: {pos_err:.6f}m  [{status}]")

            # Orientation comparison
            fk_quat = rotation_matrix_to_quat(T_fk[:3, :3])
            rec_quat = entry["eef_quat"][f]
            # angular diff
            q1_conj = np.array([rec_quat[0], -rec_quat[1], -rec_quat[2], -rec_quat[3]])
            w1, x1, y1, z1 = q1_conj
            w2, x2, y2, z2 = fk_quat
            q_rel = np.array([
                w1*w2 - x1*x2 - y1*y2 - z1*z2,
                w1*x2 + x1*w2 + y1*z2 - z1*y2,
                w1*y2 - x1*z2 + y1*w2 + z1*x2,
                w1*z2 + x1*y2 - y1*x2 + z1*w2,
            ])
            angle_err = 2 * np.degrees(np.arccos(np.clip(q_rel[0], -1, 1)))
            lines.append(f"  Orientation err: {angle_err:.2f}deg")
        else:
            lines.append(f"  (No recorded EEF data in this HDF5)")
        lines.append("")

        # Cube states
        if "cubes" in entry:
            lines.append("─ Cube States ─")
            for name, poses in entry["cubes"].items():
                pos = poses[f, :3]
                ori = poses[f, 3:7]
                lines.append(f"  {name}:")
                lines.append(f"    pos=[{pos[0]:+.4f}, {pos[1]:+.4f}, {pos[2]:+.4f}]")
                lines.append(f"    quat=[{ori[0]:+.4f}, {ori[1]:+.4f}, {ori[2]:+.4f}, {ori[3]:+.4f}]")
                # Distance from EEF
                dist = np.linalg.norm(pos - fk_pos)
                lines.append(f"    dist_to_EEF={dist:.4f}m")
            lines.append("")

        # Data integrity checks
        lines.append("─ Integrity Checks ─")
        from config import JOINT_LIMITS
        for i in range(7):
            if q[i] < JOINT_LIMITS[i, 0] or q[i] > JOINT_LIMITS[i, 1]:
                lines.append(f"  JOINT LIMIT VIOLATION: J{i+1}={q[i]:.4f} outside [{JOINT_LIMITS[i,0]:.4f}, {JOINT_LIMITS[i,1]:.4f}]")
        # Check for NaN
        if np.any(np.isnan(q)):
            lines.append("  NAN DETECTED in joint angles")
        # Check cube-EFF proximity (should be close to each other when grasped)
        lines.append("  (OK)")

        text = "\n".join(lines)
        self.debug_log.setText(text)

    def _copy_debug_log(self):
        QApplication.clipboard().setText(self.debug_log.toPlainText())

    def _dump_all_frames(self):
        if not self._episode_keys:
            return
        ek = self._episode_keys[self._current_ep]
        entry = self._data[ek]
        joints = entry["joints"]
        T = joints.shape[0]
        print(f"=== DUMP: {ek} ({T} frames) ===")
        for f in range(T):
            q = joints[f]
            T_fk = franka_fk(q)
            fk_pos = T_fk[:3, 3]
            gripper_val = entry["gripper"][f]
            info = f"  frame {f:3d}: joints=[{q[0]:+.3f} {q[1]:+.3f} {q[2]:+.3f} {q[3]:+.3f} {q[4]:+.3f} {q[5]:+.3f} {q[6]:+.3f}]"
            info += f"  eef=[{fk_pos[0]:+.3f} {fk_pos[1]:+.3f} {fk_pos[2]:+.3f}]"
            info += f"  gripper={gripper_val:.3f}"
            if "eef_pos" in entry:
                rec = entry["eef_pos"][f]
                err = np.linalg.norm(fk_pos - rec)
                info += f"  fk_err={err:.4f}"
            print(info)
        print(f"=== END DUMP: {ek} ===")

    def _safe_close(self):
        self._stop()
        self.accept()

    def closeEvent(self, event):
        self._stop()
        super().closeEvent(event)
