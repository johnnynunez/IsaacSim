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

import asyncio
import math

import numpy as np
import omni.kit.test
from isaacsim.core.api import World
from isaacsim.core.api.objects import DynamicCuboid
from isaacsim.core.prims import SingleArticulation
from isaacsim.core.utils.stage import add_reference_to_stage, create_new_stage_async, update_stage_async
from isaacsim.sensors.physics import ContactSensor
from isaacsim.storage.native import get_assets_root_path


class TestContactSensorWrapper(omni.kit.test.AsyncTestCase):
    # Before running each test
    async def setUp(self):
        await create_new_stage_async()
        self.my_world = World(stage_units_in_meters=1.0)
        await self.my_world.initialize_simulation_context_async()
        await update_stage_async()
        self.my_world.scene.add_default_ground_plane()
        cube_2 = self.my_world.scene.add(
            DynamicCuboid(
                prim_path="/World/new_cube_2",
                name="cube_1",
                position=np.array([0, 0, 1.0]),
                scale=np.array([0.6, 0.5, 0.2]),
                size=1.0,
                color=np.array([255, 0, 0]),
            )
        )
        self._contact_sensor = self.my_world.scene.add(
            ContactSensor(
                prim_path="/World/new_cube_2/contact_sensor",
                name="ant_contact_sensor",
                min_threshold=0,
                max_threshold=10000000,
                radius=-1,
            )
        )
        await self.my_world.reset_async()
        return

    # After running each test
    async def tearDown(self):
        self.my_world.clear_instance()
        await omni.kit.app.get_app().next_update_async()
        while omni.usd.get_context().get_stage_loading_status()[2] > 0:
            # print("tearDown, assets still loading, waiting to finish...")
            await asyncio.sleep(1.0)
        await omni.kit.app.get_app().next_update_async()
        return

    async def test_data_acquisition(self):
        await update_stage_async()
        await update_stage_async()
        data = self._contact_sensor.get_current_frame()
        for key in ["time", "physics_step", "in_contact", "force", "number_of_contacts"]:
            self.assertTrue(key in data.keys())
        await update_stage_async()
        await update_stage_async()
        await update_stage_async()
        await update_stage_async()
        self.assertTrue("contacts" not in data.keys())
        self._contact_sensor.add_raw_contact_data_to_frame()
        await update_stage_async()
        await update_stage_async()
        self.assertTrue("contacts" in data.keys())
        self._contact_sensor.remove_raw_contact_data_from_frame()
        await update_stage_async()
        await update_stage_async()
        self.assertTrue("contacts" not in data.keys())
        return

    async def test_pause_resume(self):
        await update_stage_async()
        await update_stage_async()
        data = self._contact_sensor.get_current_frame()
        current_time = data["time"]
        current_step = data["physics_step"]
        self._contact_sensor.pause()
        await update_stage_async()
        await update_stage_async()
        await update_stage_async()
        await update_stage_async()
        data = self._contact_sensor.get_current_frame()
        self.assertTrue(data["time"] == current_time)
        self.assertTrue(data["physics_step"] == current_step)
        self.assertTrue(self._contact_sensor.is_paused())
        current_time = data["time"]
        current_step = data["physics_step"]
        self._contact_sensor.resume()
        await update_stage_async()
        data = self._contact_sensor.get_current_frame()
        self.assertTrue(data["time"] != current_time)
        self.assertTrue(data["physics_step"] != current_step)
        await self.my_world.reset_async()
        data = self._contact_sensor.get_current_frame()
        # reset async does two steps
        self.assertEqual(data["physics_step"], 2)
        self.assertAlmostEqual(data["time"], 0.01666666753590107, delta=0.01)
        return

    async def test_properties(self):
        self._contact_sensor.set_frequency(20)
        self.assertTrue(math.isclose(20, self._contact_sensor.get_frequency(), abs_tol=2))
        self._contact_sensor.set_dt(0.2)
        self.assertTrue(math.isclose(0.2, self._contact_sensor.get_dt(), abs_tol=0.01))
        self._contact_sensor.set_radius(0.1)
        self.assertTrue(math.isclose(0.1, self._contact_sensor.get_radius(), abs_tol=0.01))
        self._contact_sensor.set_min_threshold(0.1)
        self.assertTrue(math.isclose(0.1, self._contact_sensor.get_min_threshold(), abs_tol=0.01))
        self._contact_sensor.set_max_threshold(100000)
        self.assertTrue(math.isclose(100000, self._contact_sensor.get_max_threshold(), abs_tol=0.01))
        return
