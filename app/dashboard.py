# app/dashboard.py

import streamlit as st
import pandas as pd
import xgboost as xgb
import os
from utils.features import get_feature_columns

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

st.set_page_config(page_title="NBA Player Projections", layout="wide")
st.title("🏀 NBA Player Projection Dashboard")


@st.cache_data
def load_dataset():
    path = os.path.join(ROOT, "data/dataset.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()


@st.cache_resource
def load_model(name):
    path = os.path.join(ROOT, f"models/{name}_xgb.json")
    if not os.path.exists(path):
        return None
    m = xgb.XGBRegressor()
    m.load_model(path)
    return m


df = load_dataset()

if df.empty:
    st.warning("⚠️ No dataset found. Run scraper → dataset → training.")
    st.stop()

points_model = load_model("points")
reb_model = load_model("rebounds")
ast_model = load_model("assists")

players = sorted(df["player_name"].unique())
player = st.selectbox("Select Player", players)

p_df = df[df["player_name"] == player].sort_values("game.date")
latest = p_df.tail(1).iloc[0]

X = latest[get_feature_columns()].values.reshape(1, -1)

pts = points_model.predict(X)[0]
reb = reb_model.predict(X)[0]
ast = ast_model.predict(X)[0]

col1, col2, col3 = st.columns(3)
col1.metric("Projected Points", f"{pts:.1f}")
col2.metric("Projected Rebounds", f"{reb:.1f}")
col3.metric("Projected Assists", f"{ast:.1f}")

st.line_chart(
    p_df.tail(10).set_index("game.date")[["points","rebounds","assists"]]
)
