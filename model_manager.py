# model_manager.py
from ultralytics import YOLO
import gc

_current_model = None
_current_path = None

def get_model(model_path: str):
    global _current_model, _current_path

    # If same model already loaded → reuse
    if _current_model is not None and _current_path == model_path:
        return _current_model

    # If different model → unload previous model
    if _current_model is not None:
        del _current_model
        gc.collect()

    # Load new model
    _current_model = YOLO(model_path)
    _current_path = model_path

    return _current_model
