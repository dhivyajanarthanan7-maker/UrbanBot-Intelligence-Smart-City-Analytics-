import os
from ultralytics import YOLO

# cache models in memory
_loaded_models = {}

def get_model(model_name, model_path):
    """
    Loads YOLO model only once and reuses it across pages.
    """

    # already loaded
    if model_name in _loaded_models:
        return _loaded_models[model_name]

    # check path
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")

    # load model
    model = YOLO(model_path)

    # cache it
    _loaded_models[model_name] = model

    return model
