"""
Data recorder for robot arm demonstrations.
Records joint angles, EEF pose, cube states, and subtask signals.
Exports to HDF5 format compatible with Isaac Lab Mimic / robomimic.
"""

import json
import time
import numpy as np
from pathlib import Path
from collections import defaultdict
from kinematics import franka_fk, rotation_matrix_to_quat
from config import SUBTASK_NAMES


class DemonstrationRecorder:
    """
    Records robot arm demonstration data frame by frame.
    
    Usage:
        recorder = DemonstrationRecorder()
        recorder.start_episode()
        while recording:
            recorder.record_frame(joint_angles, gripper_width, cubes, subtask_signals)
        recorder.save_episode("output.hdf5")
    """

    def __init__(self):
        self._episode_data = None
        self._frame_count = 0
        self._is_recording = False
        self._episode_index = 0
        self._prev_joint = None
        self._prev_time = None
        self._timestamp = None

        # Accumulated data across episodes (for multi-episode save)
        self._all_episodes = []

    # ───── Public API ─────

    def start_episode(self):
        """Start a new recording episode."""
        self._episode_data = defaultdict(list)
        self._frame_count = 0
        self._is_recording = True
        self._prev_joint = None
        self._prev_time = time.time()
        self._timestamp = time.time()

        # Subtask signals (default: all False)
        self._current_subtasks = {name: False for name in SUBTASK_NAMES}

    def set_subtask(self, name: str, active: bool):
        """Set subtask signal for current/future frames."""
        if name in self._current_subtasks:
            self._current_subtasks[name] = active

    def toggle_subtask(self, name: str):
        """Toggle subtask signal."""
        if name in self._current_subtasks:
            self._current_subtasks[name] = not self._current_subtasks[name]
        return self._current_subtasks.get(name, False)

    def get_subtask_states(self):
        """Get current subtask states."""
        return dict(self._current_subtasks)

    @property
    def is_recording(self):
        return self._is_recording

    @property
    def frame_count(self):
        return self._frame_count

    def record_frame(self, joint_angles, gripper_width, cube_positions=None,
                     cube_orientations=None, cube_attached=None):
        """
        Record a single frame of demonstration data.
        
        Args:
            joint_angles: (7,) Franka joint angles
            gripper_width: float, gripper opening
            cube_positions: dict of {name: (3,) xyz}
            cube_orientations: dict of {name: (4,) quaternion (w,x,y,z)}
            cube_attached: dict of {name: bool}
        """
        if not self._is_recording:
            return

        now = time.time()
        dt = now - self._prev_time if self._prev_time else 0.016
        self._prev_time = now

        # Compute EEF pose from FK
        T_ee = franka_fk(joint_angles)
        eef_pos = T_ee[:3, 3].copy()
        eef_quat = rotation_matrix_to_quat(T_ee[:3, :3])

        # Compute joint velocity (finite difference)
        if self._prev_joint is not None:
            joint_vel = (joint_angles - self._prev_joint) / max(dt, 0.001)
        else:
            joint_vel = np.zeros_like(joint_angles)

        # Actions: delta joint position + gripper (normalized)
        if self._prev_joint is not None:
            delta_joint = (joint_angles - self._prev_joint)
        else:
            delta_joint = np.zeros(7)

        self._prev_joint = joint_angles.copy()

        # --- obs/ ---
        self._episode_data["obs/joint_pos"].append(
            np.concatenate([joint_angles, [gripper_width, -gripper_width]]))
        self._episode_data["obs/joint_vel"].append(
            np.concatenate([joint_vel, [0.0, 0.0]]))
        self._episode_data["obs/eef_pos"].append(eef_pos)
        self._episode_data["obs/eef_quat"].append(eef_quat)
        self._episode_data["obs/gripper_pos"].append(
            np.array([gripper_width, -gripper_width]))

        # Action: [delta_q1..7, gripper_cmd]
        # gripper_cmd: -1 (close) to +1 (open), normalized
        gripper_cmd = (gripper_width - 0.02) / 0.02  # normalize to [-1, 1]
        self._episode_data["actions"].append(
            np.concatenate([delta_joint, [np.clip(gripper_cmd, -1, 1)]]))

        # --- obs/cube_* ---
        if cube_positions:
            cube_pos_flat = []
            cube_ori_flat = []
            obj_flat = []
            for name in sorted(cube_positions.keys()):
                pos = cube_positions[name]
                ori = cube_orientations.get(name, np.array([1.0, 0.0, 0.0, 0.0]))
                cube_pos_flat.extend(pos)
                cube_ori_flat.extend(ori)
                obj_flat.extend(pos)
                obj_flat.extend(ori)
            self._episode_data["obs/cube_positions"].append(np.array(cube_pos_flat))
            self._episode_data["obs/cube_orientations"].append(np.array(cube_ori_flat))
            self._episode_data["obs/object"].append(np.array(obj_flat))

        # --- obs/datagen_info ---
        # EEF pose as 4x4
        self._episode_data["obs/datagen_info/eef_pose/franka"].append(T_ee)

        # Cube poses as 4x4
        if cube_positions:
            for name in sorted(cube_positions.keys()):
                pos = cube_positions[name]
                ori = cube_orientations.get(name, np.array([1.0, 0.0, 0.0, 0.0]))
                T_cube = np.eye(4)
                T_cube[:3, 3] = pos
                T_cube[:3, :3] = _quat_to_rotmat(ori)
                self._episode_data[f"obs/datagen_info/object_pose/{name}"].append(T_cube)

        # Target EEF = current EEF (for Mimic compatibility)
        self._episode_data["obs/datagen_info/target_eef_pose/franka"].append(T_ee)

        # Subtask signals
        for name in SUBTASK_NAMES:
            self._episode_data[f"obs/datagen_info/subtask_term_signals/{name}"].append(
                self._current_subtasks[name])

        # --- states/ ---
        self._episode_data["states/articulation/robot/joint_position"].append(
            np.concatenate([joint_angles, [gripper_width, -gripper_width]]))
        self._episode_data["states/articulation/robot/joint_velocity"].append(
            np.concatenate([joint_vel, [0.0, 0.0]]))
        # Root pose (base of robot = identity in world)
        self._episode_data["states/articulation/robot/root_pose"].append(
            np.array([0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]))
        self._episode_data["states/articulation/robot/root_velocity"].append(
            np.zeros(6))

        # Cube states
        if cube_positions:
            for name in sorted(cube_positions.keys()):
                pos = cube_positions[name]
                ori = cube_orientations.get(name, np.array([1.0, 0.0, 0.0, 0.0]))
                self._episode_data[f"states/rigid_object/{name}/root_pose"].append(
                    np.concatenate([pos, ori]))
                self._episode_data[f"states/rigid_object/{name}/root_velocity"].append(
                    np.zeros(6))

        self._frame_count += 1

    def cancel_episode(self):
        """Cancel and discard current recording."""
        self._episode_data = None
        self._frame_count = 0
        self._is_recording = False
        self._prev_joint = None

    def finish_episode(self, success=True):
        """
        Finish current episode and store it.
        
        Args:
            success: whether the demonstration was successful
        
        Returns:
            episode_index: index of finished episode, or -1 if no data
        """
        if not self._is_recording or self._frame_count < 5:
            self.cancel_episode()
            return -1

        # Convert lists to numpy arrays
        episode = {}
        for key, values in self._episode_data.items():
            if values:
                episode[key] = np.array(values)
        
        episode["_success"] = success
        episode["_num_samples"] = self._frame_count
        episode["_timestamp"] = self._timestamp

        self._all_episodes.append(episode)
        idx = self._episode_index
        self._episode_index += 1

        self._episode_data = None
        self._frame_count = 0
        self._is_recording = False
        self._prev_joint = None

        return idx

    # ───── HDF5 Export ─────

    def save_to_hdf5(self, filepath: str, env_name: str = None):
        """
        Export all recorded episodes to HDF5 file.
        Format is compatible with Isaac Lab Mimic / robomimic.
        
        Args:
            filepath: output .hdf5 file path
            env_name: environment name string
        """
        if not self._all_episodes:
            print("No episodes to save.")
            return

        import h5py

        filepath = str(Path(filepath).with_suffix(".hdf5"))
        print(f"Saving {len(self._all_episodes)} episodes to {filepath}...")

        with h5py.File(filepath, "w") as f:
            data_group = f.create_group("data")
            data_group.attrs["total"] = len(self._all_episodes)
            data_group.attrs["env_args"] = json.dumps({
                "env_name": env_name or "Franka-CubeStack-Custom-v0",
                "type": 2,
            })

            for ep_idx, episode in enumerate(self._all_episodes):
                ep_name = f"demo_{ep_idx}"
                ep_group = data_group.create_group(ep_name)
                ep_group.attrs["num_samples"] = episode["_num_samples"]
                ep_group.attrs["success"] = bool(episode["_success"])

                # Save all recorded data into hierarchical groups
                for key, data in episode.items():
                    if key.startswith("_"):
                        continue

                    # Create nested groups
                    parts = key.split("/")
                    current = ep_group
                    for part in parts[:-1]:
                        if part not in current:
                            current = current.create_group(part)
                        else:
                            current = current[part]
                    
                    # Don't store empty data
                    if data.size == 0:
                        continue

                    current.create_dataset(
                        parts[-1],
                        data=data,
                        compression="gzip",
                        compression_opts=4,
                    )

                # Ensure initial_state group exists with first frame
                self._write_initial_state(ep_group, episode)

        print(f"✅ Saved {len(self._all_episodes)} episodes to {filepath}")

    def _write_initial_state(self, ep_group, episode):
        """Write initial_state group from first frame of episode."""
        init_group = ep_group.create_group("initial_state")

        # articulation/robot/
        art_group = init_group.create_group("articulation/robot")
        for key_name in ["joint_position", "joint_velocity", "root_pose", "root_velocity"]:
            source_key = f"states/articulation/robot/{key_name}"
            if source_key in episode:
                data = episode[source_key]
                first_frame = data[0:1] if data.ndim > 1 else data
                art_group.create_dataset(key_name, data=first_frame, compression="gzip")

        # rigid_object/cube_N/
        for ep_key in episode.keys():
            if ep_key.startswith("states/rigid_object/"):
                obj_path = ep_key[len("states/"):]
                parts = obj_path.split("/")
                obj_name = parts[1]

                current = init_group
                for p in ["rigid_object", obj_name]:
                    if p not in current:
                        current = current.create_group(p)
                    else:
                        current = current[p]

                field_name = parts[2]
                data = episode[ep_key]
                first_frame = data[0:1] if data.ndim > 1 else data
                current.create_dataset(field_name, data=first_frame, compression="gzip")

    def get_episode_count(self):
        return len(self._all_episodes)

    def clear_episodes(self):
        """Clear all stored episodes (for fresh start)."""
        self._all_episodes.clear()
        self._episode_index = 0


def _quat_to_rotmat(q):
    """(w, x, y, z) quaternion → 3x3 rotation matrix."""
    w, x, y, z = q
    return np.array([
        [1 - 2*y*y - 2*z*z,   2*x*y - 2*w*z,     2*x*z + 2*w*y],
        [2*x*y + 2*w*z,       1 - 2*x*x - 2*z*z, 2*y*z - 2*w*x],
        [2*x*z - 2*w*y,       2*y*z + 2*w*x,     1 - 2*x*x - 2*y*y],
    ])
