class FusionEngine:
    """
    Fusion engine combines LayerA (local) and LayerB (global) anomaly scores.
    """
    def __init__(self, config):
        self.config = config

    def combine(self, local_score: float, global_score: float):
        """
        Combine scores using weighted sum or multiplicative ensemble.
        Returns final score (0-1).
        """
        alpha = 0.5
        beta = 0.5

        # Option 1: weighted sum
        final_score = alpha * local_score + beta * global_score

        # Option 2: multiplicative ensemble (optional)
        # final_score = 1 - (1 - local_score)*(1 - global_score)

        return final_score