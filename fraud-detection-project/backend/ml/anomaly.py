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
    
    # IsolationForest.decision_function:
    # Typical range is ~[0.2, -0.2]. Outliers are lower.
    raw = model.decision_function(arr)[0]
    
    # Shifted and Scaled Normalization for Elite Demo:
    # We want outliers (any raw score significantly lower than the mean)
    # to hit the High/Medium thresholds (> 0.5).
    # Assuming average normal score is around 0.15.
    
    if raw < -0.01:
        # High outlier probability
        normalized = 0.7 + abs(raw) * 2
    elif raw < 0.1:
        # Medium outlier/suspicious
        normalized = 0.5 + (0.1 - raw)
    else:
        # Normal
        normalized = max(0.0, (0.2 - raw) * 2)
        
    final = round(float(min(1.0, normalized)), 3)
    return final

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