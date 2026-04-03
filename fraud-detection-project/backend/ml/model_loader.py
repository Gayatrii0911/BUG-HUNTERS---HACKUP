from backend.ml.anomaly import retrain, _get_ensemble

def warmup():
    """Call at app startup to ensure model is loaded."""
    _get_ensemble()
    print("[ML] Hybrid Forensic Ensemble ready.")