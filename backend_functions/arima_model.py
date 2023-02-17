import pandas as pd
import statsmodels.api as sm
from sklearn.decomposition import PCA
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.metrics import mean_squared_error



def decompose_features(feature_train, nr_comp):
    pca = PCA(n_components=nr_comp)
    pca.fit(feature_train)
    return pca.transform(feature_train)#, pca.explained_variance_ratio_


def prepare_dataset(X_train, nr_comp):
    decomp_features = decompose_features(X_train, nr_comp)
    return decomp_features


def iterative_imputation(X_nan_train: pd.DataFrame,
                         X_test: pd.DataFrame = None,
                        ):
    imputer = IterativeImputer(max_iter=10, random_state=0)
    X_train = imputer.fit_transform(X_nan_train)
    X_test = imputer.transform(X_test)
    return X_train, X_test


class ArimaPlayerModel:

    def __init__(self, player_name,  readiness_model, component_model, decomposed_features, y_train):
        self.player_name = player_name
        self.readiness_model = readiness_model
        self.component_model = component_model
        self.decomposed_features = decomposed_features
        self.y_train = y_train

    def __str__(self):
        return self.player_name

    def __hash__(self):
        print(hash(str(self)))
        return hash(str(self))

    def __eq__(self, other):
        return self.player_name == other.player_name

    @classmethod
    def fit(cls, player_name: str,  X_train: pd.DataFrame, y_train: pd.Series,
            nr_components, readiness_order, feature_order):
        decomposed_features = prepare_dataset(X_train, nr_components)
        first_comp_model = sm.tsa.ARIMA(endog=decomposed_features[:, 1], order=feature_order).fit()
        readiness_model = sm.tsa.ARIMA(endog=y_train, order=readiness_order, exog=decomposed_features[:, 1]).fit()
        return cls(player_name, readiness_model, first_comp_model, decomposed_features, y_train)

    def predict(self, forecasting_steps):
        feature_forecast = self.component_model.forecast(steps=forecasting_steps)
        return self.readiness_model.get_forecast(steps=forecasting_steps, exog=feature_forecast)

    def forecasting(self, X_test, y_test, forecasting_steps):
        appended_decomp_model = self.component_model
        appended_readiness_model = self.readiness_model
        results = {}
        latest_y = None
        forecasts = []
        for step in range(forecasting_steps, len(X_test)-forecasting_steps, forecasting_steps):
            latest_X = X_test[:step]
            latest_y = y_test[:step].values
            decomp_forecast =appended_decomp_model.forecast(forecasting_steps)
            appended_decomp_model = appended_decomp_model.append(latest_X, refit=True)
            forecast = appended_readiness_model.get_forecast(forecasting_steps, exog=decomp_forecast)
            appended_readiness_model = appended_readiness_model.append(endog=latest_y, exog=latest_X, refit=True)
            forecasts.append(forecast.predicted_mean)

        output = {}
        results["forecast"] = pd.concat(forecasts).reset_index(drop=True)
        results["true"] = latest_y
        output["mse"] = mean_squared_error(results["true"], results["forecast"])
        return output




