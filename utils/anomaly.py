from sklearn.ensemble import IsolationForest
import numpy as np


def detect_anomaly(values):

    try:

        data = np.array(values).reshape(-1, 1)

        model = IsolationForest(
            contamination=0.1,
            random_state=42
        )

        preds = model.fit_predict(data)

        return preds

    except:

        return None