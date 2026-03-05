import numpy as np
from sklearn.neighbors import KernelDensity
from itertools import combinations

class LayerA:
    """
    Layer A: Pairwise Logical Density Engine
    Computes local anomaly score using KDE for top-K correlated feature pairs.
    """
    def __init__(self, config):
        self.config = config
        self.kde_models = {}  # Stores KDE models for each feature pair
        self.top_pairs = []   # List of top-K correlated feature pairs
        self.fitted = False

    def compute_correlations(self, X: np.ndarray, feature_names):
        """
        Compute correlations between each pair of features (numerical only)
        and select top-K pairs for KDE analysis.
        """
        n_features = X.shape[1]
        corr_matrix = np.corrcoef(X.T)  # Pearson correlation
        corr_matrix[np.isnan(corr_matrix)] = 0
        pairs = [(i, j, abs(corr_matrix[i, j])) for i in range(n_features) for j in range(i+1, n_features)]
        # Sort by absolute correlation descending
        pairs.sort(key=lambda x: x[2], reverse=True)
        k = self.config.get("correlation_top_k", 4)
        self.top_pairs = [(i, j) for i, j, _ in pairs[:k]]
        return self.top_pairs

    def fit(self, X: np.ndarray):
        """
        Fit KDE models on top-K feature pairs.
        """
        feature_names = np.arange(X.shape[1])
        self.compute_correlations(X, feature_names)

        for i, j in self.top_pairs:
            pair_data = X[:, [i, j]]
            kde = KernelDensity(kernel='gaussian', bandwidth=0.5).fit(pair_data)
            self.kde_models[(i, j)] = kde

        self.fitted = True

    def evaluate(self, X: np.ndarray):
        """
        Evaluate anomaly score for the last row of X using top-K KDE models.
        Returns:
            score: final normalized anomaly score
            info: details about individual pairwise densities
        """
        if not self.fitted:
            raise RuntimeError("LayerA must be fitted before evaluation.")
        last_row = X[-1, :]
        scores = []
        info = {}
        for (i, j), kde in self.kde_models.items():
            pair = last_row[[i, j]].reshape(1, -1)
            log_density = kde.score_samples(pair)[0]
            score = -log_density  # Higher score = more anomalous
            scores.append(score)
            info[f"pair_{i}_{j}"] = score # an absloute score
        
        # Exaggerating the error rate
        x = sum(scores)/len(scores)
        final_score = np.exp(x) / 5
        return final_score, info