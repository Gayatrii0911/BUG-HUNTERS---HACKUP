import os
import pickle
import numpy as np
from sklearn.ensemble import IsolationForest
from typing import List

MODEL_PATH = "anomaly_model.pkl"

_model: IsolationForest = None

def _get_model() -> IsolationForest:
    global _model
    if _model is None:
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "rb") as f:
                _model = pickle.load(f)
        else:
            # Bootstrap with dummy normal data so the model is usable immediately
            dummy = np.random.normal(loc=[500, 0, 0.5, 0.1, 0, 0, 0, 0, 0.1, 0, 0, 0],
                                     scale=[200, 1, 0.3, 0.1, 0.3, 0.3, 0.3, 0.3, 0.1, 0.3, 0.3, 0.3],
                                     size=(200, 12))
            _model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
            _model.fit(dummy)
            save_model(_model)
    return _model

def score_transaction(features: List[float]) -> float:
    """Returns anomaly score from 0.0 (normal) to 1.0 (highly anomalous)."""
    model = _get_model()
    arr = np.array(features).reshape(1, -1)
    raw = model.decision_function(arr)[0]  # negative = anomalous
    # Normalize: typical range is [-0.5, 0.5], map to [0, 1] inverted
    normalized = max(0.0, min(1.0, (0.5 - raw)))
    return round(float(normalized), 3)

def retrain(all_features: List[List[float]]):
    """Adaptive retraining — call this when new labeled data arrives."""
    global _model
    X = np.array(all_features)
    _model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    _model.fit(X)
    save_model(_model)

def save_model(model):
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)