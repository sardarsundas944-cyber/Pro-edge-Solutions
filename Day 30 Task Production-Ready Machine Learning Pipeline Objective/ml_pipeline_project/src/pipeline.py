import os
import sys
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configs import config


def build_pipeline():
    pipeline = Pipeline(steps=[
        ("scaler", StandardScaler()),
        ("model", RandomForestClassifier(
            n_estimators=config.N_ESTIMATORS,
            max_depth=config.MAX_DEPTH,
            random_state=config.RANDOM_STATE
        ))
    ])
    return pipeline
