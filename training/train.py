"""Train a YOLO model from a YAML config. Usage: python training/train.py configs/smoke_detect.yaml"""
import sys
import yaml
from ultralytics import YOLO
from pathlib import Path

def main(config_path):
    cfg = yaml.safe_load(open(config_path))
    cfg["project"] = str(Path(cfg["project"]).resolve())
    model = YOLO(cfg.pop("model"))
    model.train(**cfg)


if __name__ == "__main__":
    main(sys.argv[1])
