from typing import Dict, List
from pathlib import Path
import pickle
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from statsmodels.tsa.stattools import kpss
import matplotlib.pyplot as plt

from arima_forecasting.arima_model import ArimaPlayerModel, iterative_imputation, decompose_features


def save_as_pickle(path_to_save: Path, file_name: str, model: ArimaPlayerModel):
    pickle.dump(model, open(path_to_save / file_name, "wb"))


def train_models(players, path_to_save):
    for name, player in players.items():
        X_train, y_train = prepare_player_data(player)
        model = ArimaPlayerModel.fit(name, X_train, y_train, 3, (1, 1, 2), (1, 1, 0))
        save_as_pickle(path_to_save, f"{name}.pkl", model)


def kpss_test(timeseries):
    kpsstest = kpss(timeseries, regression="c", nlags="auto")
    kpss_output = pd.Series(
        kpsstest[0:3], index=["Test Statistic", "p-value", "Lags Used"]
    )
    return kpss_output[1]


def evaluate_model(X_train, y_train, params: Dict[str, List]):
    results = []
    for components, readiness_order, feature_order in zip(params["nr_components"],
                                                          params["readiness_order"],
                                                          params["feature_order"]):
        arima = ArimaPlayerModel.fit("name", X_train, y_train, components,
                                 readiness_order,
                                 feature_order)
        results.append(
            {"MAE": arima.readiness_model.mae,
             "AICC": arima.readiness_model.aicc,
             "BIC": arima.readiness_model.bic,
             "stat_test_y": kpss_test(arima.y_train.diff()[1:]),
             "stat_test_feat": kpss_test(arima.decomposed_features[:,1])
             }
        )
    return results


def df_strip_nans(df: pd.DataFrame):
    first_idx = df["stress"].first_valid_index()
    last_idx = df["stress"].last_valid_index()
    return df.loc[first_idx:last_idx]


def evaluate_forecasting(teams):
    all_players = list(teams["TeamA"].players.values()) + list(teams["TeamB"].players.values())
    results = {}
    for name, window_size in zip(["1", "3", "7"], [1, 3, 7]):
        player_results = []
        for player in all_players:
            amount_missing_data = player.stress.isna().sum()
            X_train, y_train, X_test, y_test = prepare_player_data_for_eval(player)
            decomp_test = decompose_features(X_test, 3)[:, 1]
            model = ArimaPlayerModel.fit(player.name, X_train, y_train, 3, (1, 1, 2), (1, 1, 0))
            res = model.forecasting(decomp_test, y_test, window_size)
            res["missing"] = amount_missing_data.astype("float64")
            player_results.append(res)
        results[name] = player_results
        print(f"{name} is done")

    with open('window_experiment_results.json', 'w') as file:
        json.dump(results, file)

    for window_size, results in results.items():
        print(f"Window Size: {window_size}")
        print(f"Mean MSE: {pd.DataFrame(results)['mse'].mean()}")
        print("____________________________________________________")


def prepare_player_data(player):
    player_df = df_strip_nans(player.to_dataframe())
    col_names = player_df.columns
    X_index = player_df.index
    X, _ = iterative_imputation(player_df)
    X = pd.DataFrame(X, columns=col_names, index=X_index)
    y = X["readiness"]
    X_train = X.drop(["readiness"], axis=1)
    return X_train, y


def prepare_player_data_for_eval(player):
    player_df = df_strip_nans(player.to_dataframe())
    col_names = player_df.columns
    X_train, X_test = train_test_split(player_df, test_size=0.2, shuffle=False)
    train_index = X_train.index
    test_index = X_test.index
    X_train_np, X_test_np = iterative_imputation(X_train, X_test)
    X_train = pd.DataFrame(X_train_np, columns=col_names)
    X_test = pd.DataFrame(X_test_np, columns=col_names)
    y_test = X_test["readiness"]
    y_test.index = test_index
    X_test.index = test_index
    X_train.index = train_index
    X_test_done = X_test.drop(["readiness"], axis=1)
    return X_train, X_train["readiness"], X_test_done,  y_test

if __name__ == "__main__":
    path_to_data = Path(__file__).parent / "data" / "pickles" / "teams.pkl"
    teams = pickle.load(open(path_to_data, "rb"))
    player = list(teams["TeamA"].players.values())[5]
    params = {"nr_components": [3, 3, 3, 3, 3, 3, 3],
            "readiness_order": [(1,1,2), (1,1,1), (1,1,0), (2,1,0), (2,1,1), (2,1,2), (1,0,0)],
            "feature_order": [(1,1,0), (1,0,1), (1,1,1), (2,0,0), (2,0,1), (2,1,1), (2,1,2)]}
    #eval_results = pd.DataFrame(evaluate_model(X_train, y_train, params))
    players = {**teams["TeamA"].players, **teams["TeamB"].players}
    train_models(players, Path(__file__).parent / "data" / "pickles"/ "arima")

