import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from .utils import FrequencyEncoder

class Preprocessor:
    def __init__(self, config):
        self.config = config
        self.num_imputer = SimpleImputer(strategy="median")
        self.cat_imputer = SimpleImputer(strategy="most_frequent")
        self.scaler = StandardScaler()
        self.encoder = FrequencyEncoder()
        self.fitted = False
        self.feature_columns = []

    def fit_transform(self, df: pd.DataFrame):
        num_cols = self.config["numerical_columns"]
        cat_cols = self.config["categorical_columns"]

        df_processed = df.copy()

        # --- Numerical ---
        df_processed[num_cols] = self.num_imputer.fit_transform(df_processed[num_cols])
        df_processed[num_cols] = self.scaler.fit_transform(df_processed[num_cols])

        # --- Categorical ---
        df_processed[cat_cols] = self.cat_imputer.fit_transform(df_processed[cat_cols])
        df_processed[cat_cols] = self.encoder.fit_transform(df_processed[cat_cols])

        self.feature_columns = df_processed.columns.tolist()
        self.fitted = True

        return df_processed.to_numpy()

    def transform(self, df: pd.DataFrame):
        if not self.fitted:
            raise RuntimeError("Preprocessor must be fitted before transform.")

        num_cols = self.config["numerical_columns"]
        cat_cols = self.config["categorical_columns"]

        df_processed = df.copy()

        # --- Numerical ---
        df_processed[num_cols] = self.num_imputer.transform(df_processed[num_cols])
        df_processed[num_cols] = self.scaler.transform(df_processed[num_cols])

        # --- Categorical ---
        df_processed[cat_cols] = self.cat_imputer.transform(df_processed[cat_cols])
        df_processed[cat_cols] = self.encoder.transform(df_processed[cat_cols])

        return df_processed[self.feature_columns].to_numpy()