# SPDX-FileCopyrightText: Copyright (c) 2022-2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
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
import argparse

import yaml


def main(args):
    merged_data = {"adjacencies": [], "tiles": []}
    # Load all rules data
    for config_path in args.config_files:
        with open(config_path, "r") as yaml_file:
            config_data = yaml.safe_load(yaml_file)
        # Iterate over all added adjacencies
        for current_adj_data in config_data["adjacencies"]:
            is_update = False
            # Check in the existing ones if the tile already exists
            for merged_adj in merged_data["adjacencies"]:
                # If we find a tile with the same type, check if the adjacency itself already exists
                if current_adj_data["id"] == merged_adj["id"]:
                    for neighbor in current_adj_data["neighbors"]:
                        exists = False
                        for merged in merged_adj["neighbors"]:
                            if merged["neighbor_id"] != neighbor["neighbor_id"]:
                                continue
                            if merged["neighbor_rotation"] != neighbor["neighbor_rotation"]:
                                continue
                            if merged["self_rotation"] != neighbor["self_rotation"]:
                                continue
                            exists = True
                            break
                        # If the adjacency does not exist yet, add it to the list
                        if not exists:
                            merged_adj["neighbors"].append(neighbor)
                    is_update = True
                    break
            if is_update:
                continue
            # If this is the first time the tile type appears, simply add all adjacencies
            merged_data["adjacencies"].append(current_adj_data)
        for current_weights in config_data["tiles"]:
            is_update = False
            for merged_weight in merged_data["tiles"]:
                if current_weights["id"] == merged_weight["id"]:
                    is_update = True
                    break
            if is_update:
                continue
            merged_data["tiles"].append(current_weights)
    with open(args.save_path, "w") as yaml_file:
        yaml.dump(merged_data, yaml_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("save_path", help="Path to save the combined rules file.")
    parser.add_argument("--config_files", nargs="+", default=[], help="All files to be combined")
    args = parser.parse_args()
    main(args)
