# SPDX-FileCopyrightText: Copyright (c) 2021-2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
from isaacsim.core.utils.types import ArticulationAction
from isaacsim.examples.interactive.base_sample import BaseSample
from isaacsim.robot.manipulators.examples.franka.tasks import FollowTarget as FollowTargetTask


class ReplayFollowTarget(BaseSample):
    def __init__(self) -> None:
        super().__init__()
        self._articulation_controller = None

    def setup_scene(self):
        world = self.get_world()
        world.add_task(FollowTargetTask())
        return

    async def setup_pre_reset(self):
        world = self.get_world()
        if world.physics_callback_exists("replay_trajectory"):
            world.remove_physics_callback("replay_trajectory")
        if world.physics_callback_exists("replay_scene"):
            world.remove_physics_callback("replay_scene")
        return

    async def setup_post_load(self):
        self._franka_task = list(self._world.get_current_tasks().values())[0]
        self._task_params = self._franka_task.get_params()
        my_franka = self._world.scene.get_object(self._task_params["robot_name"]["value"])
        self._articulation_controller = my_franka.get_articulation_controller()
        self._data_logger = self._world.get_data_logger()
        return

    async def _on_replay_trajectory_event_async(self, data_file):
        self._data_logger.load(log_path=data_file)
        world = self.get_world()
        await world.play_async()
        world.add_physics_callback("replay_trajectory", self._on_replay_trajectory_step)
        return

    async def _on_replay_scene_event_async(self, data_file):
        self._data_logger.load(log_path=data_file)
        world = self.get_world()
        await world.play_async()
        world.add_physics_callback("replay_scene", self._on_replay_scene_step)
        return

    def _on_replay_trajectory_step(self, step_size):
        if self._world.current_time_step_index < self._data_logger.get_num_of_data_frames():
            data_frame = self._data_logger.get_data_frame(data_frame_index=self._world.current_time_step_index)
            self._articulation_controller.apply_action(
                ArticulationAction(joint_positions=data_frame.data["applied_joint_positions"])
            )
        return

    def _on_replay_scene_step(self, step_size):
        if self._world.current_time_step_index < self._data_logger.get_num_of_data_frames():
            target_name = self._task_params["target_name"]["value"]
            data_frame = self._data_logger.get_data_frame(data_frame_index=self._world.current_time_step_index)
            self._articulation_controller.apply_action(
                ArticulationAction(joint_positions=data_frame.data["applied_joint_positions"])
            )
            self._world.scene.get_object(target_name).set_world_pose(
                position=np.array(data_frame.data["target_position"])
            )
        return
