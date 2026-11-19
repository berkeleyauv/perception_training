# perception_training

Dataset consolidation, validation, export, training, and evaluation pipeline
for underwater robotics perception (RoboSub), starting with the gate task.

**Status: MVP.** The full pipeline runs end to end on a tiny synthetic fixture.
Real-data importers are not yet implemented.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```
Tested with Python 3.11. `requirements.txt` has the exact versions used.

## Commands

Prepare a dataset (generate fixture, import, validate, dedupe, split, export YOLO Detect):

```bash
python -m dataset_tools.prepare
```

Train (1-2 epoch smoke test):

```bash
python training/train.py configs/smoke_detect.yaml
```

Outputs go to `runs/smoke/` (gitignored).

## Pipeline

1. `dataset_tools/make_fixture.py`: tiny fake dataset with known boxes and fake scene IDs
2. `dataset_tools/importers/`: converts a source into the common manifest (`data/manifest.json`)
3. `dataset_tools/validators/`: schema values, required fields, pixel-bounds checks
4. `dataset_tools/splits/`: hash dedupe, scene-aware train/val/test split with a leakage check
5. `dataset_tools/exporters/`: YOLO Detect layout and `dataset.yaml`
6. `training/`, `configs/`: config-driven YOLO training with a fixed seed

Missing values are stored as `null`, never guessed. Records without a usable
label are excluded from an export instead of getting invented labels.

## Schema


## Not yet implemented

- Importers for the real synthetic generator output and reviewed SAM labels
- YOLO Pose and Segment export
- Visual overlays for QA
- Evaluation (precision/recall, keypoint error, failure cases, run metadata)
- Frozen real-world evaluation split
- Shared-storage (OCF) artifact workflow
- CI
- Final schema 
