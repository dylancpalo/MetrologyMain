# Mu2e tracker metrology and offline alignment fits

This repository combines the metrology inputs used to determine tracker-panel and station positions in the tracker coordinate frame. Its inputs include the X-ray measurement dataset, camera-metrology results stored in PostgreSQL, tracker-frame measurements, and related mechanical and survey data.

## Workflow role

1. `StationMetrology.sh` runs the station-level metrology sequence.
2. `GlobalProductionClean.py` coordinates the main production analysis.
3. `DBCommands.py` retrieves measurement data from PostgreSQL, while `TransformationCommands.py` provides the coordinate transformations and fits used to bring the datasets into a common frame.
4. `OpenDukeData.py` processes the X-ray scan data, fitting wire lines and straw sagitta measurements and expressing the measurements in the fiducial coordinate system.
5. `PanelPlaneTables.py` performs the offline fits that determine the values needed to construct the tracker alignment tables. These fitted offline values are an explicit output of this repository's workflow.

The camera image acquisition and import workflow is in [CameraMetrologyImageGrab_Processing](https://github.com/dylancpalo/CameraMetrologyImageGrab_Processing). The station camera results are one of several inputs combined here; the X-ray dataset and tracker-frame data are also part of the metrology solution.

## Ultem measurements and machining

The final station geometry also depends on the Ultem mounting pieces. [UltemAnalysis](https://github.com/dylancpalo/UltemAnalysis) covers their image-based measurements, quality control, and evaluation of the machining geometry. That work informs both whether the parts meet requirements and how the Ultems should be machined; it is a complementary part of establishing the final geometry, not a substitute for the metrology fits in `PanelPlaneTables.py`.

## Contents

- `StationMetrology.sh` — runs the station metrology sequence.
- `GlobalProductionClean.py` — main production-analysis driver.
- `Constants.py` — shared constants and configuration values.
- `DBCommands.py` — PostgreSQL data-access commands.
- `TransformationCommands.py` — transformations and fits between measurement coordinate systems.
- `OpenDukeData.py` — X-ray scan data processing and fits.
- `PanelPlaneTables.py` — offline fits for the values used in alignment tables.

## Environment

The scripts depend on the Mu2e metrology data sources, PostgreSQL setup, and Python scientific packages used by the analysis. Database access and input paths must be configured for the environment where the analysis is run.

## Related repositories

- [CameraMetrologyImageGrab_Processing](https://github.com/dylancpalo/CameraMetrologyImageGrab_Processing) acquires and processes camera images and imports station-assembly measurements into PostgreSQL.
- [UltemAnalysis](https://github.com/dylancpalo/UltemAnalysis) evaluates Ultem measurements, quality control, and machining geometry.
- [TrackBasedAlignment](https://github.com/dylancpalo/TrackBasedAlignment) provides track-based alignment studies and validation.
