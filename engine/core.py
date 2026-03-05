import os
import json
import pandas as pd
from .preprocessing import Preprocessor
from .layer_a import LayerA
from .layer_b import LayerB
from .fusion import FusionEngine

class SurveyEngine:
    def __init__(self, survey_id):
        self.base_path = os.path.join("surveys",survey_id)
        self.config = self.load_config()
        self.data_path = os.path.join(self.base_path, "data.csv")
        self.suspicious_path = os.path.join(self.base_path, "suspicious.csv")

    def load_config(self):
        with open(os.path.join(self.base_path, "config.json")) as f:
            return json.load(f)

    def load_data(self):
        if os.path.exists(self.data_path):
            return pd.read_csv(self.data_path)
        return pd.DataFrame()

    def save_data(self, df):
        df.to_csv(self.data_path, index=False)

    def save_suspicious(self, row, score):
        row["score"] = score

        df_data_columns = pd.read_csv(self.data_path, nrows=0).columns.tolist()
        df_data_columns.append('score')

        df = pd.DataFrame([row],columns=df_data_columns)
        if os.path.exists(self.suspicious_path):
            df.to_csv(self.suspicious_path, mode="a", header=False, index=False)
        else:
            df.to_csv(self.suspicious_path, index=False)

    def process_response(self, new_row):
        df_orginal = self.load_data()
        print(new_row)
        print(type(new_row))
        df_orginal = pd.concat( [df_orginal, pd.DataFrame([new_row])] , ignore_index=True)

        if len(df_orginal) < self.config["min_training_samples"]:
            self.save_data(df_orginal)
            return {"status": "Not enough data for anomaly detection yet."}

        df = df_orginal.copy()

        if self.config.get('columns_ignored'):
            for col in self.config.get('columns_ignored'):
                df=df.drop(col,axis=1)
        
        preprocessor = Preprocessor(self.config)
        X = preprocessor.fit_transform(df)

        layer_a = LayerA(self.config)
        layer_a.fit(X)
        local_score, local_info = layer_a.evaluate(X)

        layer_b = LayerB(self.config)
        layer_b.fit(X)
        global_score, global_info = layer_b.evaluate(X)

        fusion = FusionEngine(self.config)
        final_score = fusion.combine(local_score, global_score)

        result = {
            "anomaly_score": final_score,
            "local_details": local_info,
            "global_details": global_info
        }

        if final_score > self.config["suspicion_threshold"]:
            self.save_suspicious(new_row, final_score)
        else:
            self.save_data(df_orginal)
        
        return result