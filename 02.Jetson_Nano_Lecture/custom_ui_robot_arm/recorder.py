"""
Data recorder: frame buffer, velocity estimation, HDF5 hierarchical writer.

Output format matches Isaac Lab Mimic / robomimic convention:

/data/
  attrs: total=N
  demo_0/
    attrs: num_samples=T, success=True
    actions                     (T, 8)
    obs/joint_pos               (T, 9)
    obs/joint_vel               (T, 9)
    obs/eef_pos                 (T, 3)
    obs/eef_quat                (T, 4)
    obs/cube_positions          (T, 9)
    obs/cube_orientations       (T, 12)
    obs/datagen_info/eef_pose          (T, 4, 4)
    obs/datagen_info/object_pose       (T, 4, 4)
    obs/datagen_info/target_eef_pose   (T, 4, 4)
    obs/datagen_info/subtask_term_signals/grasp_1  (T,)
    obs/datagen_info/subtask_term_signals/grasp_2  (T,)
    obs/datagen_info/subtask_term_signals/stack_1  (T,)
    states/articulation/robot/joint_position  (T, 9)
    initial_state/articulation/robot/joint_position  (1, 9)
"""

import os
import numpy as np
import h5py
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Optional

from config import (
    NUM_JOINTS, NUM_CUBES, SUBTASK_NAMES,
    ACTION_DIM, DEFAULT_FPS,
)


@dataclass
class Frame:
    """Single recorded frame."""
    joint_pos: np.ndarray          # (7,)
    gripper: float                 # current gripper width
    eef_pos: np.ndarray            # (3,)
    eef_quat: np.ndarray           # (4,)  (x, y, z, w)
    eef_pose: np.ndarray           # (4,4)
    cube_positions: np.ndarray     # (NUM_CUBES, 3)
    cube_orientations: np.ndarray  # (NUM_CUBES, 4)
    subtask_signals: np.ndarray    # (3,)  bool: [grasp_1, grasp_2, stack_1]
    timestamp: float               # seconds since episode start


@dataclass
class Episode:
    """Single demonstration episode."""
    frames: List[Frame] = field(default_factory=list)
    num_samples: int = 0

    def add_frame(self, frame: Frame):
        self.frames.append(frame)
        self.num_samples += 1


class Recorder:
    """Manages recording state, frame buffer, and HDF5 export."""

    def __init__(self):
        self.recording = False
        self.current_episode: Optional[Episode] = None
        self.episodes: List[Episode] = []
        self._start_time: float = 0.0
        self._prev_joint_pos: Optional[np.ndarray] = None

        # subtask state
        self.subtask_signals = np.zeros(len(SUBTASK_NAMES), dtype=bool)

    # ── Control ─────────────────────────────────

    def start_recording(self) -> bool:
        """Begin a new episode.  Returns False if already recording."""
        if self.recording:
            return False
        self.recording = True
        self.current_episode = Episode()
        self._start_time = 0.0
        self._prev_joint_pos = None
        return True

    def stop_recording(self) -> Optional[Episode]:
        """Finish current episode and store it."""
        if not self.recording or self.current_episode is None:
            return None
        ep = self.current_episode
        if len(ep.frames) < 5:
            # Too short – discard
            self.recording = False
            self.current_episode = None
            return None
        self.episodes.append(ep)
        self.recording = False
        self.current_episode = None
        return ep

    def cancel_recording(self):
        """Discard current episode without saving."""
        self.recording = False
        self.current_episode = None
        self._prev_joint_pos = None

    def set_subtask(self, idx: int, active: bool):
        """Set subtask signal (e.g. grasp_1, stack_1)."""
        if 0 <= idx < len(SUBTASK_NAMES):
            self.subtask_signals[idx] = active

    def clear_subtasks(self):
        self.subtask_signals[:] = False

    # ── Recording ───────────────────────────────

    def record_frame(self, joint_pos, gripper, eef_pos, eef_quat,
                     eef_pose, cube_positions, cube_orientations,
                     dt: float):
        """Record a single frame.  Call every timestep when recording."""
        if not self.recording or self.current_episode is None:
            return

        frame = Frame(
            joint_pos=np.asarray(joint_pos, dtype=np.float64).copy(),
            gripper=float(gripper),
            eef_pos=np.asarray(eef_pos, dtype=np.float64).copy(),
            eef_quat=np.asarray(eef_quat, dtype=np.float64).copy(),
            eef_pose=np.asarray(eef_pose, dtype=np.float64).copy(),
            cube_positions=np.asarray(cube_positions, dtype=np.float64).copy(),
            cube_orientations=np.asarray(cube_orientations, dtype=np.float64).copy(),
            subtask_signals=self.subtask_signals.copy(),
            timestamp=self._start_time + len(self.current_episode.frames) * dt,
        )
        self.current_episode.add_frame(frame)
        self._prev_joint_pos = frame.joint_pos.copy()

    # ── Export ──────────────────────────────────

    def save(self, filepath: str, dataset_name: str = "data") -> int:
        """
        Write all recorded episodes to HDF5.

        Parameters
        ----------
        filepath : str  e.g.  "C:\\Users\\user\\Desktop\\output.hdf5"
        dataset_name : str  top-level group name (default "data")

        Returns
        -------
        total_episodes : int  number of episodes saved
        """
        total = len(self.episodes)
        if total == 0:
            return 0

        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)

        with h5py.File(filepath, "w") as f:
            grp = f.create_group(dataset_name)
            grp.attrs["total"] = total

            for ep_idx, ep in enumerate(self.episodes):
                demo = grp.create_group(f"demo_{ep_idx}")
                self._write_episode(demo, ep)

        return total

    def save_single(self, filepath: str, episode: Episode,
                    dataset_name: str = "data") -> bool:
        """Save a single episode to HDF5."""
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        with h5py.File(filepath, "w") as f:
            grp = f.create_group(dataset_name)
            grp.attrs["total"] = 1
            demo = grp.create_group("demo_0")
            self._write_episode(demo, episode)
        return True

    # ── Internal ────────────────────────────────

    def _write_episode(self, demo: h5py.Group, ep: Episode):
        """Write a single episode group."""
        T = ep.num_samples
        demo.attrs["num_samples"] = T
        demo.attrs["success"] = True

        # --- Build arrays ---
        joint_pos_arr  = np.zeros((T, 9), dtype=np.float64)   # 7 + 2 dummy (gripper)
        joint_vel_arr  = np.zeros((T, 9), dtype=np.float64)
        eef_pos_arr    = np.zeros((T, 3), dtype=np.float64)
        eef_quat_arr   = np.zeros((T, 4), dtype=np.float64)
        eef_pose_arr   = np.zeros((T, 4, 4), dtype=np.float64)
        cube_pos_arr   = np.zeros((T, NUM_CUBES * 3), dtype=np.float64)
        cube_ori_arr   = np.zeros((T, NUM_CUBES * 4), dtype=np.float64)
        actions_arr    = np.zeros((T, ACTION_DIM), dtype=np.float64)
        subtask_arrs   = {name: np.zeros(T, dtype=bool)
                          for name in SUBTASK_NAMES}

        prev_jp = None
        for t, frame in enumerate(ep.frames):
            # joint positions  (pad to 9 with gripper at indices 7, 8)
            jp = frame.joint_pos   # (7,)
            joint_pos_arr[t, :7] = jp
            joint_pos_arr[t, 7] = frame.gripper
            joint_pos_arr[t, 8] = 0.0  # dummy

            # joint velocities (finite-difference)
            if prev_jp is not None and t > 0:
                dt_sec = frame.timestamp - ep.frames[t - 1].timestamp
                if dt_sec > 0:
                    vel = (jp - prev_jp) / dt_sec
                    joint_vel_arr[t, :7] = vel
                    joint_vel_arr[t, 7] = 0.0  # gripper vel
                    joint_vel_arr[t, 8] = 0.0  # dummy
            prev_jp = jp.copy()

            # actions = [Δq₁..₇, gripper_cmd]
            if prev_jp is not None and t > 0:
                delta = jp - ep.frames[t - 1].joint_pos
                actions_arr[t, :7] = delta
                actions_arr[t, 7] = frame.gripper - ep.frames[t - 1].gripper
            else:
                actions_arr[t, :] = 0.0

            # EEF
            eef_pos_arr[t] = frame.eef_pos
            eef_quat_arr[t] = frame.eef_quat
            eef_pose_arr[t] = frame.eef_pose

            # Cubes
            for ci in range(NUM_CUBES):
                idx3 = ci * 3
                idx4 = ci * 4
                cube_pos_arr[t, idx3:idx3 + 3] = frame.cube_positions[ci]
                cube_ori_arr[t, idx4:idx4 + 4] = frame.cube_orientations[ci]

            # Subtask signals
            for si, name in enumerate(SUBTASK_NAMES):
                subtask_arrs[name][t] = frame.subtask_signals[si]

        # --- Write datasets ---
        demo.create_dataset("actions", data=actions_arr,
                            compression="gzip", compression_opts=4)

        obs = demo.create_group("obs")
        obs.create_dataset("joint_pos", data=joint_pos_arr,
                           compression="gzip", compression_opts=4)
        obs.create_dataset("joint_vel", data=joint_vel_arr,
                           compression="gzip", compression_opts=4)
        obs.create_dataset("eef_pos", data=eef_pos_arr,
                           compression="gzip", compression_opts=4)
        obs.create_dataset("eef_quat", data=eef_quat_arr,
                           compression="gzip", compression_opts=4)
        obs.create_dataset("cube_positions", data=cube_pos_arr,
                           compression="gzip", compression_opts=4)
        obs.create_dataset("cube_orientations", data=cube_ori_arr,
                           compression="gzip", compression_opts=4)

        # datagen_info
        dgi = obs.create_group("datagen_info")
        dgi.create_dataset("eef_pose", data=eef_pose_arr,
                           compression="gzip", compression_opts=4)
        # object_pose = first cube (index 0) 4×4
        obj_pose = np.tile(np.eye(4), (T, 1, 1))
        for t in range(T):
            idx3 = 0 * 3
            obj_pose[t, :3, 3] = cube_pos_arr[t, idx3:idx3 + 3]
        dgi.create_dataset("object_pose", data=obj_pose,
                           compression="gzip", compression_opts=4)
        # target_eef_pose = last frame eef (goal)
        target_pose = np.tile(eef_pose_arr[-1], (T, 1, 1))
        dgi.create_dataset("target_eef_pose", data=target_pose,
                           compression="gzip", compression_opts=4)

        # subtask_term_signals
        sts = dgi.create_group("subtask_term_signals")
        for name in SUBTASK_NAMES:
            sts.create_dataset(name, data=subtask_arrs[name],
                               compression="gzip", compression_opts=4)

        # states
        states = demo.create_group("states")
        art = states.create_group("articulation")
        rob = art.create_group("robot")
        rob.create_dataset("joint_position", data=joint_pos_arr,
                           compression="gzip", compression_opts=4)

        # initial_state
        init = demo.create_group("initial_state")
        init_art = init.create_group("articulation")
        init_rob = init_art.create_group("robot")
        init_rob.create_dataset("joint_position",
                                data=joint_pos_arr[0:1],
                                compression="gzip", compression_opts=4)

    # ── Statistics ──────────────────────────────

    @property
    def total_frames(self) -> int:
        return sum(ep.num_samples for ep in self.episodes)

    @property
    def num_episodes(self) -> int:
        return len(self.episodes)

    def reset(self):
        """Clear all recorded episodes."""
        self.episodes.clear()
        self.current_episode = None
        self.recording = False
        self._prev_joint_pos = None
        self.clear_subtasks()
