import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from scipy.spatial import ConvexHull, cKDTree
from matplotlib.path import Path
from itertools import combinations


train_file = "F:/聚球藻/new/abundance - new - 副本.csv"
pred_file = "F:/聚球藻/new/data_2023_demo.xlsx"

train_df = pd.read_csv(train_file)
pred_df = pd.read_excel(pred_file)


features = [
    "Temperature","Salinity","pCO2","Mixed-layer-depth",
    "Oxygen","Nitrate","Phosphate","Silicate",
    "Iron","Carbonate"
]

X_train = train_df[features]
X_pred = pred_df[features]


scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_pred_scaled = scaler.transform(X_pred)

pca = PCA()

train_pca = pca.fit_transform(X_train_scaled)
pred_pca = pca.transform(X_pred_scaled)

var = np.cumsum(pca.explained_variance_ratio_)
n_pc = np.argmax(var >= 0.9) + 1

print("PCA轴数量:", n_pc)

train_pca = train_pca[:, :n_pc]
pred_pca = pred_pca[:, :n_pc]


pc_pairs = list(combinations(range(n_pc),2))

print("PC组合数:", len(pc_pairs))

extrap_count = np.zeros(len(pred_pca))

for pc1, pc2 in pc_pairs:

    train_points = train_pca[:,[pc1,pc2]]

    hull = ConvexHull(train_points)

    hull_path = Path(train_points[hull.vertices])

    pred_points = pred_pca[:,[pc1,pc2]]

    inside = hull_path.contains_points(pred_points)

    extrap_count += (~inside)

env_extrapolation = extrap_count / len(pc_pairs)

pred_df["env_extrapolation"] = env_extrapolation


train_coords = train_df[["lat","lon"]].values
pred_coords = pred_df[["lat","lon"]].values

tree = cKDTree(train_coords)

distances, _ = tree.query(pred_coords,k=1)

pred_df["geo_distance"] = distances

scaler_env = MinMaxScaler()
scaler_geo = MinMaxScaler()

pred_df["env_scaled"] = scaler_env.fit_transform(pred_df[["env_extrapolation"]])
pred_df["geo_scaled"] = scaler_geo.fit_transform(pred_df[["geo_distance"]])


pred_df["final_extrapolation"] = (
    2*pred_df["env_scaled"] + pred_df["geo_scaled"]
)/3


pred_df["underrepresented"] = pred_df["final_extrapolation"] > 0.05

pred_df.to_csv(
    "F:/聚球藻/new/extrapolation_map_2023.csv",
    index=False
)

print("完成")
