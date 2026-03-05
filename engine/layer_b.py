import numpy as np
from sklearn.covariance import EmpiricalCovariance
from sklearn.ensemble import IsolationForest

class LayerB:
    """
    Layer B: Global Statistical Distance Engine
    Computes Mahalanobis distance and Isolation Forest anomaly score.
    """
    def __init__(self, config):
        self.config = config
        self.mah_model = None
        self.iso_model = None
        self.fitted = False

    def fit(self, X: np.ndarray):
        """
        Fit both Mahalanobis and Isolation Forest models on historical data (excluding last row).
        """
        if X.shape[0] < 2:
            self.fitted = False
            return
        train_X = X[:-1]  # Exclude last row (new record)
        # Mahalanobis
        self.mah_model = EmpiricalCovariance().fit(train_X)
        # Isolation Forest
        self.iso_model = IsolationForest(contamination=0.01, random_state=42)
        self.iso_model.fit(train_X)
        self.fitted = True

    def evaluate(self, X: np.ndarray):
        """
        Evaluate anomaly score for the last row using Mahalanobis and Isolation Forest.
        Returns normalized score (0-1) and info dictionary.
        """
        if not self.fitted:
            return 0.0, {}

        last_row = X[-1, :].reshape(1, -1)
        # Mahalanobis distance
        mahal = self.mah_model.mahalanobis(last_row)[0]
        max_mah = max(self.mah_model.mahalanobis(X[:-1])) if X.shape[0] > 1 else 1.0
        norm_mahal = mahal / max_mah

        # Isolation Forest score (-1 anomaly, 1 normal)
        iso_score_raw = self.iso_model.score_samples(last_row)[0]
        iso_score = 1 - (iso_score_raw + 1)/2  # normalize 0-1

        # Combine scores internally (equal weight)
        combined_score = 0.5*norm_mahal + 0.5*iso_score

        info = {
            "mahalanobis": mahal,
            "norm_mahal": norm_mahal,
            "isolation_raw": iso_score_raw,
            "isolation_score": iso_score
        }

        return combined_score, info