import argparse

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def train_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--normalize", default=True, type=bool, help="maximum depth")
    parser.add_argument(
        "--n_estimators", default=100, type=int, help="number of estimators"
    )
    parser.add_argument(
        "--max_features",
        default=6,
        type=int,
        help="maximum of features",
    )
    parser.add_argument("--max_depth", default=5, type=int, help="maximum depth")
    opt = parser.parse_args()
    return opt


df = pd.read_csv("housing.csv")
# print(df.head())
opt = train_options()
df.dropna(inplace=True)
X = df[
    [
        "total_rooms",
        "total_bedrooms",
        "population",
        "households",
        "median_income",
        "median_house_value",
    ]
]
y = df["median_house_value"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# print(X)
# print(y)

if opt.normalize == True:
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

rf = RandomForestRegressor(
    n_estimators=opt.n_estimators,
    max_features=opt.max_features,
    max_depth=opt.max_depth,
)
model = rf.fit(X_train, y_train)
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_pred, y_test))
mae = mean_absolute_error(y_pred, y_test)
print("rmse: ", rmse)
print("mae: ", mae)
