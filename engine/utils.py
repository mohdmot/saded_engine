import numpy as np
import pandas as pd

def normalize_scores(scores):
    """
    Normalize a list or array of scores to 0-1 range.
    """
    scores = np.array(scores)
    min_s = np.min(scores)
    max_s = np.max(scores)
    if max_s - min_s == 0:
        return np.zeros_like(scores)
    return (scores - min_s)/(max_s - min_s)


class FrequencyEncoder:
    def __init__(self):
        self.freq_maps = {}

    def fit(self, df):
        for col in df.columns:
            freq = df[col].value_counts(normalize=True)
            self.freq_maps[col] = freq.to_dict()

    def transform(self, df):
        df_out = pd.DataFrame()
        for col in df.columns:
            df_out[col] = df[col].map(self.freq_maps[col]).fillna(0)
        return df_out

    def fit_transform(self, df):
        self.fit(df)
        return self.transform(df)