# train/train_model.py

import pandas as pd
import xgboost as xgb
import os
from utils.features import get_feature_columns

def train_stat_model(stat):
    df = pd.read_csv("data/dataset.csv")

    X = df[get_feature_columns()].fillna(0)
    y = df[stat].fillna(0)

    model = xgb.XGBRegressor(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05
    )

    model.fit(X, y)

    os.makedirs("models", exist_ok=True)
    out = f"models/{stat}_xgb.json"
    model.save_model(out)

    print(f"Saved model → {out}")
    return model
