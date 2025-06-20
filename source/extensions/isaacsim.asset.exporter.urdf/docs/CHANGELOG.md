# Changelog

## [1.2.5] - 2025-06-02
### Changed
- Update lxml==5.4.0

## [1.2.4] - 2025-05-30
### Changed
- Update nvidia-srl-usd-to-urdf==1.0.1

## [1.2.3] - 2025-05-22
### Changed
- Update copyright and license to apache v2.0

## [1.2.2] - 2025-05-20
### Changed
- Update urdf exporter pip prebundle

## [1.2.1] - 2025-04-04
### Changed
- Version bump to fix extension publishing issues

## [1.2.0] - 2025-04-02
### Changed
- Moved Urdf Exporter into File menu next to the other Exporter
- Options are integrated into the File Exporter dialog
- Removed option to export from USD file without opening it on Stage
- usd to urdf library upgraded to python 3.11

## [1.1.5] - 2025-03-26
### Changed
- Cleanup and standardize extension.toml, update code formatting for all code

## [1.1.4] - 2025-03-04
### Changed
- Update to kit 107.1 and fix build issues

## [1.1.3] - 2025-01-21
### Changed
- Update extension description and add extension specific test settings

## [1.1.2] - 2025-01-14
### Added

- Missing dependency

## [1.1.1] - 2025-01-13
### Fixed

- Add missing `pathlib` to `exporter/urdf/ui_builder.py`

## [1.1.0] - 2024-10-29
### Fixed
- Fix incorrect URDF export when the USD prims have scaling values

### Changed
- Export .mtl files with the .obj files based on USD material prims
- Include inertia values from USD in URDF
- Use Isaac name override for frame name if it exists
- Add option to use ROS URI file prefix in the exported URDF

## [1.0.2] - 2024-10-28
### Changed
- Remove test imports from runtime

## [1.0.1] - 2024-10-24
### Changed
- Updated dependencies and imports after renaming

## [1.0.0] - 2024-09-27
### Fixed
- extension renamed to isaacsim.asset.exporter.urdf

## [0.3.2] - 2024-08-28
### Fixed
- Added missing dependency

## [0.3.1] - 2024-07-23
### Fixed
- removed unnecessary dependencies

## [0.3.0] - 2024-04-26
### Fixed
- Fix cylinder radii check
- Fix checking for duplicate prim names
- Fix issue with joint limits set to inf for revolute joints, set to continuous joint instead
- Fix cylinder scaling issue

### Added
- Replace absolute path and uri path options with mesh path prefix option
- Parse velocity and effort limits from USD and include in URDF
- Add UsdGeom.Cylinder to error message as one of the valid geom prim types
- Add hack to not include camera mesh files when exporting from isaac sim extension
- Add mesh file path char length check
- Add NodeType.SENSOR and functionality to include sensor frames in the URDF

## [0.2.0] - 2023-12-01
### Fixed
- Scaling bug when geometry prim is a child of Xform prim with scaling
- Cylinder scaling issue
- Joint frame alignment when child link transform is not identity
- Exporting revolute joints with inf limits, export as continuous joints now
- Too many root links
- Velocity and effort limits always being set to zero
- Large camera meshes added erroneously to URDF
- Terminal output labeled as error even when export is successful

### Added
- Exporting sensor prim frames to URDF
- Ability to set mesh path prefix
- Optionally setting output to directory (URDF file name automatically set to match USD file name)

## [0.1.1] - 2023-09-19
### Fixed
- Add missing dependencies and remove unused code

## [0.1.0] - 2023-07-27
### Added
- Initial version of Isaac Sim URDF exporter
