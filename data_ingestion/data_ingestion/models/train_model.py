from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

def train_model(data, target_column):
    """
    Train a Random Forest model on the given data.

    Args:
        data (pd.DataFrame): Input features as a DataFrame.
        target_column (str): Name of the target column.

    Returns:
        RandomForestClassifier: Trained model.
    """
    try:
        X = data.drop(columns=[target_column])
        y = data[target_column]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        accuracy = model.score(X_test, y_test)
        print(f"Model accuracy: {accuracy * 100:.2f}%")

        return model
    except Exception as e:
        print(f"Error training model: {e}")
        return None
