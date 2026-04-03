from backend.ml.anomaly import retrain, _get_model

def warmup():
    """Call at app startup to ensure model is loaded."""
    _get_model()
    print("[ML] Anomaly model ready.")