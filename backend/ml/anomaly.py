import os
import pickle
import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from typing import List

MODEL_PATH = "anomaly_ensemble.pkl"

class FraudEnsemble:
    def __init__(self):
        self.iso_forest = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
        # RF for supervised hint - bootstrapped with known patterns
        self.rf = RandomForestClassifier(n_estimators=50, random_state=42)
        self.is_trained = False

    def bootstrap(self):
        # 14-dimensional features to match features.py extraction
        # [amount, sender_id, amount_dev, dev_score, new_rec, new_dev, new_loc, freq, risk, travel, mismatch, graph_risk, conns, cycle]
        
        # Normal Baseline
        normal = np.random.normal(loc=[500, 100, 0, 0.1, 0, 0, 0, 0, 0.1, 0, 0, 0.1, 1, 0],
                                  scale=[200, 50, 0.1, 0.05, 0.1, 0.1, 0.1, 0.1, 0.05, 0.1, 0.1, 0.05, 0.5, 0.1],
                                  size=(300, 14))
        
        # Fraud Patterns (Known)
        # Pattern 1: High amount + New Device + New Location + Graph Risk
        fraud1 = np.random.normal(loc=[5000, 100, 5, 0.8, 1, 1, 1, 0, 0.8, 1, 0, 0.7, 5, 1],
                                  scale=[500, 20, 1, 0.1, 0, 0, 0, 0, 0.1, 0, 0, 0.1, 1, 0],
                                  size=(20, 14))
        
        # Pattern 2: Frequency Spike + High Deviation
        fraud2 = np.random.normal(loc=[200, 100, 8, 0.9, 0, 0, 0, 1, 0.5, 0, 0, 0.3, 2, 0],
                                  scale=[50, 20, 1, 0.1, 0, 0, 0, 0, 0.1, 0, 0, 0.1, 1, 0],
                                  size=(20, 14))
        
        X = np.vstack([normal, fraud1, fraud2])
        y = np.array([0]*300 + [1]*20 + [1]*20)
        
        self.iso_forest.fit(X)
        self.rf.fit(X, y)
        self.is_trained = True

    def predict(self, features: List[float]) -> float:
        arr = np.array(features).reshape(1, -1)
        # Unsupervised Outlier Score
        iso_score = self.iso_forest.decision_function(arr)[0]
        # Supervised Classification Prob
        rf_prob = self.rf.predict_proba(arr)[0][1]
        
        # Fusing: High RF prob or Low Iso score = High Anomaly
        # Iso score: ~0.15 is normal, <0 is outlier
        normalized_iso = 0.5 + (0.0 - iso_score) if iso_score < 0.05 else max(0, (0.15 - iso_score) * 2)
        
        # Final Anomaly Score is Max of both (Sensitive)
        final = max(float(rf_prob), float(normalized_iso))
        return round(float(min(1.0, final)), 3)

    def retrain(self, X_train: np.ndarray, y_train: np.ndarray):
        self.iso_forest.fit(X_train)
        self.rf.fit(X_train, y_train)
        self.is_trained = True

_ensemble: FraudEnsemble = None

def _get_ensemble() -> FraudEnsemble:
    global _ensemble
    if _ensemble is None:
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "rb") as f:
                _ensemble = pickle.load(f)
        else:
            _ensemble = FraudEnsemble()
            _ensemble.bootstrap()
            save_model(_ensemble)
    return _ensemble

def score_transaction(features: List[float]) -> float:
    ensemble = _get_ensemble()
    return ensemble.predict(features)

def retrain(all_features: List[List[float]]):
    ensemble = _get_ensemble()
    X = np.array(all_features)
    # Automated labeling: score > 0.6 is anomalous hint for next cycle
    y = np.array([1 if ensemble.predict(f) > 0.6 else 0 for f in all_features])
    ensemble.retrain(X, y)
    save_model(ensemble)

def save_model(model):
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)